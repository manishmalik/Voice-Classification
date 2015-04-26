from Tkinter import *
import tkMessageBox,socket,tkFileDialog,os
class makeGui:
	def __init__(self):
		self.started=0
		self.frame = Tk()
		self.frame.title("Enter Port number to start...")
		self.w = Label(self.frame,text="Enter Port number to start:")
		self.w.pack(pady=20)
		self.pframe = Frame(self.frame)
		self.pLabel = Label(self.pframe,text="Port Address: ").pack(side=LEFT)
		self.portAdd = Entry(self.pframe,width=20)
		self.portAdd.pack(side=LEFT)
		self.pframe.pack(padx=30,pady=10)
		self.btnSubmit = Button(self.frame,text="Connect",command=self.connect)
		self.btnSubmit.pack(side=BOTTOM,pady=30)
		self.frame.bind('<Return>',self.bindEnter)
		self.frame.mainloop()

	def end(self,event):
		self.frame.destroy()
		exit(1)

	def connect(self):
		portAdd = self.portAdd.get()
		if not portAdd.isdigit():
			tkMessageBox.showerror("Invalid Port","Port Address seems Invalid.")
			return None
		if len(portAdd)!=4:
			tkMessageBox.showerror("Invalid Port","Port Address must be of 4 digit.")
			return None
		else:
			self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				self.ser_socket.bind(('',int(portAdd)))
				self.ser_socket.listen(10)
				tkMessageBox.showinfo("Server Started","Server listengning at Port %d"%int(portAdd))
				self.started = 1
				self.frame.destroy()
			except Exception,e:
				print e
				tkMessageBox.showerror("Failed to Start","Server failed to start. %s"%e)
				return 0

	def bindEnter(self,event):
		if self.started == 0:
			self.connect()
		else:
			pass
