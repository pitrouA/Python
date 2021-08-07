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
clients_connectes = []
socks=[]

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

def write_config_file(self,config_file = None):
	pass

def ad_hexa(nombre):
	if nombre < 10:
		return str(nombre)
	elif nombre == 10:
		return "a"
	elif nombre == 11:
		return "b"
	elif nombre == 12:
		return "c"
	elif nombre == 13:
		return "d"
	elif nombre == 14:
		return "e"
	else:
		return "f"



def ad_longueur_hexa(longueur):
	seizaines = 0
	while longueur > 16:
		longueur = longueur - 16
		seizaines = seizaines + 1
	return "\\x"+ad_hexa(seizaines)+""+ad_hexa(longueur)


def do_M_OPENMSG(p):
	print "message ouvert2"
	user = 'alice'
	msg2=p[0]+user+'\x01'+p[2] #recompose le message
	msg2=str(hex(len(msg2)+1))+msg2 #ajout de la taille
	print("--msg2 "+msg2+"--")
	#buf=msg2.encode('utf-8')
	#for sc in socks:
	socks[0].send(msg2)
	print ("--buffer "+buf)


def repondre(p):
	print("--repondre_"+p[0])
	c = p[0]
	if c == M_LOGIN:
		#do_M_LOGIN(p)
		print "login"
	elif c == M_OPENMSG:
		print "message ouvert"
		do_M_OPENMSG(p)
	elif c == M_PERSONAL:
		print "message perso"
		#do_M_PERSONAL(p)
	"""elif c == M_STATUS:
		#do_M_STATUS(p)
	elif c == M_ERROR:
		#do_M_ERROR(p)
	elif c == M_IMPORTANT:
		#do_M_IMPORTANT(p)
	elif c == M_EXIT:
		#do_M_EXIT(p)
	elif c == M_CMD_OUTPUT:
		#do_M_CMD_OUTPUT(p)
	elif c == M_PROTO:
		#do_M_PROTO(p)
	elif c == M_BEEP:
		#do_M_BEEP(p)
	elif c == M_PING:
		#do_M_PING(p)
	elif c == M_PONG:
		#do_M_PONG(p)
	else:
		#do_M_unknown(p)
"""


"""def parsemsg(msg):
	cmd_split = 0
	while cmd_split < len(msg) and msg[cmd_split] not in '\x01':
		cmd_split = cmd_split + 1
	cmd = string.lower(msg[:cmd_split])
	if cmd_split < len(msg):
		cmd_split = cmd_split + 1
	print cmd+"  "+msg[cmd_split:]
	repondre([cmd,msg[cmd_split:]])"""

def parsemsg(msg):
	ret = [msg[1], msg[:1], msg[2:]]#la commande est forcement en position 1
	print(ret)
	repondre(ret)

class Threadserveur(threading.Thread):
	def __init__(self,conn):
		threading.Thread.__init__(self)
		self.connexion = conn

	def run(self):
		nom=self.getName()
		print "nom1"+nom+"\n"
		while True:
			msg=self.connexion.recv(1024)
			msg=msg.decode('utf-8')
			print msg
			if msg=="":
				break
			parsemsg(msg)


def saveChat(nick, message):
	os.chdir("log")
	folderPath = "agora"
	filePath = folderPath + "/" + str(time.strftime("%Y-%m"))
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)
	if not os.path.exists(filePath):
		f = open(filePath, "a")
		f.write(nick + ": " + message + "\n")
		f.close()




def clientHandler(c):
	pass


def ad_connect(s, sc, addr):
	print("--ad_connect--")
	print("--nouvelle connexion--")


	print("--j--")
	#c.send("01\x01a\x01j1\x01\x00")
	msg2="\x0F"+M_PROTO+"1\x01daicbd\x01icbd\x00"
	buf=msg2.encode('utf-8')
	sc.send(buf)
	print ("--buffer ", buf)
	print addr
	clients_connectes.append((sc,addr))
	data = sc.recv(1024)
	msg = data.decode('utf-8')
	print ("--message ", msg)


	print("--a--")
	msg2="\x02"+M_LOGIN+"\x00"
	buf=msg2.encode('utf-8')
	sc.send(buf)
	print ("--buffer ", buf)


	print("--d--")
	msg3="\x23"+M_STATUS+"Status\x01You are now in group Agora\x00"
	buf=msg3.encode('utf-8')
	sc.send(buf)
	print ("--buffer ", buf)


	th=Threadserveur(sc)
	th.start()
	idthread=th.getName()
	print "idthread"+idthread



if __name__ == "__main__":
	print("--mainloop2--")
	#self.set_cbreak()
	saveChat("adad", "bonjour")
	lesgroupes=dict()
	lesgroupes["agora"]=[]
	s = socket(AF_INET,SOCK_STREAM)
	s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	s.bind(('0.0.0.0', 7326))
	s.listen(4)

	while 1:
		print("--while--")
		sc, addr = s.accept()

		#cherche si la socket existe. Sinon, lance la connexion
		if sc in socks:
			print("--contiens--")
		else:
			ad_connect(s, sc, addr)
			socks.append(sc)
