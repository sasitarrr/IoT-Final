############## NETWORK #################
kitchenip = "172.20.10.3"
kitchenport = 7000

################# GUI ##################
from tkinter import *
from tkinter import ttk
import socket
import threading

foodlist = {'1001':{'fid':'1001','name':'Basic beef burger','price':10},
			'1002':{'fid':'1002','name':'Corned beef','price':20},
			'1003':{'fid':'1003','name':'Beef Wellington','price':30},
			'1004':{'fid':'1004','name':'Beef Soup','price':40},
			'1005':{'fid':'1005','name':'Beefsteak','price':50},
			'1006':{'fid':'1006','name':'Boat noodles(Beef)','price':60},
			}

GUI = Tk()
GUI.geometry('700x700')
GUI.title("Kitchen's section")

FONT = ('Angsana New',20)

F01 = Frame(GUI)
F0 = Frame(GUI)
F1 = Frame(GUI)
F2 = Frame(GUI)
F01.place(x=10,y=0)
F0.place(x=150,y=50)
F1.place(x=20,y=120)
F2.place(x=220,y=120)

################ F0 ################
L1 = Label(F0, text = "Kitchen's temperature", font = FONT).pack()

v_status = StringVar()
v_status.set("<< No status >>")
L2 = Label(F0, textvariable = v_status, font = FONT, foreground='red').pack()

img = PhotoImage(file="level1.png")
ICON = Label(F01,image=img)
ICON.pack()

################ F1 ################
L11 = ttk.Label(F1,text='Queue',font=FONT,foreground='green').pack()

header = ['Food Order No.','Quantity']
hwid = [100,70]

table_queue = ttk.Treeview(F1,height=25,column=header,show='headings')
table_queue.pack()

for hd,hw in zip(header,hwid):
	table_queue.heading(hd,text=hd)
	table_queue.column(hd,width=hw)

################ F2 ################
L21 = ttk.Label(F2,text='Food list',font=FONT,foreground='green').pack()

header = ['ID','Food Name','Price','Quantity','Total']
hwid = [70,150,70,70,70] 

table_food = ttk.Treeview(F2,height=25,column=header,show='headings')
table_food.pack()

for hd,hw in zip(header,hwid):
	table_food.heading(hd,text=hd)
	table_food.column(hd,width=hw)

################# FUNCTIONS ##################
def runservertemp():
    #####################
    serverip = '172.20.10.3'
    port = 9000
    #####################

    buffsize = 4096

    while True:
            server = socket.socket()
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            server.bind((serverip,port))
            server.listen(1)
            print('waiting micropython...')

            client, addr = server.accept()
            print('connected from:', addr)

            data = client.recv(buffsize).decode('utf-8')
            print('Data from MicroPython: ',data)
            
            data_split = data.split(":") #TEMP:20.5

            if float(data_split[1]) > 20.5:
                img = PhotoImage(file="level3.png")
                ICON.configure(image=img)
                ICON.image = img
                v_status.set("{} status {}".format(data_split[0], data_split[1] ))
            elif float(data_split[1]) > 20.4:
                img = PhotoImage(file="level2.png")
                ICON.configure(image=img)
                ICON.image = img
                v_status.set("{} status {}".format(data_split[0], data_split[1] ))
            elif float(data_split[1]) > 20.3:
                img = PhotoImage(file="level1.png")
                ICON.configure(image=img)
                ICON.image = img
                v_status.set("{} status {}".format(data_split[0], data_split[1] ))
            else:
                img = PhotoImage(file="level1.png")
                ICON.configure(image=img)
                ICON.image = img
                v_status.set("too cold")
            
            client.send('received your messages.'.encode('utf-8'))
            client.close()

def ConverttoTable(data):
	data = data.split('|')[2] #'k|1001=3,1002=2' to ['ID','Name','Price','Qtty','Total']
	food = data.split(',')
	allfood = []
	for f in food:
		fs = f.split('=')
		fid = fs[0]
		quan = fs[1]
		dt = [fid,
			  foodlist[fid]['name'],
			  foodlist[fid]['price'],
			  quan,
			  int(foodlist[fid]['price']) * int(quan)]
		allfood.append(dt)
	print(allfood)
	return allfood

global food_cooking
food_cooking = {}
global chef_cooking
chef_cooking = [] #chef_cooking = [1001,1002,1003]
def RunServer():
	global chef_cooking
	my_ip = kitchenip 
	port = kitchenport

	while True:
		server = socket.socket()
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

		server.bind((my_ip,port))
		server.listen(1)
		print('Waiting for client...')

		client, addr = server.accept()
		print('Connected from: ',str(addr))
		data = client.recv(1024).decode('utf-8') #k-Q1001-1001=3-1002=1

		if data[0] == 'k':
	
			ordernum = data.split('|')[1]
			
			food_cooking[ordernum] = ConverttoTable(data) #add result to dictionary

			if len(chef_cooking) == 0: #no oreder
				v_current.set('#' + ordernum)

				sumquan = []
				for fc in food_cooking[ordernum]:
					table_food.insert('','end',value=fc)
					sumquan.append(int(fc[3]))

				print('ORDER NO.',ordernum,type(ordernum))
				table_queue.insert('','end',value=[ordernum,sum(sumquan)])
				chef_cooking.append([ordernum,sum(sumquan)])

			else: #have order
				sumquan = []
				for fc in food_cooking[ordernum]:
					sumquan.append(int(fc[3]))
			
				table_queue.insert('','end',value=[ordernum,sum(sumquan)])
				chef_cooking.append([ordernum,sum(sumquan)])
		else:
			print('<<<< message is not for kitchen >>>>')

		print('Message from client: ',data)
		client.send('We received your Message.'.encode('utf-8'))
		client.close()

v_current = StringVar()
v_current.set('----ORDER NO.----')
currentorder = Label(GUI,textvariable=v_current)
currentorder.configure(font=(None,30,'bold'))
currentorder.configure(foreground='green')
currentorder.place(x=400,y=50)

def ShowFood(event=None):
	select = table_queue.selection() 
	data = table_queue.item(select) 
	v_current.set('#' + data['values'][0])
	print('DATA:',data)
	table_food.delete(*table_food.get_children())
	for fc in food_cooking[data['values'][0]]:
		table_food.insert('','end',value=fc)

table_queue.bind('<Double-1>',ShowFood)

def ThreadRunServer():
	task = threading.Thread(target=RunServer)
	task.start()

def Threadrunservertemp():
	task = threading.Thread(target = runservertemp)
	task.start()

ThreadRunServer()
Threadrunservertemp()

GUI.mainloop()
