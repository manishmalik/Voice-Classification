class listenClients:

	def __init__(self,app):
		self.app = app

	def getFiles(self):
		mssg = self.app.ser_socket.recv(512)
		if '%%eofn%%' in mssg:
			self.getFile(mssg)
	def getFile(self,mssg):
		mssg = mssg.split("%%eofn%%")
		file_name = mssg[0]
		data1 = mssg[1]
		tkMessageBox.showinfo("Client is sending a File...",'Client sending file %s'%file_name)
		f = open(file_name,'w')
		count = 0
		while 1:
			data = self.app.ser_socket.recv(512)
			print data
			if count == 0:
				data = data+data1
			if '%%eofoc%%' in data:
				f.write(data.split('%%eofoc%%')[0])
				print 'done'
				f.close()
				break
			f.write(data)
			count = count+1
