from gui_class import makeGui
from listenServer import MakeClientGui
import threading,tkMessageBox
from Crypto.Cipher import AES

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
			self.listenForMessages()
		elif self.no == 1:
			MakeClientGui(self.app)

	def listenForMessages(self):
		while 1:
			mssg = self.app.cl_socket.recv(512)
			if '%%mssg%%' in mssg:
				mssg = mssg.split('%%mssg%%')[1]
				# mssg='Gender Predicted by the Server is : '+mssg
				tkMessageBox.showinfo("Prediction from Server ...",mssg)
			elif '%%eofn%%' in mssg:
				self.listenForFiles(mssg)

	def listenForFiles(self,mssg):
		#con = self.app.cl_socket
		mssg = mssg.split("%%eofn%%")
		#print mssg
		file_name = mssg[0]
		if '%%eofoc%%' in file_name:
			file_name = file_name.split('%%eofoc%%')[1]
		data1 = mssg[1]
		tkMessageBox.showinfo("Server is sending a File...","Server seding file %s."%file_name)
		f = open(file_name,'w')
		count = 0
		while 1:
			data = self.app.cl_socket.recv(512)
			#print data
			if count == 0:
				data = data+data1
			if '%%eofoc%%' in data and '%%eofn%%' in data:
				data = data.split('%%eofoc%%')[0]
				if encValue == 1:
					data = self.decrypt(data)
				f.write(data)
				#print 'done'
				f.close()
				self.listenForFiles(data.split('%%eofoc%%')[1])
			if '%%eofoc%%' in data:
				data = data.split('%%eofoc%%')[0]
				if encValue == 1:
					data = self.decrypt(data)
				f.write(data)
				#print 'done'
				f.close()
				break
			if encValue == 1:
				data = self.decrypt(data)
			f.write(data)
			count = count+1

app = makeGui()
encValue = 0
if app.connected == 1:
	for i in range(2):
		ClientThread(app,i).start()
