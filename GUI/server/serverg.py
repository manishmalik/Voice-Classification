from gui_class import makeGui
import threading,socket,tkMessageBox,tkFileDialog,os
from Tkinter import *
from pitch_anal import audio_analysis
connections = list()
connIps =list()
password = open("password","r").read()

class ClientThread(threading.Thread):
	def __init__(self,app,no):
		self.app = app
		self.no = no
		threading.Thread.__init__(self)

	def encrypt(self,string):
		aes = AES.new(password, AES.MODE_ECB)
		return aes.encrypt(string)

	def decrypt(self,string):
		aes = AES.new(password, AES.MODE_ECB)
		return aes.decrypt(string)

	def run(self):
		if self.no == 0:
			self.listenForClients()
		elif self.no == 1:
			while 1:
				for con in connections:
					mssg = con.recv(512)
					if '%%eofn%%' in mssg:
						self.saveFile(mssg,con)
					elif '%%eocon%%' in mssg:
						self.updateClients(con)
		else:			
			self.frame = Tk()
			self.frame.title("Welcome to server file transfer control.")
			self.list = Frame(self.frame)
			Label(self.list,text="Connected Clients...").pack(padx=40,pady=20)
			self.connList = Listbox(self.list,selectmode=MULTIPLE)
			self.fillList()
			self.connList.pack(padx=40,pady=20)
			self.refBtn = Button(self.list,text="Refresh",command=self.fillList)
			self.refBtn.pack(side=RIGHT,pady=20)
			self.list.grid(row=0,column=0)
			# self.options = Frame(self.frame)
			# Label(self.options,text="Message:").pack(pady=5)
			# self.msgText = Entry(self.options,width=20)
			# self.msgText.pack(pady=5,padx=10)
			# self.sendMsgBtn = Button(self.options,text="BroadCast Message",command=self.broadcast)
			# self.sendMsgBtn.pack(pady=10)
			# self.sendFileBtn = Button(self.options,text="Send File",command = self.sendFile)
			# self.sendFileBtn.pack(pady=10)
			# self.sendPdfsBtn = Button(self.options,text="Send All PDFs",command=self.sendPdfs)
			# self.sendPdfsBtn.pack(pady=10)
			# self.sendDocsBtn = Button(self.options,text="Send All Doc Files",command=self.sendDocs)
			# self.sendDocsBtn.pack(pady=10)
			# self.encValue = IntVar()
			# self.encBtn = Checkbutton(self.options,text="Encrypt File(s).",variable=self.encValue)
			# self.encBtn.pack(pady=10)
			# self.options.grid(row=0,column=1)
			self.frame.mainloop()

	def sendPdfs(self):
		files = os.listdir('.')
		pdfs = list()
		for f in files:
			fext = f.split('.')[-1]
			if fext == 'pdf':
				pdfs.append(f)
		tkMessageBox.showinfo("Sending all PDF files","Sending all PDF files. %d Found..."%len(pdfs))
		self.sendAllFiles(pdfs)

	def sendDocs(self):
		files = os.listdir('.')
		docs = list()
		for f in files:
			fext = f.split('.')[-1]
			if fext == 'doc' or fext == 'docx':
				docs.append(f)
		tkMessageBox.showinfo("Sending all Doc files","Sending all PDF files. %d Found..."%len(docs))
		self.sendAllFiles(docs)

	def updateClients(self,con):
		ip = connIps.pop(connections.index(con))
		connections.pop(connections.index(con))
		tkMessageBox.showinfo("Client Disconnected..","Connection closed by Client %s."%ip)

	def saveFile(self,mssg,con):
		mssg = mssg.split("%%eofn%%")
		file_name = mssg[0]
		data1 = mssg[1]
		tkMessageBox.showinfo("Client is sending a File...",'Client sending file %s'%file_name)
		f = open(file_name,'wb')
		count = 0
		while 1:
			data = con.recv(2048)
			if count == 0:
				data = data+data1
			if '%%eofoc%%' in data:
				f.write(data.split('%%eofoc%%')[0])				
				f.close()
				break
			f.write(data)
			count = count+1
		f.close()
		gender=audio_analysis(file_name)
		print gender
		tkMessageBox.showinfo("Speaker Gender","Gender of the Speaker Must be : %s"%gender)
		# Responding to the client
		for con in connections:
			try:
				con.sendall('%%mssg%%'+gender)
			except:
				pass


	def fillList(self):
		self.connList.delete(0,self.connList.size())
		for ip in connIps:
			self.connList.insert(END,ip)

	def broadcast(self):
		for con in connections:
			try:
				con.sendall('%%mssg%%'+self.msgText.get())
			except:
				pass

	def sendFile(self):
		self.sendFileBtn.config(state = DISABLED)
		files = tkFileDialog.askopenfilename(parent = self.frame,filetypes = [('All Format','*')],multiple=1)
		tkMessageBox.showinfo("Sending files","Sending Files to all Clients...")
		#print connections
		self.sendAllFiles(files)
		self.sendFileBtn.config(state = ACTIVE)

	def sendAllFiles(self,files):
		for fil in files:
			try:
				f = open(fil,'r')
				fil = fil.split('/')[-1]
				for con in connections:
					con.send(fil+"%%eofn%%")	#eof name
				while 1:
					data = f.readline()
					if not data:
						con.send('%%eofoc%%')	#eof occured
						break
					for con in connections:
						if self.encValue == 1:
							data = self.encrypt(data)
						con.send(data)
			except Exception,e:
				print e

	def listenForClients(self):
		while 1:
			con,client = self.app.ser_socket.accept()
			connections.append(con)
			connIps.append(client[0])
			tkMessageBox.showinfo('Recieived Cient','Recieved Conection from %s'%client[0])			

app = makeGui()

if app.started == 1:
	for i in range(3):
		ClientThread(app,i).start()
