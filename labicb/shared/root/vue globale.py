
class IcbConn:#connexions de l'IBC

	#lit un fichier et remplit server_dict et default_server
	def read_config_file(self,config_file = None)

	#appelle read_config_file et remplit les champs de l'objet ( constructeur )
	def __init__ ( self , nic = None , group = None , logid = None , server = None , port = None )

	#ouvre une connexion
	def connect(self)

	#verifie si le fichier existe
	def fileno(self)

	#receptionne les prochaines informations
	def __recv(self,length)
	def recv(self)

	#envoie les informations
	def send(self,msglist)

	#envoie le login SEND
	def login(self, command = 'login')

	#coupe la connexion
	def close(self)

	#envoie un message LOGIN
	def openmsg(self, msg)

	#envoie une commande LOGIN
	def command(self, cmd, args)

class IcbSimple(IcbConn) #la base de l'application

	#exception
	class IcbQuitException(Exception)

	#affichage du temps
	def pretty_time(self,secs)

	#ecrit une ligne dans un fichier
	def print_line(self,line)

	#
	def indent_print(self,indent, msg)

	#fait les affichages de boite de message
	def do_M_LOGIN(self,p)
	def do_M_OPENMSG(self,p)
	def do_M_PERSONAL(self,p)
	def do_M_STATUS(self,p)
	def do_M_ERROR(self,p)
	def do_M_IMPORTANT(self,p)
	def do_M_EXIT(self,p)

	#les actions a saisir
	def do_C_GENERIC(self,p)
	def do_C_END(self,p)
	def do_C_WHO_LIST(self,p)
	def do_C_WHO_GROUP(self,p)
	def do_C_WHO_HEAD(self,p)
	def do_C_GROUP_HEAD(self,p)
	def do_C_CLIENT_CMD_LIST(self,p)
	def do_C_CLIENT_LIST(self,p)
	def do_C_unknown(self,p)

	#fait les messages
	def do_M_CMD_OUTPUT(self,p)
	def do_M_PROTO(self,p)
	def do_M_BEEP(self,p)
	def do_M_PING(self,p)
	def do_M_PONG(self,p)
	def do_M_unknown(self,p)

	#dernier paquet du recv
	def recv(self)

	#affichage
	def show(self,p = None)

	#
	def select(self)

	#
	def user_recv(self)

	#effectue les commandes SHOW
	def process_cmd(self, cmd, line)

	#convertit une commande
	def _parse_cmd(self, command_line)

	#OPENMSG SHOW PROCESS_CMD
	def process_user(self, userline = None)

class IcbTerminalApp(IcbSimple) #adaptation au terminal

	#
	def on_stop(self, sig, stack)

	#
	def set_cbreak(self)

	#
	def restore_termios(self)

	#SHOW
	def do_display_cmd(self, cmd, line)

	#SHOW
	def process_cmd(self, cmd, line)

	#affiche le curseur avant l'ouverture d'un message
	def openmsg(self, msg)

	#
	def _remember_line(self,line)

	#
	def print_line(self,line,remember=1)

	#ecrit n backspace
	def _backspace(self, n)

	#fait l'action des saisies du terminal
	def process_char(self,c,line)

	#
	def readline(self,file)

	#
	def user_recv(self)

	#boucle principale de l'application RECV LOGIN CLOSE SHOW PROCESS_USER
	def mainloop(self)

	#constructeur CONNECT
	def __init__(self)

class IcbPersonalized(IcbTerminalApp) #main

	#fait le main ( lance init de IcbTerminalApp )
