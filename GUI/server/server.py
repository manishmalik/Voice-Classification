#!/usr/bin/python
import socket
ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	port = int(raw_input("Enter port number to listen: "))
except:
	print "Invalid port..."
	exit()
print "Server listening at port %d..."%port
ser_socket.bind(('',port))
ser_socket.listen(5)
while 1:
	con,client = ser_socket.accept()
	file_name = con.recv(512).split("%%eofn%%")
	fil = file_name[0]
	data1 = file_name[1]
	f = open(fil,'w')
	count = 0
	while 1:
		data = con.recv(512)
		if not data:
			f.close()
			break
		else:
			if count == 0:
				data = data1+data
			f.write(data)
			count = count+1
	print "Recivied file %s from remote client... saved!"%fil
	con.close()
