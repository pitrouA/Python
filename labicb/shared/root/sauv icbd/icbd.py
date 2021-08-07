#! /usr/bin/python --
##

## Copyright (c) 2011, Michael C. Thornburgh
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without modification,
## are permitted provided that the following conditions are met:
##
## 1. Redistributions of source code must retain the above copyright notice,
## this list of conditions and the following disclaimer.
##
## 2. Redistributions in binary form must reproduce the above copyright notice,
## this list of conditions and the following disclaimer in the documentation
## and/or other materials provided with the distribution.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
## DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
## CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
## OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

##
## icbd connection object
##

import string
from socket import *
import os
import pwd
import time
import sys
import select
import threading

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

class icbdConn:
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

	default_server = "Default"
	config_file = "/local/lib/serversIcbd"
	server_dict = {'default': ['default.icbd.net', 7326]}
	server_name = "Evolve"
	MAX_LINE = 239

	def read_config_file(self,config_file = None):
		if config_file == None:
			config_file = self.config_file
		try:
			f = open(config_file, "r")
		except:
			self.print_line("warning: can't read config file, using defaults.")
			return
		i = f.readline()
		first_one = 1
		line = 0
		while i != "":
			line = line + 1
			if i[0] == '#':
				i = f.readline()
				continue
			i_split = string.split(i)
			if len(i_split) < 4:
				self.print_line("warning: config file syntax error line %d" % (line))
				i = f.readline()
				continue
			s_name = string.lower(i_split[0])
			self.server_dict[s_name] = [i_split[1], \
				string.atoi(i_split[3]), i_split[0]]
			if first_one:
				self.default_server = i_split[0]
				first_one = 0
			i = f.readline()

	def __init__ ( self ,
	  group = None ,
	  logid = None ,
	  server = None ,
	  port = None ):
	  	print("--init2--")
		self.read_config_file()
		if logid != None:
			self.logid = logid
		else:
			self.logid = pwd.getpwuid(os.getuid())[0]
		#if nic != None:
		#	self.nickname = nic
		#else:
		#	self.nickname = self.logid
		print("--group--")
		if group != None:
			self.group = group
		else:
			self.group = '1'
		print("--server--")
		if server != None:
			if self.server_dict.has_key(string.lower(server)):
				self.server = self.server_dict[string.lower(server)][0]
				self.server_name = self.server_dict[string.lower(server)][2]
			else:
				print("--server default--")
				self.server = "alice"#server
				self.server_name = server
		else:
			self.server = self.server_dict[string.lower(self.default_server)][0]
			self.server_name = self.default_server
		print("--port--")
		if port != None:
			self.port = port
		else:
			self.port = self.server_dict[string.lower(self.default_server)][1]
		self.socket = None
		print("--fin init2--")

	def connect(self):
		self.socket = socket.socket ( socket.AF_INET , \
			socket.SOCK_STREAM )
		self.socket.connect (( self.server , self.port ))

	def fileno(self):
		return self.socket.fileno()

	def __recv(self,length):
		retval = ""
		amt_read = 0
		while amt_read < length:
			retval = retval + self.socket.recv(length - amt_read)
			amt_read = len(retval)
		return retval

	def recv(self):
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

	def send(self,msglist):
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
		self.socket.send(chr(len(msg))+msg)

	def login(self, command = 'login'):
		self.send([self.M_LOGIN, self.logid,
		  self.nickname, self.group, command, ''])

	def close(self):
		self.socket.close()

	def openmsg(self, msg):
		self.send([self.M_OPENMSG, msg])

	def command(self, cmd, args):
		self.send([self.M_COMMAND, cmd, args])

class icbdSimple(icbdConn):
	last_packet = []
	beeps_ok = 1
	alert_mode = 0
	last_alert = 0
	term_width = 80
	term_height = 24
	right_margin = 2
	input_file = sys.stdin
	output_file = sys.stdout
	class icbdQuitException(Exception):
		pass
	m_personal_history = []

	def pretty_time(self,secs):
		if secs == 0:
			return '-'
		if secs < 60:
			return "%ds" % (secs)
		if secs < 3600:
			return "%dm%ds" % (int(secs/60), secs % 60)
		if secs >= 3600:
			return "%dh%dm" % (int(secs/3600), int((secs%3600)/60))

	def print_line(self,line):
		output_line = line
		now = time.time()
		if (self.alert_mode == 1) and (now - self.last_alert > 0.5):
			output_line = '\007' + output_line
			self.last_alert = now
		output_line = output_line + '\n'
		self.output_file.write(output_line)

	def indent_print(self,indent, msg):
		left = 0
		max_line = self.term_width - len(indent) - 1 - self.right_margin
		while len(msg) - left > max_line:
			right = left + max_line
			while right > left and msg[right] not in ' \t-':
				right = right - 1
			if right == left:
				right = left + max_line - 1
				self.print_line("%s %s-" % (indent, msg[left:right]))
			else:
				right = right + 1
				self.print_line("%s %s" % (indent, msg[left:right]))
			left = right
		self.print_line("%s %s" % (indent, msg[left:]))

	#def do_M_LOGIN(self,p):
	#	self.print_line("Logged in.")

	#def do_M_OPENMSG(self,p):
	#	self.indent_print("<"+p[1]+">", p[2])

	#def do_M_PERSONAL(self,p):
	#	self.indent_print("<*"+p[1]+"*>", p[2])

	#def do_M_STATUS(self,p):
	#	self.indent_print("[="+p[1]+"=]", p[2] )

	#def do_M_ERROR(self,p):
	#	self.indent_print("[*Error*]", p[1] )

	#def do_M_IMPORTANT(self,p):
	#	self.indent_print("[** "+p[1]+" **]", p[2] )

	#def do_M_EXIT(self,p):
	#	raise self.icbdQuitException

	def do_M_HELP(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	def do_M_BEEP(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	def do_M_BOOT(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	def do_M_CHANGE(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	def do_M_NAME(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	def do_M_NOBEEP(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	def do_M_PERSONAL(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	def do_M_PASS(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	def do_M_TOPIC(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	def do_M_WHO(self, p):
		self.print_line("Server supports following commands:")
		self.print_line("beep boot g m name nobeep pass topic w")

	##
	## command-output handler
	##
	C_GENERIC = 'co'
	C_END = 'ec'
	C_WHO_LIST = 'wl'
	C_WHO_GROUP = 'wg'
	C_WHO_HEAD = 'wh'
	C_GROUP_HEAD = 'gh'
	C_CLIENT_CMD_LIST = 'ch'
	C_CLIENT_LIST = 'c'

	def do_C_GENERIC(self,p):
		self.print_line(p[2])

	def do_C_END(self,p):
		self.print_line("** got C_END **")

	def do_C_WHO_LIST(self,p):
		t=time.localtime(string.atoi(p[6]))
		if p[2] != ' ':
			mod_char = '*'
		else:
			mod_char = ' '
		self.print_line(" %c %-12s  %6s  %5s  %s@%s %s" % (
			mod_char,
			p[3],
			self.pretty_time(string.atoi(p[4])),
			"%2d:%02d" % ( t[3], t[4] ),
			p[7],
			p[8],
			p[9] ))

	def do_C_WHO_GROUP(self,p):
		self.print_line(`p`) # XXX

	def do_C_WHO_HEAD(self,p):
		self.print_line('   Nickname        Idle Signon  Account')

	def do_C_GROUP_HEAD(self,p):
		pass

	def do_C_CLIENT_CMD_LIST(self,p):
		pass

	def do_C_CLIENT_LIST(self,p):
		pass

	def do_C_unknown(self,p):
		self.print_line("** unknown command output: " + `p`)

	def do_M_CMD_OUTPUT(self,p):
		cmd = p[1]
		if   cmd == self.C_GENERIC:
			self.do_C_GENERIC(p)
		elif cmd == self.C_END:
			self.do_C_END(p)
		elif cmd == self.C_WHO_LIST:
			self.do_C_WHO_LIST(p)
		elif cmd == self.C_WHO_GROUP:
			self.do_C_WHO_GROUP(p)
		elif cmd == self.C_WHO_HEAD:
			self.do_C_WHO_HEAD(p)
		elif cmd == self.C_GROUP_HEAD:
			self.do_C_GROUP_HEAD(p)
		elif cmd == self.C_CLIENT_CMD_LIST:
			self.do_C_CLIENT_CMD_LIST(p)
		elif cmd == self.C_CLIENT_LIST:
			self.do_C_CLIENT_LIST(p)
		else:
			self.do_C_unknown(p)

	def do_M_PROTO(self,p):
		if len(p) > 3:
			server_id = p[3]
		else:
			server_id = "(unknown)"
		if len(p) > 2:
			host_id = p[2]
		else:
			host_id = self.server_name
		self.print_line("connected to the %s icbd server (%s)" % \
			( host_id , server_id ))

	def do_M_BEEP(self,p):
		if self.beeps_ok:
			if self.alert_mode == 0:
				self.output_file.write('\007')
			self.show([self.M_STATUS,"Beep", \
				"%s has annoyingly beeped you." % \
				( p[1] )])

	def do_M_PING(self,p):
		print "ping"
		pass

	def do_M_PONG(self,p):
		print "pong"
		pass

	def do_M_unknown(self,p):
		self.print_line("unknown packet:" + `p`)

	def recv(self):
		self.last_packet = icbdConn.recv(self)
		return self.last_packet

	def show(self,p = None):
		if p == None:
			p = self.last_packet
		c = p[0]

		if   c == self.M_HELP:
			self.do_M_HELP(p)
		elif c == self.M_BEEP:
			self.do_M_BEEP(p)
		elif c == self.M_BOOT:
			self.do_M_BOOT(p)
		elif c == self.M_CHANGE:
			self.do_M_CHANGE(p)
		elif c == self.M_NAME:
			self.do_M_NAME(p)
		elif c == self.M_NOBEEP:
			self.do_M_NOBEEP(p)
		elif c == self.M_PERSONAL:
			self.do_M_PERSONAL(p)
		elif c == self.M_CMD_PASS:
			self.do_M_CMD_PASS(p)
		elif c == self.M_TOPIC:
			self.do_M_TOPIC(p)
		else: #if c == self.M_WHO:
			self.do_M_WHO(p)

	def select(self):
		user_ready = 0
		server_ready = 0
		server_error = 0
		iobjs = []
		oobjs = []
		eobjs = []
		print("--select--")
		try:
			iobjs, oobjs, eobjs = select.select (
				[self.input_file, self],
				[],
				[self])
		except select.error:
			pass
		print("--if--")
		if self.input_file in iobjs:
			user_ready = 1
		if self in iobjs:
			server_ready = 1
		if self in eobjs:
			server_error = 1
		return user_ready, server_ready

	def user_recv(self):
		self.userline = self.input_file.readline()
		if self.userline != None and self.userline[-1] == '\n':
			self.userline = self.userline[:-1]
		if len(self.userline) > self.MAX_LINE:
			self.indent_print("[ Error ]", \
				"input line too long, truncating...")
			self.userline = self.userline [:MAX_LINE]

	def process_cmd(self, cmd, line):
		if cmd == 'q':
			raise self.icbdQuitException
		elif cmd == 'alert':
			if self.alert_mode == 0:
				self.alert_mode = 1
				self.show([self.M_STATUS, "Status", \
					"alert mode enabled (beep)."])
			else:
				self.show([self.M_STATUS, "Status", \
					"d00d: alert mode already enabled."])
		elif cmd == 'noalert':
			if self.alert_mode == 1:
				self.alert_mode = 0
				self.show([self.M_STATUS, "Status", \
					"alert mode disabled (shhhh)."])
			else:
				self.show([self.M_STATUS, "Status", \
					"d00d: alert mode already disabled."])
		elif cmd == 'beep':
			if line != "":
				self.command(cmd, line)
			elif self.beeps_ok == 1:
				self.show([self.M_STATUS, "Status", \
					"beeps already allowed."])
			else:
				self.beeps_ok = 1
				self.show([self.M_STATUS, "Status", \
					"folks can now annoyingly beep you."])
		elif cmd == 'nobeep':
			if self.beeps_ok == 0:
				self.show([self.M_STATUS, "Status", \
					"beeps already disabled."])
			else:
				self.beeps_ok = 0
				self.show([self.M_STATUS, "Status", \
					"folks can no longer annoyingly beep you."])
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
		while cmd_split < len(command_line) and \
		  command_line[cmd_split] not in ' \t':
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


no_termios = 0
try:
	import termios
except:
	no_termios = 1

## as of python 2.1.1, module "TERMIOS" is deprecated, and its
## functionality (symbols) is part of "termios".
if not no_termios:
	if hasattr(termios,'ICANON'):
		TERMIOS=termios
	else:
		import TERMIOS


def repondre(p):
	c = p[0]
	if c == M_LOGIN:
		#do_M_LOGIN(p)
		print "login"
	elif c == M_OPENMSG:
		print "message ouvert"
		#do_M_OPENMSG(p)
	elif c == M_PERSONAL:
		print "message perso"
		#do_M_PERSONAL(p)
	"""elif c == self.M_STATUS:
		#do_M_STATUS(p)
	elif c == self.M_ERROR:
		#do_M_ERROR(p)
	elif c == self.M_IMPORTANT:
		#do_M_IMPORTANT(p)
	elif c == self.M_EXIT:
		#do_M_EXIT(p)
	elif c == self.M_CMD_OUTPUT:
		#do_M_CMD_OUTPUT(p)
	elif c == self.M_PROTO:
		#do_M_PROTO(p)
	elif c == self.M_BEEP:
		#do_M_BEEP(p)
	elif c == self.M_PING:
		#do_M_PING(p)
	elif c == self.M_PONG:
		#do_M_PONG(p)
	else:
		#do_M_unknown(p)
"""

def parsemsg(msg):
	cmd_split = 0
	while cmd_split < len(msg) and msg[cmd_split] not in ' \t':
		cmd_split = cmd_split + 1
	cmd = string.lower(msg[:cmd_split])
	if cmd_split < len(msg):
		cmd_split = cmd_split + 1
	print cmd+"  "+msg[cmd_split:]
	repondre([cmd,msg[cmd_split:]])

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


import signal
class icbdTerminalApp(icbdSimple):
	old_termios = None
	last_m_personal = 0
	default_display_buffer = 200

	def on_stop(self, sig, stack):
		self.restore_termios()
		signal.signal(signal.SIGTSTP, signal.SIG_DFL)
		os.kill(os.getpid(), signal.SIGTSTP)
		signal.signal(signal.SIGTSTP, self.on_stop)
		self.set_cbreak()

	def set_cbreak(self):
		if no_termios:
			return
		self.old_termios = termios.tcgetattr(self.input_file.fileno())
		new_termios = termios.tcgetattr(self.input_file.fileno())
		new_termios[3] = new_termios[3] & ~TERMIOS.ICANON
		new_termios[3] = new_termios[3] & ~TERMIOS.ECHO
		new_termios[6][TERMIOS.VMIN] = 1
		new_termios[6][TERMIOS.VTIME] = 0
		termios.tcsetattr(self.input_file.fileno(), TERMIOS.TCSANOW, \
			new_termios)
		new_termios = termios.tcgetattr(self.input_file.fileno())

	def restore_termios(self):
		if no_termios:
			return
		if self.old_termios != None:
			termios.tcsetattr(self.input_file.fileno(), \
			TERMIOS.TCSANOW, self.old_termios)

	def do_display_cmd(self, cmd, line):
		try:
			s = string.split ( line )
			if len ( s ) > 0:
				show_lines = string.atoi ( s[0] )
			else:
				show_lines = self.display_buffer_length
		except ValueError:
			self.show([self.M_ERROR, "Number of lines must be numeric."])
			return
		for i in self.display_buffer[-show_lines:]:
			self.print_line(i,remember=0)

	def process_cmd(self, cmd, line):
		if cmd == 'display':
			self.do_display_cmd(cmd, line)
		elif cmd == 'page':
			if not self.page_mode:
				self.show([self.M_STATUS, "Status", \
					"Page mode enabled."])
			else:
				self.show([self.M_STATUS, "Status", \
					"d00d: Page mode already enabled."])
			self.page_mode = 1
		elif cmd == 'nopage':
			if self.page_mode:
				self.show([self.M_STATUS, "Status", \
					"Page mode enabled."])
			else:
				self.show([self.M_STATUS, "Status", \
					"d00d: Page mode already enabled."])
			self.page_mode = 0
		elif cmd == 'm':
			self._remember_line ( '/m %s' % ( line, ))
			icbdSimple.process_cmd(self, cmd, line)
		else:
			icbdSimple.process_cmd(self, cmd, line)

	def openmsg(self, msg):
		self._remember_line('--> ' + msg)
		icbdSimple.openmsg(self,msg)

	def _remember_line(self,line):
		self.display_buffer.append(line)
		self.display_buffer = self.display_buffer[-self.display_buffer_length:]

	def print_line(self,line,remember=1):
		if remember:
			self._remember_line(line)
		self.num_lines = self.num_lines + 1
		if self.page_mode and ( self.num_lines >= self.term_height - 1 ):
			self.output_file.write ( '\r-- more --' )
			self.output_file.flush()
			self.input_file.read(1)
			self.num_lines = 0
			self.output_file.write ( '\r           \r' )
			self.output_file.flush()
		icbdSimple.print_line(self,line)

	def _backspace(self, n):
		while n > 0:
			self.output_file.write("\b \b")
			n = n - 1

	##
	## process_char returns two-tuple (r, line)
	##   r:
	##     0 - process next character
	##     1 - line done, return
	##   line:
	##     line after this character has been processed
	##
	def process_char(self,c,line):
		if   c == '\n' or c == '\r':
			self.output_file.write('\n')
			self.output_file.flush()
			return (1, line)
		elif c == '\022': # redraw line
			self.output_file.write('\r' + line)
			self.output_file.flush()
		elif c == '\025' or ( no_termios == 0 and \
		     c == self.old_termios[6][TERMIOS.VKILL]): # kill-line
			self._backspace(len(line))
			self.output_file.flush()
			line = ""
			return (1, line)
		elif c == '\010' or c == '\177' or ( no_termios == 0 and \
		     c == self.old_termios[6][TERMIOS.VERASE]): # backspace/erase
			if len(line) > 0:
				line = line[:-1]
				self._backspace(1)
				self.output_file.flush()
			if len(line) == 0:
				return (1, line)
		elif c == '\027' or ( no_termios == 0 and
		     c == self.old_termios[6][TERMIOS.VWERASE]): # word-erase
			oldlen = len(line)
			while line != "" and line[-1] in " \t":
				line = line[:-1]
			while line != "" and line[-1] not in " \t":
				line = line[:-1]
			if oldlen > 0:
				self._backspace(oldlen - len(line))
				self.output_file.flush()
		elif ord(c) >= 0x20 and ord(c) < 0x7f: # YUK, there should be a string.printable
			if len(line) > self.MAX_LINE:
				self.output_file.write('\007')
				self.output_file.flush()
			else:
				line = line + c
				self.output_file.write(c)
				self.output_file.flush()
				self.do_history = 0
		elif self.do_history and c == '\t': # tab, cycle through m_personal_history
			if self.m_personal_history != []:
				if line != "":
					self._backspace(len(line))
				line = "/m " + self.m_personal_history[self.last_m_personal] + " "
				self.output_file.write(line)
				self.output_file.flush()
				self.last_m_personal = self.last_m_personal - 1
				if self.last_m_personal < 0:
					self.last_m_personal = len(self.m_personal_history) - 1
		else:
			## unknown character, ignore
			pass
		if line == "":
			return (1, line)
		else:
			return (0, line)

	def readline(self,file):
		self.num_lines = 0
		line = ""
		self.last_m_personal = len(self.m_personal_history) - 1
		self.do_history = 1
		while 1:
			try:
				c = file.read(1)
				done, line = self.process_char(c,line)
				if done:
					break
			except IOError:
				pass
		if line == "":
			return None
		else:
			return line

	def user_recv(self):
		self.userline = self.readline(self.input_file)
		if self.userline != None and self.userline[-1] == '\n':
			self.userline = self.userline[:-1]

	def ad_connect(self, s, sc, addr, clients_connectes):
		print("--ad_connect--")
		print("--nouvelle connexion--")


		print("--j--")
		#c.send("01\x01a\x01j1\x01\x00")
		msg2="\x0F"+self.M_PROTO+"1\x01daicbd\x01icbd\x00"
		buf=msg2.encode('utf-8')
		sc.send(buf)
		print ("--buffer ", buf)
		print addr
		clients_connectes.append((sc,addr))
		data = sc.recv(1024)
		msg = data.decode('utf-8')
		print ("--message ", msg)


		print("--a--")
		msg2="\x02"+self.M_LOGIN+"\x00"
		buf=msg2.encode('utf-8')
		sc.send(buf)
		print ("--buffer ", buf)


		print("--d--")
		msg3="\x23"+self.M_STATUS+"Status\x01You are now in group Agora\x00"
		buf=msg3.encode('utf-8')
		sc.send(buf)
		print ("--buffer ", buf)


		th=Threadserveur(sc)
		th.start()
		idthread=th.getName()
		print "idthread"+idthread


	def mainloop(self):
		print("--mainloop2--")
		#self.set_cbreak()
		saveChat("adad", "bonjour")
		lesgroupes=dict()
		lesgroupes["agora"]=[]
		clients_connectes = []
		s = socket(AF_INET,SOCK_STREAM)
		s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		s.bind(('0.0.0.0', 7326))
		s.listen(4)
		socks=[]


		while 1:
			print("--while--")
			sc, addr = s.accept()

			#cherche si la socket existe. Sinon, lance la connexion
			if sc in socks:
				print("--contiens--")
			else:
				self.ad_connect(s, sc, addr, clients_connectes)
				socks.append(sc)




	def __init__(self):
		import getopt

		nick = None
		logid = None
		group = None
		command = 'login'
		server = None

		self.display_buffer_length = self.default_display_buffer
		self.display_buffer = []

		self.page_mode = 0
		self.num_lines = 0

		try:
			self.term_width=string.atoi(os.environ['COLUMNS'])
			self.term_height=string.atoi(os.environ['LINES'])
		except:
			pass

		# process args
		try:
			print("--getopt--")
			optlist, args = getopt.getopt(sys.argv[1:],'4:C:d:G:L:n:S:v')
		except getopt.error, detail:
			self.print_line('error: %s' % (`detail`))
			self.print_line('usage: %s [-46Cdv] [-G group1[,group2,...]] [-L prefix] [-M modtab]\n\t[-S name] [[addr][:port] ...]' % (sys.argv[0]))
			return
		for i in optlist:
			if i[0] == '-G':
				group = i[1]
			elif i[0] == '-L': 	#elif i[0] == '-n': #nick = i[1]
				logid = i[1] #elif i[0] == '-w': #command = 'w'
			elif i[0] == '-S':
				server = i[1]
			else:
				print("else", i[0])

		self.print_line("welcome to python icbd.")
		#icbdSimple.__init__(self,group,logid,server)
		icbdSimple.__init__(self,"agora","Evolve","10.0.0.1")
		#try:
		#	self.connect()
		#except socket.error, detail:
		#	self.print_line("can't connect to client: %s" % (detail))
		#	return
			#c.close()
			#(g, quic) = s.accept()
			#c.send("coucou")
			#s.close()

		#self.login(command)
		#self.socket = socket.socket ( socket.AF_INET , \
		#	socket.SOCK_STREAM )
		#self.socket.connect (( '10.0.0.0' , 7326 ))
		print("--mainloop_init--")
		self.mainloop()

class icbdPersonalized(icbdTerminalApp):
	pass

##
## if we are standalone, not library, then implement
## default ui
##

if __name__ == "__main__":
	print("--debut--")
	customfile = os.environ['HOME'] + '/.icbdrc'
	try:
		execfile(customfile)
	except IOError:
		pass
	session = icbdPersonalized()
