try:
	from Tkinter import *
except:
	from tkinter import *

def printhello(ip):
	print "Hello ",ip

root = Tk()
root.title('Connect to remote server...')
w = Label(root,text="Enter IP and Port number to start server.").pack(pady = 20, padx = 30)
ipframe = Frame(root)
Label(ipframe,text="IP Address: ").pack(side=LEFT)
ip = Entry(ipframe,width=20).pack(side=LEFT)
ipframe.pack(padx=30,pady=20)
pframe = Frame(root)
Label(pframe,text="Port Address: ").pack(side=LEFT)
Entry(pframe,width=20).pack(side=LEFT)
pframe.pack(padx=30,pady=20)
btnSubmit = Button(root,text="Submit",command=printhello(ip),bitmap="question").pack(side=BOTTOM,pady=30)
root.mainloop()

