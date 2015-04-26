from Tkinter import *
import tkMessageBox,socket,tkFileDialog

class MakeClientGui:
	def __init__(self,app):
		self.app = app
		self.frame = Tk()
		self.frame.title("Welcome to Client file transfer control.")
		self.sendFileBtn = Button(self.frame,text="Send File to server",command=self.sendFile)
		self.sendFileBtn.pack(pady=20,padx=40)
		self.closeConnBtn = Button(self.frame,text="Disconnect",command=self.disconnect)
		self.closeConnBtn.pack(pady=20)
		self.frame.mainloop()

	def sendFile(self):
		self.sendFileBtn.config(state = DISABLED)
		files = tkFileDialog.askopenfilename(parent = self.frame,filetypes = [('All Format','*')],multiple=1)
		tkMessageBox.showinfo("Sending files","Sending Files to all Server...")
		for fil in files:
			try:
				f = open(fil,'rb')
				fil = fil.split('/')[-1]
				con=self.app.cl_socket
				con.send(fil+"%%eofn%%")
				print "Sending file...%s"%fil,
				while 1:
					data = f.readline()
					if not data:
						con.send('%%eofoc%%')
						break
					con.send(data)
			except Exception,e:
				print e
		self.sendFileBtn.config(state = ACTIVE)

	def disconnect(self):
		self.app.cl_socket.send('%%eocon%%')
		self.frame.destroy()
