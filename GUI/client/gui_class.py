from Tkinter import *
import tkMessageBox,socket,tkFileDialog
class makeGui:
	def __init__(self):
		self.connected=0
		self.frame = Tk()
		self.frame.title("Connect to remote server...")
		self.w = Label(self.frame,text="Enter IP and Port number to connect!")
		self.w.pack(pady=20)
		self.ipframe = Frame(self.frame)
		self.ipLabel = Label(self.ipframe,text="IP Address/Host:").pack(sid=LEFT)
		self.ipAdd = Entry(self.ipframe,width=20)
		self.ipAdd.pack(side=LEFT)
		self.ipframe.pack(padx=30,pady=20)
		self.pframe = Frame(self.frame)
		self.pLabel = Label(self.pframe,text="Port Address: ").pack(side=LEFT)
		self.portAdd = Entry(self.pframe,width=20)
		self.portAdd.pack(side=LEFT)
		self.pframe.pack(padx=30,pady=10)
		self.btnSubmit = Button(self.frame,text="Connect",command=self.connect)
		self.btnSubmit.pack(side=BOTTOM,pady=30)
		self.frame.bind('<Return>',self.bindEnter)
		self.frame.mainloop()

	def findFileWindow(self):
		self.frame.title("Choose file to send...")
		self.w.destroy()
		self.ipframe.destroy()
		self.pframe.destroy()
		self.btnSubmit.destroy()

		self.frame.bind('<Return>',self.fileBox)
		self.fileFrame = Frame(self.frame,width=300,height=200)
		self.w = Label(self.fileFrame,text="Find file(s) to send:")
		self.w.pack(pady=20)
		self.btnFindFiles = Button(self.fileFrame,text="Find Files",command=self.fileBox)
		self.btnFindFiles.pack(side = BOTTOM, pady=30)
		self.fileFrame.pack()


	def fileBox(self,event=None):
		self.btnFindFiles.config(state = DISABLED)
		files = tkFileDialog.askopenfilename(parent = self.frame,filetypes = [('All Format','*')],multiple=1)
		tkMessageBox.showinfo("Sending files","Sending Files to remote Server...")
		for fil in files:
			try:
				f = open(fil,'rb')
				fil = fil.split('/')[-1]
				self.cl_socket.send(fil+"%%eofn%%")
				print "Sending file...%s"%fil,
				while 1:
					data = f.readline()
					if not data:
						break
					self.cl_socket.send(data)
				print " Done!"
			except Exception,e:
				print e
		self.btnFindFiles.config(state = ACTIVE)

	def bindEnter(self, event ):
		self.connect()


	def connect(self):
		ipAdd = self.ipAdd.get()
		portAdd = self.portAdd.get()
		if len(ipAdd)==0:
			tkMessageBox.showerror("Invalid IP/Host","Please provide a valid host")
			return None
		if not portAdd.isdigit():
			tkMessageBox.showerror("Invalid Port","Port Address seems Invalid.")
			return None
		if len(portAdd)!=4:
			tkMessageBox.showerror("Invalid Port","Port Address must be of 4 digit.")
			return None
		else:
			self.cl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				self.cl_socket.connect((ipAdd,int(portAdd)))				
				tkMessageBox.showinfo("Connected","Successfully connected!")
				self.connected = 1
				self.frame.destroy()
			except Exception,e:
				tkMessageBox.showerror("Failed to connect...",e)				
