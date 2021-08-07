#! /usr/bin/python --


#./icbserv.py -4 -C -d -G agora -L log -n -S daicbd -v 0.0.0.0:7326 &
import string
import os
import pwd
import time
import sys
import select
import threading
from socket import *

"""now = time.time()
print now
print now.year
print now.month"""
default_server = "Default"
config_file = "/local/lib/servers"
server_dict = {'default': ['default.icb.net', 7326]}
server_name = "Evolve"
MAX_LINE = 239

M_LOGIN = 'a'
M_OPENMSG = 'b'
M_PERSONAL = 'c'
M_STATUS = 'd'
M_ERROR = 'e'
M_IMPORTANT = 'f'
M_EXIT = 'g'
M_COMMAND = 'h'
M_CMD_OUTPUT = 'i'
M_PROTO = 'j'
M_BEEP = 'k'
M_PING = 'l'
M_PONG = 'm'
alert_mode = 0

class IcbQuitException(Exception):
	pass


class Group():

	def __init__(self, nom):
		self.nom = nom
		self.users = []
		#self.nom = "Default"
		self.moderator = None
		self.topic = None


def write_config_file(self,config_file = None):
	pass

def do_M_LOGIN(sc,nom,p):
	msg2="\x02"+M_LOGIN+"\x00"
	buf=msg2.encode('utf-8')
	sc.send(buf)
	msg3="\x23"+M_STATUS+"Status\x01You are now in group Agora\x00"
	buf=msg3.encode('utf-8')
	sc.send(buf)
	print (buf)
	for th in lesgroupes["agora"].users:
		if th.connexion !=s and th.connexion!=sc:
			msg=M_STATUS+"Sign-on\x01"+nom+" ("+nom+"@"+str(th.adresse[0])+") entered group\x00"

			saveChat(msg)
			msg2=chr(len(msg))+msg
			buf=msg2.encode('utf-8')

			th.connexion.send(buf)

def send(socket,nom,msglist):
		msg = msglist[0]
		try:
			msg = msg + msglist[1]
		except:
			pass
		for i in msglist[2:]:
			msg = msg + '\001' + i
		msg = msg + '\000'
		if len(msg) > 254:
			print "*** mesg too long ***"
			msg = msg[:254]
		msg=nom+"\x01"+msg
		print "send"+msg
		socket.send(chr(len(msg))+msg)
		#saveChat(msg)


def do_M_OPENMSG(t,source,nom,p):
	for th in lesgroupes[t.group].users:
		if th.connexion !=s and th.connexion != source:
			send(th.connexion,M_OPENMSG+nom,p)




def do_M_PERSONAL(source,nom,p):
	dest=False
	#nom2 = ad_recupererArgument(p)
	nom2 = p[0].split(' ')
	for th in clients_connectes:
		print(th.nom)
		if nom2[0] == th.nom: #th.connexion !=s and th.connexion != source and
			send(th.connexion,M_PERSONAL+nom,nom2[1])
			dest=True
	#si le destinataire n'existe pas
	if dest:
		send(source,M_ERROR+"No such user"+nom2[0],[" "])


def do_M_EXIT(t):
	th.connexion.close()
	lesgroupes[t.group].users.remove(t)
	clients_connectes.remove(t)
	for th in lesgroupes[t.group].users:
		if th.connexion !=s:
			send(th.connexion,M_OPENMSG+"Depart",[th.nom+" ("+th.nom+"@"+str(th.adresse[0])+") just left"])



def do_M_GROUP(th, p):

	groupName = p.split(' ')[0]

	if th.group == groupName: #l'utilisateur est deja dans le groupe
		return

	lesgroupes[th.group].users.remove(th)# enleve du groupe precedent
	for thr in lesgroupes[th.group].users:
		send(thr.connexion,M_OPENMSG+"Depart",[th.nom+" ("+th.login+"@"+str(th.adresse[0])+") just left"])

	if groupName not in lesgroupes: #la cle n'existe pas deja dans lesgroupes
		lesgroupes[groupName]=Group(groupName)#cree un nouveau groupe
		lesgroupes[groupName].moderator = th #donne la moderation
		send(th.connexion,M_OPENMSG+"Status",["You are now in group "+groupName+" as moderator"])
	else:
		send(th.connexion,M_OPENMSG+"Status",["You are now in group "+groupName])
		for thr in lesgroupes[groupName].users:
			if thr != th:
				send(thr.connexion,M_OPENMSG+"Arrivee",[th.nom+" ("+th.nom+"@"+str(th.adresse[0])+") entered group"])



	lesgroupes[groupName].users.append(th)# ajout dans le groupe
	th.group = groupName # change l'utilisateur de groupe

	for gr in lesgroupes:
		print(lesgroupes[gr].users)

def do_M_RECAP(th, sc, nom, p):
	for group in lesgroupes:
		moderator = "(None)"
		topic = "(None)"
		if lesgroupes[group].moderator != None:
			moderator = lesgroupes[group].moderator.nom
		#if
		if lesgroupes[group].topic != None:
			topic = lesgroupes[group].topic
		#if
		send(th.connexion,"ico",["Group : "+group+" (mvl) Mod : "+moderator+"\t Topic : "+topic]) #envoi de ico
		for user in lesgroupes[group].users:
			mod = 'm'
			if lesgroupes[group].moderator == user: #l'info de moderation
				mod = ' '
			#if
			send(th.connexion,"iwl",[mod+"\x01",user.nom,str(int(time.time()-user.timeConnected)),"0",str(int(user.timeConnected)),user.login,user.adresse[0]," "]) #info utilisateur
		#for
	#for
	send(th.connexion,"ico",["Total : "+str(len(clients_connectes))+" users in "+str(len(lesgroupes))+" groups"]) #info de fin
#def

def do_M_PASS(th, sc, nom, p):
	#on passe la moderation
	if lesgroupes[th.group].moderator==None:
		lesgroupes[th.group].moderator=th
		print "server has passed moderation to "+th.nom
		send(th.connexion,M_OPENMSG+"Notify",["server just passed you moderation of "+th.group])
		for t in lesgroupes[th.group].users:
			if t!= th:
				send(t.connexion,M_OPENMSG+"Notify",["server has passed moderation to "+th.nom])
		saveChat("server has passed moderation to "+th.nom)

	#deja modo on pass la moderation au serveur
	elif lesgroupes[th.group].moderator==th:
		lesgroupes[th.group].moderator=None
		for t in lesgroupes[th.group].users:

			send(t.connexion,M_OPENMSG+"Notify",[th.nom+" has passed moderation to server"])
		saveChat("server has passed moderation to "+th.nom)

	#il y a deja un modo
	else:
		send(th.connexion,M_ERROR+"Operation not permitted.",[" "])
		saveChat("[*Error*] Operation not permitted.")

def do_M_NAME(th,p):
	if(p[0]!=""):
		nom=p[0]
		send(th.connexion,M_STATUS+"Name",[th.nom+" changed nickname to "+nom])
		th.nom=nom
		saveChat(th.nom+" changed nickname to "+nom)
	else:
		send(th.connexion,M_STATUS+"Name",["Your nickname is "+th.nom])

def do_M_TOPIC(th, p):
	group = lesgroupes[th.group]
	if(p!=""):
		if group.moderator == th: #si moderateur
			send(th.connexion,M_STATUS+"Topic",[th.nom+" changed topic to \""+p+"\""])
			group.topic=p
			saveChat(th.nom+" changed topic to "+p)
		else: #pas le droit de modifier le topic
			send(th.connexion,M_STATUS+"Notify",["Setting the topic is not only for moderators."])
		#if
	#if
	else: #donne le topic si defini
		if(group.topic == None):
			send(th.connexion,M_STATUS+"Topic",["The topic is not set."])
		else:
			send(th.connexion,M_STATUS+"Topic",["The topic is : "+group.topic])
		#if
	#if
#def

def commande(th, sc,nom,p):
	c = p[0]
	if c=="m":
		print("--mes_personnel : "+nom+"--")
		print(p[1:])
		do_M_PERSONAL(sc,nom,p[1:])
	elif c=="w":
		print("--recap--")
		do_M_RECAP(th, sc, nom, p[1])
	elif c=="g":
		print("--group--")
		do_M_GROUP(th, p[1])
	elif c=="topic":
		print("--topic--")
		do_M_TOPIC(th, p[1])
	elif c=="pass":
		print("--pass--")
		do_M_PASS(th, sc, nom, p[1:])
	elif c=="name":
		print("--name--")
		do_M_NAME(th,p[1:])
	elif c=="?":
		send(th.connexion,M_STATUS+"Help",["beep boot g m name nobeep pass topic w"])
		print("aide")
	elif c=="q":
		print("quitter")
		do_M_EXIT(th)
	else:
		send(th.connexion,M_ERROR+"Unsupported command: "+c,[" "])

def repondre(th, sc,nom,p):
	c = p[0]
	print "C"+c

	if c == M_OPENMSG:
		print "message ouvert"
		do_M_OPENMSG(th,sc,nom,p[1:])
	elif c == M_PERSONAL:
		print "message perso"
		do_M_PERSONAL(sc,nom,p[1:])
	elif c == M_COMMAND:
		print "command"
		print p[1:]
		commande(th, sc,nom,p[1:])
	"""elif c == M_STATUS:
		do_M_STATUS(p)
	elif c == M_ERROR:
		do_M_ERROR(p)
	elif c == M_IMPORTANT:
		do_M_IMPORTANT(p)
	elif c == M_EXIT:
		do_M_EXIT(p)
	elif c == M_CMD_OUTPUT:
		do_M_CMD_OUTPUT(p)"""
	"""elif c == M_BEEP:
		do_M_BEEP(p)
	elif c == M_PING:
		do_M_PING(p)
	elif c == M_PONG:
		do_M_PONG(p)
	else:
		do_M_unknown(p)"""


def __recv(length,socket):
	retval = ""
	amt_read = 0
	while amt_read < length:
		retval = retval + socket.recv(length - amt_read)
		amt_read = len(retval)
	print "RETVAL"+retval
	return retval

def recv(socket):
	msg = ""
	length = ord(socket.recv(1))
	while length == 0:
		msg = msg +__recv(255,socket)
		length = ord(socket.recv(1))
	if length != 1:
		msg = msg +__recv(length,socket)
	if len(msg) <= 2:
		return [msg[0]]
	else:
		return [msg[0]] + string.split(msg[1:-1],'\001')

def process_cmd(self, cmd, line):
	if cmd == 'q':
		raise self.IcbQuitException
	elif cmd == 'm':
		s = string.split(line)
		if len(s) > 0:
			if s[0] in self.m_personal_history:
				self.m_personal_history.remove(s[0])
			self.m_personal_history.append(s[0])
		self.command(cmd, line)
	else:
		self.command(cmd, line)

def _parse_cmd(self, command_line):
	cmd_split = 0
	while cmd_split < len(command_line) and command_line[cmd_split] not in ' \t':
		cmd_split = cmd_split + 1
	cmd = string.lower(command_line[:cmd_split])
	if cmd_split < len(command_line):
		cmd_split = cmd_split + 1
	self.process_cmd(cmd,command_line[cmd_split:])

def process_user(self, userline = None):
	if userline == None:
		userline = self.userline
	if userline != None:
		if userline[0] == '/':
			if len(userline) > 1:
				if userline[1] == '/':
					self.openmsg(userline[1:])
				else:
					self._parse_cmd(userline[1:])
			else:
				self.show([self.M_STATUS, "Error", \
					"empty command"])
		else:
			self.openmsg(userline)



class Threadserveur(threading.Thread):

	def __init__ (self,conn,ad):
		threading.Thread.__init__(self)
		self.connexion = conn
		self.nom=None
		self.adresse=ad
		self.group = "agora"
		self.timeConnected = time.time()
		self.login = None #pour /w

	def run(self):
		#nom=self.getName()
		while True:
			msg=recv(self.connexion)
			print "MSG"
			print msg
			print "ADR"
			print self.adresse

			print self.connexion
			if msg=="":
				break
			elif msg[0]== M_LOGIN:
				self.nom=msg[2]
				self.login = self.nom
				print "NOM"
				print self.nom
				do_M_LOGIN(sc,self.nom,msg)
			repondre(self, self.connexion,self.nom,msg)



def saveChat(message):

	folderPath = "agora"
	filePath = folderPath + "/" + str(time.strftime("%Y-%m"))
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)

	f = open(filePath, "a")
	f.write(str(time.strftime("%H:%M")) + ": " + message + "\n")
	f.close()


def clientHandler(c):
	pass


if __name__ == "__main__":
	os.chdir("log")
	saveChat("bonjour")
	lesgroupes=dict()
	lesgroupes["agora"]=Group("agora")
	print("le serveur")
	clients_connectes = []
	s = socket(AF_INET,SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

	s.bind(('0.0.0.0',7326))
	s.listen(4)

	socks=[s]
	while True:
		rlist, wlist, xlist =select.select(socks, [], [])

		for t in rlist:
			sc, addr = s.accept()
			#if t==s and sc not in clients_connectes:
			msg2="\x0F"+M_PROTO+"1\x01daicbd\x01icbd\x00"
			buf=msg2.encode('utf-8')
			sc.send(buf)
			print sc
			print addr
			th=Threadserveur(sc,addr)
			th.start()
			idthread=th.getName()
			clients_connectes.append(th)

			#ajout dans le groupe agora
			lesgroupes["agora"].users.append(th)
