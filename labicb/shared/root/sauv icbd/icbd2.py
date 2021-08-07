#! /usr/bin/python --
#travail realise par PITROU Adrien & CALVO-FERNANDEZ Adelie

print("--Debut programme--")

import string
import socket
import os
import pwd
import time
import sys
import select

class Icb:

	groups = 0
	srvname = "monServeur"
	line = ""
	tabCommande = ["nickname","group"]
	socket = None;
	server = "Monserveur" ,
	port = 666

	##recherche une commande et renvoie son indice dans la chaine de caracteres.
	def icb_cmd_lookup( flux ):
		print("--lookup--")

	##affiche l'aide
	def icb_cmd_help( flux):
		print("--help--")

	##Desactive la fonction de beep si possible
	def icb_cmd_beep( flux , user):
		print("--beep--")

	##passe les droits a un autre utilisateur
	def icb_cmd_boot( flux , user ):
		print("--boot--")

	##fait le changement de groupe pour un utilisateur.
	##si le groupe n'existe pas, la fonction doit le creer
	def icb_cmd_change( flux , user):
		print("--change--")

	##change le nom de l'utilisateur
	def icb_cmd_name( flux, user):
		print("--name--")

	##reactive la fonction de beep pour user (on, verbose ou off)
	def icb_cmd_nobeep( flux, user):
		print("--nobeep--")

	##envoie un message prive
	def icb_cmd_personal( _a4, _a8):
		print("--personal--")

	##prend ou libere le droit de moderation
	def icb_cmd_pass( _a4, _a8):
		print("--pass--")

	##change le sujet de la discussion
	def icb_cmd_topic( _a4, _a8):
		print("--topic--")

	##renvoie les membres du groupe
	def icb_cmd_who( _a4, _a8):
		print("--who--")

	#le lancement a la construction
	def icb_init():
		print("--init--")

	##initialise les variables de l'icb
	def icb_start( _a4):
		print("--start--")

	##verifie si la ligne est une commande correcte ou un message ?
	def icb_input( _a4):
		print("--input--")

	##lance une connexion avec login et mot de passe
	##si auccun groupe n'est cree, la methode en cree un
	##si le groupe passe n'existe pas, la methode le cree
	def icb_login( _a4, _a8, login, mdp):
		print("--login--")

	##envoie un message a un groupe de personnes ?
	def icb_groupmsg( _a4, _a8):
		print("--groupmsg--")

	##envoie un message prive
	def icb_privmsg( _a4, _a8, _a12):
		print("--privmsg--")

	##verifie si la commande existe
	def icb_command( _a4, _a8, _a12):
		print("--command--")

	## ???
	def icb_cmdout( _a4, _a8):
		print("--cmdout--")

	##verifie si le message peut s'envoyer correctement
	##sinon, fait une erreur
	def icb_status( _a4, _a8, _a12, _a16):
		print("--status--")

	##donne le statut du groupe.
	def icb_status_group( _a4, _a8, _a12, _a16, _a20):
		print("--status group--")

	##affiche une erreur
	def icb_error( _a4, _a8, _a12):
		print("--error--")

	##Enleve un membre du groupe.
	def icb_remove( _a4, _a8):
		print("--remove--")

	##ajoute un membre au groupe
	def icb_addgroup( _a4, _a8):
		print("--addgroup--")

	##Donne les infos du groupe ???
	def icb_dowho( _a4, _a8):
		print("--dowho--")

	##Recherche un membre ?
	def icb_who( _a4, _a8):
		print("--who--")

	##True si user est moderateur. False sinon
	def icb_ismod( flux, user):
		print("--ismod--")

	##Met a jour le moderateur ?
	def icb_modpermit( _a4, _a8):
		print("--modpermit--")

	##Passe la moderation a otheruser
	def icb_pass( flux, user, otheruser):
		print("--pass--")

	##Envoie le format d'envoi ?
	def icb_sendfmt( _a4, _a8, _a12):
		print("--sendfmt--")

	##Recupere un token
	def icb_token( _a4, _a8, _a12,_a16, _a20, _a24, _a28):
		print("--token--")

	##Efface les espaces au debut et a la fin
	def icb_trim( _a4, _a8):
		print("--trim--")

	##Visite le flux ?
	#def icb_vis( _a4, _a8, _a12, _a16):
	#	print("--vis--")

	##recupere la ligne courante#################################################

	def connect(self):
		self.socket = socket.socket ( socket.AF_INET , \
			socket.SOCK_STREAM )
		self.socket.connect (( self.server , self.port ))

	def __recv(self,length):
		retval = ""
		amt_read = 0
		while amt_read < length:
			retval = retval + self.socket.recv(length - amt_read)
			amt_read = len(retval)
		return retval

	def recv(self):
		print("--recv--")
		msg = ""
		length = ord(self.socket.recv(1))
		while length == 0:
			msg = msg + self.__recv(255)
			length = ord(self.socket.recv(1))
		if length != 1:
			msg = msg + self.__recv(length)
		if len(msg) <= 2:
			return [msg[0]]
		else:
			return [msg[0]] + string.split(msg[1:-1],'\001')

	##############################################################################

	##le main initialise les variables, affiche usage et ajoute des groupes et des
	##utilisateurs quand necessaire. Le tout en verifiant a chaque fois qu' il n'y a pass
	##de problemes

	#char* main(_unknown_ __ebx,_unknown_ __edi,_unknown_ __esi,char _a4)ICBD

class Icbd(Icb):

	##accepte, mais quoi ???
	def icbd_accept( __ebx, __edi, __esi,_a4, _a8, _a12):
		print("--accept--")

	##Met le flux en pause
	def icbd_paused( _a8, _a12):
		print("--paused--")

	##Affiche l'usage
	def usage(self):
		v12 = 'f'
		v16 = 0
		v20 = "Mon programme" #progname
		v24 = 0
		v28 = 0
		v32 = 0
		v36 = 0
		v52 = 0
		v68 = 0
		t29 = 0
		t39 = 0

		print("usage: [-46Cdv] [-G group1[,group2,...]] [-L prefix] [-M modtab]\n\t[-S name] [[addr][:port] ...]\n")

	##
	def icbd_ioerr( _a8, _a12):
		print("--ioerr--")

	def icbd_dispatch( __ebx, __esi,_a4, _a8):
		print("--dispatch--")

	def icbd_send( _a4, _a8, _a12):
		print("--send--")

	def icbd_drop( _a4, _a8):
		print("--drop--")

	def icbd_log( _a4, _a8, _a12, _a16):
		print("--log--")

	def icbd_modupdate():
		print("--modupdate--")

	def __init__(self):
		self.usage()
		self.icb_token(2, 3, 4, 5, 6, 7)
		self.connect()
		self.recv()

if __name__ == "__main__":
	print("--main--")
	app = Icbd()

print("--Fin programme--")
