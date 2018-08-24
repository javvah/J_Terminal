import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
import serial
import serial.tools.list_ports
from serial import SerialException
import socket

port = list(serial.tools.list_ports.comports())

print(port)
root = Tk()
root.title("J Terminal V1.0")
root.geometry("600x440")
root.resizable(width=False, height=False)
nb = ttk.Notebook(root)
page1 = ttk.Frame(nb)
page2 = ttk.Frame(nb)
nb.add(page1, text="Serial")
nb.add(page2, text="Tcp")
nb.pack(expand=1, fill="both")
number = StringVar()
speed = StringVar()
ip = StringVar()
por= StringVar()
var1= IntVar()
var2 = IntVar()
var11= IntVar()
var22 = IntVar()
con1st=0
con2st=0
def serialthread(seri):

    while True :
        if con1st==1:
            txt=seri.read().decode()
            consol1.insert(END,txt)
        else :
            break
def serialthread2(sock):
    while True :
        if con2st==1:
          data=sock.recv(1024).decode()
          consol2.insert(END,data)
        else :
            break

def callback():
    global ser,tr
    global con1st

    if con1st==1 :

       con1st = 0
       tr.join(1)
       ser.close()
       B.config(text="Connect", background="green")
       status.config(text="Status : Disonnected")


    else:
       try:
         print(number.get())
         ser = serial.Serial(number.get()[0:5], speed.get(),writeTimeout = 0)
         con1st = 1
         tr=threading.Thread(target=serialthread,args=(ser,))
         tr.start()
         B.config(text="Disconnect",background="red")
         status.config(text="Status : Connected")

       except SerialException:
           messagebox.showinfo("Error", "port already open")

def send_callbck():
    ser.write(str.encode(e.get()))

    if var1.get()==1:
        ser.write(str.encode("\r"))
    if var2.get()==1 :
        ser.write(str.encode("\n"))
    print("OK")
def consol_clc():
    consol1.delete('1.0',END)
    consol2.delete('1.0',END)
def socket_con():
    global sock,con2st,tr2
    tcp_ip=ip.get()
    tcp_port=int(por.get())
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if con2st==1:
        con2st=0
        tr2.join()
        sock.close()
        BB.config(text="Connect", background="green")
        status2.config(text="Status : Disonnected")
    else :
      try :
        sock.connect((tcp_ip,tcp_port))
        con2st = 1
        tr2 = threading.Thread(target=serialthread2, args=(sock,))
        tr2.start()
        BB.config(text="Disconnect", background="red")
        status2.config(text="Status : Connected")
      except socket.error as e:
        messagebox.showinfo("Error", "Connection Problem")
def socket_send():
    sock.send(str.encode(ee.get()))
    if var11.get() == 1:
        sock.send(str.encode("\r"))
    if var22.get() == 1:
        sock.send(str.encode("\n"))

#page1*********************************
B=Button(page1,text="Connect",command=callback,width=15,background="green")
B1=Button(page1,text="SEND", command=send_callbck,width=15)
B2=Button(page1,text="Clear", command=consol_clc,width=10)
etiket = Label(page1,text="Port:", font=("arial",10))
C = ttk.Combobox(page1, width=30, textvariable=number)
hz = ttk.Combobox(page1, width=12, textvariable=speed)
e = Entry(page1, width=30,)
consol1 = tkst.ScrolledText(page1,width=71,height=18,background="black",foreground="yellow")
chek1=Checkbutton(page1, text="+CR", variable=var1)
chek2=Checkbutton(page1, text="+LF", variable=var2)
status = Label(page1, text="Status : Disconnect", bd=1, relief=SUNKEN, anchor=W)
#page2**********************************
L1 = Label(page2,text="Tcp Ip:", font=("arial",10))
CC = ttk.Combobox(page2, width=30, textvariable=ip)
CC2 = ttk.Combobox(page2, width=12, textvariable=por)
ee = Entry(page2, width=30)
BB=Button(page2,text="Connect",command=socket_con,width=15,background="green")
BB1=Button(page2,text="SEND", command=socket_send,width=15)
BB2=Button(page2,text="Clear", command=consol_clc,width=10)
consol2 = tkst.ScrolledText(page2,width=71,height=18,background="black",foreground="yellow")
chek11=Checkbutton(page2, text="+CR", variable=var11)
chek22=Checkbutton(page2, text="+LF", variable=var22)
status2 = Label(page2, text="Status : Disconnect", bd=1, relief=SUNKEN, anchor=W)

e.insert(0, "type here")
ee.insert(0, "type here")
C['values']=port
C.current(0)
hz['values']="115200","19200","9600","1200","300"
hz.current(0)
CC['values']="127.0.0.1"
CC.current(0)
CC2['values']="5005"
CC2.current(0)

e.pack()
B.pack()
B1.pack()
B2.pack()
C.pack()
etiket.pack()
hz.pack()
chek1.pack()
chek2.pack()
status.pack(side=BOTTOM, fill=X)

CC.pack()
CC2.pack()
ee.pack()
BB.pack()
BB1.pack()
BB2.pack()
L1.pack()
consol2.pack()
chek11.pack()
chek22.pack()
status2.pack(side=BOTTOM, fill=X)


consol1.pack()
etiket.place(x=5, y=5)
C.place(x=40, y=5)
hz.place(x=250, y=5)
B.place(x=350, y=3)
B1.place(x=350, y=35)
B2.place(x=495, y=370)
e.place(x=40, y=35)
consol1.place(x=5, y=75)
chek1.place(x=250, y=35)
chek2.place(x=300, y=35)

L1.place(x=5, y=5)
CC.place(x=50, y=5)
CC2.place(x=260, y=5)
ee.place(x=50, y=35)
BB.place(x=360, y=3)
BB1.place(x=360, y=35)
BB2.place(x=495, y=370)
consol2.place(x=5, y=75)
chek11.place(x=250, y=35)
chek22.place(x=300, y=35)
root.mainloop()


