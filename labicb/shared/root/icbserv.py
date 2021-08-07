#! /usr/bin/python --
# -*- coding: utf-8 -*-

##################################################################################
##            Copyright (c) 2017 PITROU Adrien & CALVO-FERNANDEZ Adelie         ##
##################################################################################
## Projet realise dans le cadre de la l3 INFORMATIQUE specialite INGE de        ##
## l'universite d'ORLEANS par 2 eleves du groupe 1.                             ##
## Le projet RESEAU consistait en une reecriture d'un serveur fourni : icbd     ##
## ( format .ELF ). Ci-dessous une retranscription possible.                    ##
## Ce serveur correspond a un laboratoire NETKIT contenant entre autre icb.py   ##
## le client. Le laboratoire est a lancer avec lstart et le serveur.startup     ##
## doit lancer la ligne suivante au demarrage :                                 ##
##      ./icbserv.py -4 -C -d -G agora -L log -n -S daicbd -v 0.0.0.0:7326 &    ##
## Ce projet peut contenir des bugs & erreurs.                                  ##
##################################################################################

import string
import os
import pwd
import time
import sys
import select
import threading
from socket import *

## variables globales de l'application

default_server = "Default"
config_file = "/local/lib/servers"
server_dict = {'default': ['default.icb.net', 7326]}
server_name = "Evolve"
MAX_LINE = 239
alert_mode = 0

## constantes de icb les memes commandes sont utilisees

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

##Classe pour modeliser une exception produite lors de la deconnexion
class IcbQuitException(Exception):
	pass
#class

##Classe pour modeliser un groupe
class Group():

	def __init__(self, nom):
		self.nom = nom
		self.users = []
		self.moderator = None
		self.topic = None
	#def
#class

##Actions liees a une demande de connexion d'un client
def do_M_LOGIN(t,sc,nom,p):
	msg2="\x02"+M_LOGIN+"\x00" #envoie les messages de connexion au nouveau client
	buf=msg2.encode('utf-8')
	sc.send(buf)
	msg3="\x23"+M_STATUS+"Status\x01You are now in group Agora\x00"
	buf=msg3.encode('utf-8')
	sc.send(buf)
	for th in lesgroupes["agora"].users: #envoie l'information a tout les autres clients deja connectes
		if th.connexion !=s and th.connexion!=sc:
			msg=M_STATUS+"Sign-on\x01"+nom+" ("+nom+"@"+str(th.adresse[0])+") entered group\x00"
			msg2=chr(len(msg))+msg
			buf=msg2.encode('utf-8')
			th.connexion.send(buf)
		#if
	#for
	saveChat(t.group,nom+" ("+nom+"@"+str(t.adresse[0])+") entered group\x00")
#def

##Transforme les parametres en un message a envoyer par la socket
def send(socket,nom,msglist):
		msg = msglist[0]
		try:
			msg = msg + msglist[1]
		except:
			pass
		#try
		for i in msglist[2:]:
			msg = msg + '\001' + i
		#for
		msg = msg + '\000'
		if len(msg) > 254:
			print "*** mesg too long ***"
			msg = msg[:254]
		#if
		msg=nom+"\x01"+msg
		socket.send(chr(len(msg))+msg)
#def

##Actions liees a l'envoi d'un message ouvert par un client
def do_M_OPENMSG(t,source,nom,p):
	for th in lesgroupes[t.group].users: #envoie le message aux membres du groupe
		if th.connexion !=s and th.connexion != source:
			send(th.connexion,M_OPENMSG+nom,p)
		#if
	#for
	saveChat(t.group,"<"+nom+"> "+" ".join(p))
#def

##Actions liees a l'envoi d'un message personnel par un client
def do_M_PERSONAL(th,nom,p):
	dest=False
	if len(p)==0:
		send(th.connexion,M_ERROR+"Empty message",[" "])
		return
	if len(p[0])<2:
		send(th.connexion,M_ERROR+"Empty message",[" "])
		return
	nom2 = p[0].split(' ')
	msg=" ".join(nom2[1:])
	if msg!="":
		for t in lesgroupes[th.group].users: #cherche le bon client a qui envoyer le message
			if nom2[0] == t.nom:
				send(t.connexion,M_PERSONAL+nom,[msg])
				dest=True
	else: #si le message est vide, ne l'envoie pas
		send(th.connexion,M_ERROR+"Empty message",[" "])
		return

	if dest==False: #si le destinataire n'existe pas
		send(th.connexion,M_ERROR+"No such user "+nom2[0],[" "])
#def

##Actions liees a une demande de fermeture d'un client
def do_M_EXIT(t):
	t.connexion.close()
	if lesgroupes[t.group].moderator == t: #rend la moderation si besoin
		lesgroupes[t.group].moderator = None
	#if
	lesgroupes[t.group].users.remove(t)
	clients_connectes.remove(t)
	for th in lesgroupes[t.group].users: #Envoie l'information aux membres du groupe
		if th!=t:
			send(th.connexion,M_STATUS+"Sign-off",[t.nom+" ("+t.nom+"@"+str(t.adresse[0])+") just left"])
		#if
	#for
	saveChat(t.group,t.nom+" ("+t.nom+"@"+str(t.adresse[0])+") just left")
#def

##Actions liees a une demande de changement de groupe d'un client
def do_M_GROUP(th, p):
	groupName = p.split(' ')[0]
	groupName= groupName.strip()
	if groupName=="": #verifie si le nom de groupe est valide
		send(th.connexion,M_ERROR+"Invalid group name",[" "])
		return
	#if
	if th.group == groupName: #l'utilisateur est deja dans le groupe
		return
	#if
	saveChat(th.group,th.nom+" ("+th.nom+"@"+str(th.adresse[0])+") just left")
	lesgroupes[th.group].users.remove(th)# enleve du groupe precedent

	for thr in lesgroupes[th.group].users: #envoie l'information de depart aux membres de l'ancien groupe
		send(thr.connexion,M_STATUS+"Depart",[th.nom+" ("+th.login+"@"+str(th.adresse[0])+") just left"])
	#for
	if lesgroupes[th.group].moderator == th: #rend la moderation si besoin
		lesgroupes[th.group].moderator = None
	#if
	
	if groupName not in lesgroupes: #la cle n'existe pas deja dans lesgroupes
		lesgroupes[groupName]=Group(groupName)#cree un nouveau groupe
		lesgroupes[groupName].moderator = th #donne la moderation
		send(th.connexion,M_STATUS+"Status",["You are now in group "+groupName+" as moderator"])
	else:
		send(th.connexion,M_STATUS+"Status",["You are now in group "+groupName])
		for thr in lesgroupes[groupName].users: #envoie l'information aux membre du nouveau groupe
			if thr != th:
				send(thr.connexion,M_STATUS+"Arrivee",[th.nom+" ("+th.nom+"@"+str(th.adresse[0])+") entered group"])
			#if
		#for
	#if
	lesgroupes[groupName].users.append(th)# ajout dans le groupe
	th.group = groupName # change l'utilisateur de groupe
	saveChat(th.group,th.nom+" ("+th.nom+"@"+str(th.adresse[0])+") entered group")
#def

##Actions liees a une demande de recap d'un client
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
		for user in lesgroupes[group].users: #envoie une information pour chaque autre membre du groupe
			mod = ' '
			if lesgroupes[group].moderator == user: #l'info de moderation
				mod = 'm'
			#if
			send(th.connexion,"iwl",[mod+"\x01",user.nom,str(int(time.time()-user.timeConnected)),"0",str(int(user.timeConnected)),user.login,user.adresse[0]," "]) #info utilisateur
		#for
	#for
	send(th.connexion,"ico",["Total : "+str(len(clients_connectes))+" users in "+str(len(lesgroupes))+" groups"]) #info de decompte
	send(th.connexion,"iec",["Fin"]) #info de fin
#def

##Actions liees a une demande de passation / prise de moderation d'un client
def do_M_PASS(th, sc, nom, p):
	if lesgroupes[th.group].moderator==None: #on passe la moderation
		lesgroupes[th.group].moderator=th
		send(th.connexion,M_STATUS+"Notify",["server just passed you moderation of "+th.group])
		for t in lesgroupes[th.group].users: #fait passer l'info aux membres du groupe
			if t!= th:
				send(t.connexion,M_STATUS+"Notify",["server has passed moderation to "+th.nom])
			#if
		#for
		saveChat(th.group,"server has passed moderation to "+th.nom)
	elif lesgroupes[th.group].moderator==th: #deja modo on pass la moderation au serveur
		lesgroupes[th.group].moderator=None
		for t in lesgroupes[th.group].users:
			send(t.connexion,M_STATUS+"Notify",[th.nom+" has passed moderation to server"])
		#for
		saveChat(th.group,"server has passed moderation to "+th.nom)
	#if
	else: #il y a deja un modo
		send(th.connexion,M_ERROR+"Operation not permitted.",[" "])
	#if
#def

##Actions liees a une demande de renomage d'un client
def do_M_NAME(th,p):
	if(p[0]!=""): #le /pass nom -> renomage
		nom=p[0]
		send(th.connexion,M_STATUS+"Name",[th.nom+" changed nickname to "+nom])
		saveChat(th.group,th.nom+" changed nickname to "+nom)
		th.nom=nom
	else: #/pass -> donne le surnom
		send(th.connexion,M_STATUS+"Name",["Your nickname is "+th.nom])
	#if
#def

##Actions liees a une demande de changement de sujet d'un client
def do_M_TOPIC(th, p):
	group = lesgroupes[th.group]
	if(p!=""): #/topic sujet
		if group.moderator == th: #si moderateur
			send(th.connexion,M_STATUS+"Topic",[th.nom+" changed topic to \""+p+"\""])
			group.topic=p
			saveChat(th.group,th.nom+" changed topic to "+p)
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

##Actions liees a une demande d' exclusion d'un client
def do_M_BOOT(th, p):
	if lesgroupes[th.group].moderator != th:
		send(th.connexion,M_STATUS+"Notify",["Sorry, booting is a privilege you don't possess"])
		return
	#if
	if(p[0]!=""): #le /pass nom -> renomage
		nom=p[0]
		for t in lesgroupes[th.group].users: #cherche la cible a expulser
			if t.nom == nom: #la cible trouvee
				send(t.connexion,"g",[" "]) #deconnecte le client
				t.connexion.close() #deconnecte
				t.connexion = None #pour sortir du run de Client
				lesgroupes[t.group].users.remove(t)
				clients_connectes.remove(t)
				for thr in lesgroupes[th.group].users: #Envoie l'information aux membres du groupe restants
					send(thr.connexion,M_STATUS+"Sign-off",[t.nom+" ("+t.nom+"@"+str(t.adresse[0])+") just left: booted"])
				#for
				saveChat(t.group,t.nom+" ("+t.nom+"@"+str(t.adresse[0])+") just left")
				return
			#if
		#for
		send(th.connexion,M_STATUS+"Notify",["No such user"])
	else: #/pass -> erreur
		send(th.connexion,M_ERROR+"Invalid user",[" "])
	#if
#def

##Lance l'action adequate selon la commande invoquee ( de 'a' a 'm' )
def commande(th, sc,nom,p):
	c = p[0]
	if c=="m":
		do_M_PERSONAL(th,nom,p[1:])
	elif c=="w":
		do_M_RECAP(th, sc, nom, p[1])
	elif c=="g":
		do_M_GROUP(th, p[1])
	elif c=="topic":
		do_M_TOPIC(th, p[1])
	elif c=="pass":
		do_M_PASS(th, sc, nom, p[1:])
	elif c=="name":
		do_M_NAME(th,p[1:])
	elif c=="boot":
		do_M_BOOT(th,p[1:])
	elif c=="?":
		send(th.connexion,M_STATUS+"Help",["beep boot g m name nobeep pass topic w"])
	elif c=="q":
		do_M_EXIT(th)
	else:
		send(th.connexion,M_ERROR+"Unsupported command: "+c,[" "])
	#if
#def

##Lance l'action adequate selon la commande invoquee ( de 'a' a 'm' )
def repondre(th, sc,nom,p):
	c = p[0]
	if c == M_OPENMSG:
		do_M_OPENMSG(th,sc,nom,p[1:])
	elif c == M_PERSONAL:
		do_M_PERSONAL(th,nom,p[1:])
	elif c == M_COMMAND:
		commande(th, sc,nom,p[1:])
	#if
#def

##Fonction cachee -> attend et decoupe les informations reçues sur les thread
def __recv(length,socket):
	retval = ""
	amt_read = 0
	while amt_read < length:
		retval = retval + socket.recv(length - amt_read)
		amt_read = len(retval)
	#while
	return retval
#def

##Attend et decoupe les informations reçues sur les thread. Utilise __recv pour cela.
def recv(socket):
	msg = ""
	test=socket.recv(1)
	if test:
		length = ord(test)
		while length == 0:
			msg = msg +__recv(255,socket)
			length = ord(socket.recv(1))
		#while
		if length != 1:
			msg = msg +__recv(length,socket)
		#if
		if len(msg) <= 2:
			return [msg[0]]
		else:
			return [msg[0]] + string.split(msg[1:-1],'\001')
		#if
	else:
		raise IcbQuitException
	#if
#def

##Classe pour modeliser un client. La classe etend Thread pour gerer
##des actions asynchrones entre clients
class Client(threading.Thread):

	def __init__ (self,conn,ad):
		threading.Thread.__init__(self)
		self.connexion = conn
		self.nom=None
		self.adresse=ad
		self.group = "agora"
		self.timeConnected = time.time()
		self.login = None #pour /w
	#def

	def run(self):
		#nom=self.getName()
		while True:
			try:
				msg=recv(self.connexion)
			except:
				if self.connexion != None: #non-deboote
					do_M_EXIT(self)
				#if
				return
			#try
			if len(msg)<0:
				return
			elif msg[0]== M_LOGIN:
				self.nom=msg[2]
				self.login = self.nom
				do_M_LOGIN(self,sc,self.nom,msg)
			#if
			repondre(self, self.connexion,self.nom,msg)
		#while
	#def
#class

##Sauvegarde les messages recus par ce serveur dans le fichier de chemin passe en parametres
def saveChat(folderPath,message):
	print "[icbd]: "+message
	filePath = folderPath + "/" + str(time.strftime("%Y-%m"))
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)
		print "[icbd]: logger_open: log/"+filePath
	#if
	f = open(filePath, "a")
	f.write(str(time.strftime("[%H:%M]")) + ": " + message + "\n")
	f.close()
#def

## Le main. Initialise les tableaux de clients et de groupes et gere l'arrivee de nouveaux clients.
## Une fois cree la classe client prend en charge les actions correspondant a ce client precis et,
## par consequent, le main n'a pas besoin de s'en charger. Il retourne donc dans un etat d'attente
## d'une nouvelle connexion.
if __name__ == "__main__":
	os.chdir("log")
	lesgroupes=dict()
	lesgroupes["agora"]=Group("agora")
	print("Bienvenue sur le serveur d'Adélie et Adrien")
	clients_connectes = []
	s = socket(AF_INET,SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind(('0.0.0.0',7326))
	s.listen(4)
	socks=[s]

	while True:
		rlist, wlist, xlist =select.select(socks, [], []) #synchronisation

		for t in rlist: #clients connectes
			sc, addr = s.accept()
			msg2="\x0F"+M_PROTO+"1\x01daicbd\x01icbd\x00"
			buf=msg2.encode('utf-8')
			sc.send(buf)
			th=Client(sc,addr) #nouveau client / fil d'execution
			th.start()
			idthread=th.getName()
			clients_connectes.append(th)
			lesgroupes["agora"].users.append(th) #ajout dans le groupe agora
		#for
	#while
#if main
