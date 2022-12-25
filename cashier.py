############## NETWORK ###############
kitchenip = "172.20.10.3"
kitchenport = 7000

############## GUI ###############
from tkinter import *
from tkinter import ttk
import socket
import threading

GUI = Tk()
GUI.geometry('1100x700')
GUI.title("Cashier's section")

FONT = ('Angsana New',20)

F1 = Frame(GUI)
F2 = Frame(GUI)
F3 = Frame(GUI)
F4 = Frame(GUI)
F1.place(x=20,y=20)
F2.place(x=600,y=20)
F3.place(x=650,y=500)
F4.place(x=0,y=300)

########### F1 ############
L11 = ttk.Label(F1,text='Available food',font=FONT,foreground='green').pack()

foodlist = {'1001':{'fid':'1001','name':'Basic beef burger','price':10},
			'1002':{'fid':'1002','name':'Corned beef','price':20},
			'1003':{'fid':'1003','name':'Beef Wellington','price':30},
			'1004':{'fid':'1004','name':'Beef Soup','price':40},
			'1005':{'fid':'1005','name':'Beefsteak','price':50},
			'1006':{'fid':'1006','name':'Boat noodles(Beef)','price':60},
			}

global buffer_tablefood
buffer_tablefood = {}
global order_state 
order_state = False
global order_no
order_no = 1000
def InsertFood(fid):
	global buffer_tablefood
	global order_state
	global order_no

	if order_state == False:
		order_no += 1
		v_orderno.set(order_no)
		order_state = True

	if fid not in buffer_tablefood:
		flist = foodlist[fid]
		flist = list(flist.values()) #['1001','Basic beef burger'',10]
		quan = 1
		total = flist[2] * quan
		flist.append(quan)
		flist.append(total)

		buffer_tablefood[fid] = flist
	else:
		flist = buffer_tablefood[fid] #['1001','Basic beef burger'',10]
		flist[-2] = flist[-2] + 1 #add 1
		flist[-1] = flist[-3] * flist[-2]
		buffer_tablefood[fid] = flist

	table_food.delete(*table_food.get_children()) #clear data in table

	for vl in buffer_tablefood.values():
		table_food.insert('','end',value=vl)

	#total
	total = sum([ vl[-1] for vl in buffer_tablefood.values()])
	v_total.set(f'{total:,.2f} NTD')

########### Table&F2 ############
Ftable = Frame(F1)
Ftable.pack()

rowcount = 0
bcount = 0
for k,v in foodlist.items():
	print('KEY:',k)
	print('VALUE:',v)
	B1 = ttk.Button(Ftable,text=v['name'],width=15)
	B1.configure(command=lambda x=k: InsertFood(x))

	if bcount % 3 == 0:
		rowcount = rowcount + 1 # rowcount += 1
		cl = 0
	elif bcount % 3 == 1:
		cl = 1
	elif bcount % 3 == 2:
		cl = 2
	else:
		pass
	
	B1.grid(row=rowcount,column=cl ,padx=10,pady=10,ipady=10)

	bcount = bcount + 1

### F2 ###
L21 = ttk.Label(F2,text='Selected food',font=FONT,foreground='green').pack()

header = ['ID','Food Name','Price','Quantity','Total']
hw = [70,150,70,70,70] # |  ID  |   Foodname   | Price |xxxx

table_food = ttk.Treeview(F2,height=15,column=header,show='headings')
table_food.pack()

for hd,w in zip(header,hw):
	table_food.heading(hd,text=hd)
	table_food.column(hd,width=w)

v_total = StringVar() #TotalPrice
Ltotal = ttk.Label(GUI,text='Total: ',font=('Angsana New',30),foreground='green').place(x=500,y=450)
total = ttk.Label(GUI,textvariable=v_total)
total.configure(font=('Angsana New',30,'bold'))
total.configure(foreground='green')
total.place(x=600,y=450)

v_orderno = StringVar() #OrderNO.
Lorderno = ttk.Label(GUI,text='Order No. ',font=('Angsana New',30),foreground='green').place(x=500,y=400)
orderno = ttk.Label(GUI,textvariable=v_orderno)
orderno.configure(font=('Angsana New',30,'bold'))
orderno.configure(foreground='green')
orderno.place(x=650,y=400)

######## FUNCTIONS ########
def ConverttoNetwork(data):
	text = ''
	for d in data.values():
		text += '{}={},'.format(d[0],d[-2])
	text = text[:-1]
	return text

def SendtoKitchen():
	global buffer_tablefood

	data = 'k|' + 'SST' + v_orderno.get() + '|'

	v_orderno.set('-')
	v_total.set('0.00 NTD')
	
	global order_state
	order_state = False
	
	table_food.delete(*table_food.get_children()) #clear data in treeview

	data = data + ConverttoNetwork(buffer_tablefood)

	serverip =  kitchenip 
	port = kitchenport 
	server = socket.socket()
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	server.connect((serverip,port))
	server.send(data.encode('utf-8'))

	data_server = server.recv(1024).decode('utf-8')
	print('Data from Server: ', data_server)
	server.close()

	buffer_tablefood = {}

def ThreadSendtoKitchen():
	task = threading.Thread(target=SendtoKitchen)
	task.start()

########### F3 ############
B1 = ttk.Button(F3,text="Done",command=ThreadSendtoKitchen)
B1.grid(row=0,column=0,ipadx=20,ipady=10,padx=10)

########### F4 ############
img = PhotoImage(file="cashier.png")
CASH= Label(F4,image=img).pack()

GUI.mainloop()
