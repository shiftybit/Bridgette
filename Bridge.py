#!/usr/bin/env python3
import time
import json
import string,random #for the uid generator stopgap
from twisted.words.protocols.irc import IRC
from twisted.internet import task , protocol, reactor
from twisted.internet.protocol import ClientFactory
# ----   Configuration   ---- # 
ServerName = "rummy.top.com"
ServerPort = 9090
ServerHost = "localhost"
ServerPassword = "RainbowTables"
ServerSID = "0FE"
APIListenerPort = 8000
ServerChannel = "#top"
ServerCloak = "DiscordRelay"

	def __init__(self, factory):
		self.factory = factory
	def connectionMade(self):
		self.sendLine("PASS {}".format(ServerPassword))
		self.sendLine("PROTOCTL NICKv2 VHP NICKIP UMODE2 SJOIN SJOIN2 SJ3 NOQUIT TKLEXT ESVID MLOCK")
		self.sendLine("PROTOCTL EAUTH={}".format(ServerName))
		self.sendLine("PROTOCTL SID={}".format(ServerSID))
		self.sendLine("SERVER {} 1 :Bridge Serv".format(ServerName))
		self.sendLine(":{} EOS".format(ServerSID))
		self.sendLine("PING :{}".format(ServerSID))

	def Message(self,message,user,channel=ServerChannel):
		print("Message subroutine")
		self.sendLine(":{} PRIVMSG {} :{}".format(user,channel, message))
	def joinUser(self, user):
		"""Joins a user to a channel."""
		line = ":{} JOIN {}".format(user, ServerChannel)
		print("Join User. CMD]] {}".format(line))
		self.sendLine(line)
	def registerUser(self, user):
		current_time = int(time.time())
		real_name = "discordUser"
		hostname = "bbox1.net"
		username = "discordUserUN"
		#Example UID/Join ['darkscrypt`', '0', '1514778126', 'darkscrypt', '172.56.1.105', '002BH6A1G', '0', '+iwx', '64F3883C.55E961CE.B5D49925.IP', '64F3883C.55E961CE.B5D49925.IP', 'rDgBaQ==', 'realname']

		uid = "001G1{}{}{}".format(random.choice(string.ascii_letters),random.choice(string.ascii_letters),random.choice(string.ascii_letters))
		brd_id = "".join(random.choice(string.ascii_letters) for i in range(12))
		print("Generating Random UID{}".format(uid))
		registerString = ":{0} UID {1} 0 {2} {3} {4} {5}{6} 0 +ixw {7} * :{8}".format(ServerSID, user, current_time, username, hostname, brd_id, uid, ServerCloak, real_name)
		print("Register: {}".format(registerString))
		self.sendLine(registerString)
		self.joinUser(user)
	def irc_PING(self, prefix, params):
		response = params[0]
		self.sendLine("PONG {}".format(response))
	def irc_UID(self, prefix, params):
		print("irc_UID -params")
		print(params)
		print("irc_UID -prefix")
		print(prefix)
	def irc_unknown(self, prefix, command, params):
		#print("\033[31m{} \033[33m{} \033[34m{}\033[0m".format(prefix, command, params))
		pass
class ServicesFactory(ClientFactory):
	def __init__(self):
		self.protocols = []
		self.IRCConnection = None
		print("init run")
	def buildProtocol(self, addr): 
		protocol = IRCProtocol(self)
		if len(self.protocols) > 1:
			raise "can only init once"
		self.protocols.append(protocol)
		self.IRCConnection = protocol
		return protocol	

class Echo(protocol.Protocol):
	def dataReceived(self, data):
		print(data)
		data=str(data.decode("utf-8").rstrip())
		self.dispatch(data)
	def dispatch(self,data):
		irc = IRCFactory.IRCConnection
		try:
			object = json.loads(data)
		except json.decoder.JSONDecodeError:
			print("Error Decoding Json Data")
			return
		if(object["action"] == "register"):
			irc.registerUser(object["user"])
		if(object["action"] == "join"):
			print("Join")
		if(object["action"] == "msg"):
			irc.Message(user = object["user"], message = object["message"])
			print("msg")
class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Echo()

		

global IRCFactory
global APIFactory
IRCFactory = ServicesFactory()
APIFactory = EchoFactory()
reactor.listenTCP(APIListenerPort, APIFactory)
reactor.connectTCP(ServerHost, ServerPort, IRCFactory)
reactor.run()
