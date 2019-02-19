import tkinter as tk
from twisted.internet import protocol, reactor, tksupport
import string,random 
import json
port=6161
host="Api Listener FQDN/IP here"

def destroy(event=None):
	reactor.stop()
	print("connection terminated")
	#root.destroy()


class EchoClient(protocol.Protocol):
	def connectionMade(self):
		print("connectionTest")
		#randomString= "".join(random.choice(string.ascii_letters) for i in range(12))
		#self.transport.write(randomString.encode('ascii'))
	def dataReceived(self,data):
		print("Server Said:\t{}".format(data))
		#self.transport.loseConnection()

class EchoFactory(protocol.ClientFactory):
	def buildProtocol(self, addr):
		global MyEC
		MyEC = EchoClient()
		return MyEC
		
def SendLine(data):
	data = data.encode("ascii")
	textbox.delete("%d.%d" % (0,0), tk.END)
	textbox.insert(tk.INSERT, data)
	MyEC.transport.write(data)
	
def SendMessage(user,message):
	d = {}
	d["action"] = "msg"
	d["user"] = user
	d["message"] = message
	j = json.dumps(d)
	SendLine(j)
	
def RegisterUser(user):
	d = {}
	d["action"] = "register"
	d["user"] = user
	j = json.dumps(d)
	SendLine(j)
	
def RegisterUser_click():
	print("Register User Clicked")
	#randomString= "".join(random.choice(string.ascii_letters) for i in range(12))
	username = entry_username.get()
	RegisterUser(username)
	
def SendMessage_click():
	message  = entry_message.get()
	user = entry_username.get()
	SendMessage(user,message)

def JoinChannel_click():
	print("Join Channel Clicked")
	d={}
	d["action"] = "join"
	
	pass
	
def StartReactor():
	reactor.connectTCP(host,port,EchoFactory())
	reactor.run()

def ClickTest():
	textbox.delete("%d.%d" % (0,0), tk.END)
	textbox.insert(tk.INSERT, "my thing")
	
MyEC = None	
root = tk.Tk()
root.geometry("600x400")
textbox = tk.Text(root, height=7, width=45)
textbox['bg'] = "#000000"
textbox['fg']= "#00ff00"
textbox["pady"]= 15
textbox.grid(row=8,sticky=tk.W, columnspan=2, rowspan=3, pady=50, padx=10)
tksupport.install(root)
tk.Label(root, text="Username").grid(row=2,column=0)
entry_username = tk.Entry(root)
entry_username.grid(row=2, column=1)

tk.Label(root, text="Message").grid(row=3,column=0)
entry_message = tk.Entry(root)
entry_message.grid(row=3, column=1)
button = tk.Button(root, text="Register User", command=RegisterUser_click)
button.grid(row=4)
button = tk.Button(root, text="Join Channel", command=JoinChannel_click)
button.grid(row=5)
button = tk.Button(root, text="Send Message", command=SendMessage_click)
button.grid(row=6)
tk.Button(root, text="clicky", command=ClickTest).grid(row=7)

root.after(3000,StartReactor)
#root.protocol("WM_DELETE_WINDOW", destroy)
root.bind("<Destroy>", destroy)
root.mainloop()