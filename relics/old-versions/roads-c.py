from tkinter import *
import random
import time
import _thread

root = Tk()
root.title("metro")
#root['bg']='ivory'
root.option_add('*Font', 'Calibri 16')
#root.option_add('*Background', 'ivory')
M=Canvas(root,height=650,width=700,bd=0)
#llis=[M.create_oval(0,0,50,50,fill='ivory',outline='ivory'),
#M.create_oval(650,0,700,50,fill='ivory',outline='ivory'),
#M.create_oval(0,600,50,650,fill='ivory',outline='ivory'),
#M.create_oval(650,600,700,650,fill='ivory',outline='ivory'),
#M.create_rectangle(25,0,675,650,fill='ivory',outline='ivory'),
#M.create_rectangle(0,25,700,625,fill='ivory',outline='ivory')]
M.grid(row=1,column=1,rowspan=200)

timet=0
ti=1
run=1
rtot=0
ltot=0
money=100
delivered=0
newtrlev=1
k_lis = []
k_x=[]
k_y=[]
k_level=[]
k_tagids=[]
k_ids=[]
k_txtids=[]
k_full=[]
k_occ=[]
r_mem=[]
l_route=[]
l_pos=[]
l_color=[]
l_dis=[]
l_color=['#EE1111','#4DB361','#BB44BB','#3370CC','#F79709','#FFEE00','#AF833F','#AAAAAA']
l_box=[]
l_ele=[]
l_trnum=[]
l_sch=[]
ktot=0
navi=[]


def addknot(x):
	global ktot,run,money
	pool=[]
	x=350
	y=300
	l=1
	for j in range(6):
		for i in range(0,l):
			pool.append((x,y))
			x+=50
		for i in range(0,l):
			pool.append((x,y))
			y+=50
		l+=1
		for i in range(0,l):
			pool.append((x,y))
			x-=50
		for i in range(0,l):
			pool.append((x,y))
			y-=50
		l+=1

	print("pool:  ",pool)
	for i in range(5):
		rd=random.randint(0, min(10,len(pool)))
		x,y=pool[rd]
		pool.pop(rd)
		k_x.append(x+random.randint(-10,10))
		k_y.append(y+random.randint(-10,10))
		k_lis.append([])
		k_level.append(1)
		k_occ.append([])
		k_tagids.append(M.create_text(k_x[ktot],k_y[ktot]+15,text=k_lis[ktot]))
		k_full.append(0)
		k_ids.append(M.create_oval(k_x[ktot]-7,k_y[ktot]-7,k_x[ktot]+7,k_y[ktot]+7))
		k_txtids.append(M.create_text(k_x[ktot],k_y[ktot],text=ktot))
		ktot+=1
		floyed()
	while run and len(pool):
		for i in range(60):
			time.sleep(ti)
			if not run:
				break
		rd=random.randint(0, min(10,len(pool)))
		x,y=pool[rd]
		pool.pop(rd)
		pool.pop(0)
		k_x.append(x+random.randint(-10,10))
		k_y.append(y+random.randint(-10,10))
		k_lis.append([])
		k_level.append(1)
		k_occ.append([])
		k_tagids.append(M.create_text(k_x[ktot],k_y[ktot]+15,text=k_lis[ktot]))
		k_full.append(0)
		k_ids.append(M.create_oval(k_x[ktot]-7,k_y[ktot]-7,k_x[ktot]+7,k_y[ktot]+7,fill='black'))
		k_txtids.append(M.create_text(k_x[ktot],k_y[ktot],text=ktot))
		ktot+=1
		money+=10
		floyed()

def addpeople(x):
	global timet
	time.sleep(ti*2)
	while run:
		where=random.randint(0,ktot-1)
		towhere=random.randint(0,ktot-1)
		if where!=towhere:
			k_lis[where].append(towhere)
			if int(timet/10)%6==4:
				time.sleep(ti*10/ktot**2)  #速率
			else:
				time.sleep(ti*20/ktot)  #速率


def modline(line,route):
	print(line,"line edited")
	if l_ele[line]!=-1:
		M.delete(l_ele[line])
	l_route[line]=route
	l_pos[line]=[]
	l_dis[line]=[]
	for i in range(0,len(l_route[line])):
		l_route[line][i]=int(l_route[line][i])
		M.itemconfig(k_ids[l_route[line][i]],outline=l_color[line])
		l_pos[line].append((k_x[l_route[line][i]],k_y[l_route[line][i]]))
	#print(k_x)
	for i in range(0,len(l_route[line])-1):
		#print(i,l_route[line])
		l_dis[line].append(int(((k_x[l_route[line][i]]-k_x[l_route[line][i+1]])**2+(k_y[l_route[line][i]]-k_y[l_route[line][i+1]])**2)**0.5))
	l_ele[line]=M.create_line(l_pos[line],fill=l_color[line],width=4)
	M.tag_lower(l_ele[line])
	print(l_route)
	floyed()

def addtrolley(line,d):
	try:
		level=newtrlev
	except:
		return
	if pay(20*level):
		_thread.start_new_thread( trolley,(line,d,level))
		l_trnum[line]+=1
'''
def trolley(line,dire,level):
	if dire:
		routing=l_route[line][::-1]
		dis=l_dis[line][::-1]
	else:
		routing=l_route[line]
		dis=l_dis[line]
	pas=[]
	print(routing)
	x=k_x[routing[0]]
	y=k_y[routing[0]]
	tro=M.create_polygon(x,y,x-5,y-10,x+5,y-10,fill=l_color[line])
	tag=M.create_text(x,y-20,text=pas,fill=l_color[line])
	while timet<l_sch[line][dire]:
		time.sleep(1)
	l_sch[line][dire]=timet+10
	#time.sleep(ti*random.randint(3,15))
	for at in range(len(routing)-1):
		while line in k_occ[routing[at]] or len(k_occ[routing[at]])>=k_level[routing[at]]:
			time.sleep(ti*1)
		k_occ[routing[at]].append(line)
		M.itemconfig(k_ids[routing[at]],outline=l_color[line])
		i=0
		while i<len(pas):
			if line*2+dire not in navi[routing[at]][pas[i]]:
				k_lis[routing[at]].append(pas[i])
				pas.pop(i)
				M.itemconfig(tag,text=pas)
				#M.itemconfig(k_tagids[routing[at]],text=k_lis[routing[at]][0:min(6,len(k_lis[routing[at]]))])
				time.sleep(ti*0.5/level)
				i-=1
			i+=1
		i=0
		while i <len(k_lis[routing[at]]) and len(pas)<level*3+3:
			#print(i,len(k_lis[routing[at]]),routing[at])
			#print(k_lis[routing[at]][i])
			#print(navi)
			if line*2+dire in navi[routing[at]][k_lis[routing[at]][i]]:
				pas.append(k_lis[routing[at]][i])
				k_lis[routing[at]].pop(i)
				M.itemconfig(tag,text=pas)
				#M.itemconfig(k_tagids[routing[at]],text=k_lis[routing[at]][0:min(6,len(k_lis[routing[at]]))])
				time.sleep(ti*0.5/level)
				i-=1
			i+=1
		print(pas)
		time.sleep(ti*1/level)
		try:
			k_occ[routing[at]].remove(line)
		except:
			pass
		dash=M.create_line(k_x[routing[at]],k_y[routing[at]],k_x[routing[at+1]],k_y[routing[at+1]],fill=l_color[line])
		dist=int(dis[at])
		for i in range(dist):
			M.move(tro,(k_x[routing[at+1]]-x)/dist,(k_y[routing[at+1]]-y)/dist)
			M.move(tag,(k_x[routing[at+1]]-x)/dist,(k_y[routing[at+1]]-y)/dist)
			time.sleep(ti*0.02)
		M.delete(dash)
		x=(k_x[routing[at+1]])
		y=(k_y[routing[at+1]])
		time.sleep(ti*0.5)
	while len(pas):
		k_lis[routing[-1]].append(pas[0])
		pas.pop(0)
		M.itemconfig(tag,text=pas)
		#M.itemconfig(k_tagids[routing[at]],text=k_lis[routing[at]][0:min(6,len(k_lis[routing[at]]))])
		time.sleep(ti*0.5/level)
	M.delete(tro)
	M.delete(tag)
	if run:
		trolley(line,1-dire,level)
'''
def trolley(line,dire,level):
	if dire:
		atk=l_route[line][-1]
	else:
		atk=l_route[line][0]
	pas=[]
	x=k_x[atk]
	y=k_y[atk]
	tro=M.create_polygon(x,y,x-5,y-10,x+5,y-10,fill=l_color[line])
	tag=M.create_text(x,y-20,text=pas,fill=l_color[line])
	while timet<l_sch[line][dire]:
		time.sleep(1)
	l_sch[line][dire]=timet+10
	#time.sleep(ti*random.randint(3,15))
	while True:
		while line in k_occ[atk] or len(k_occ[atk])>=k_level[atk]:
			time.sleep(ti*1)
		k_occ[atk].append(line)
		M.itemconfig(k_ids[atk],outline=l_color[line])
		i=0
		while i<len(pas):
			if line*2+dire not in navi[atk][pas[i]]:
				k_lis[atk].append(pas[i])
				pas.pop(i)
				M.itemconfig(tag,text=pas)
				#M.itemconfig(k_tagids[atk],text=k_lis[atk][0:min(6,len(k_lis[atk]))])
				time.sleep(ti*0.5/level)
				i-=1
			i+=1
		i=0
		while i <len(k_lis[atk]) and len(pas)<level*3+3:
			#print(i,len(k_lis[atk]),atk)
			#print(k_lis[atk][i])
			#print(navi)
			if line*2+dire in navi[atk][k_lis[atk][i]]:
				pas.append(k_lis[atk][i])
				k_lis[atk].pop(i)
				M.itemconfig(tag,text=pas)
				#M.itemconfig(k_tagids[atk],text=k_lis[atk][0:min(6,len(k_lis[atk]))])
				time.sleep(ti*0.5/level)
				i-=1
			i+=1
		print(pas)
		time.sleep(ti*1/level)
		try:
			k_occ[atk].remove(line)
		except:
			pass
		try:
			at=l_route[line].index(atk)
		except:
			break
		if (at==0 and dire==1) or (at==len(l_route[line])-1 and dire==0):
			break
		else:
			natk=l_route[line][at+1-dire*2]
		dash=M.create_line(k_x[atk],k_y[atk],k_x[natk],k_y[natk],fill=l_color[line])
		print(at,dire)
		dist=int(l_dis[line][at-dire])
		for i in range(dist):
			M.move(tro,(k_x[natk]-x)/dist,(k_y[natk]-y)/dist)
			M.move(tag,(k_x[natk]-x)/dist,(k_y[natk]-y)/dist)
			time.sleep(ti*0.02)
		M.delete(dash)
		x=(k_x[natk])
		y=(k_y[natk])
		time.sleep(ti*0.5)
		atk=natk
	while len(pas):
		k_lis[atk].append(pas[0])
		pas.pop(0)
		M.itemconfig(tag,text=pas)
		#M.itemconfig(k_tagids[atk],text=k_lis[atk][0:min(6,len(k_lis[atk]))])
		time.sleep(ti*0.5/level)
	M.delete(tro)
	M.delete(tag)
	if run:
		trolley(line,1-dire,level)

def floyed():
	maps=[]
	finder=[]
	global navi
	for i in range(ktot+1):      # 创建一个5行的列表（行）
		maps.append([])        # 在空的列表中添加空的列表
		finder.append([])
		for j in range(ktot+1):  # 循环每一行的每一个元素（列）
			if i==j:
				maps[i].append(0)
			else:
				maps[i].append(10000000000)
			finder[i].append(set())
	#print(maps)
	#print(finder)
	for i in range(ltot):
		for j in range(len(l_dis[i])):
			print(i,j,l_route[i][j],l_route[i][j+1],maps[l_route[i][j]][l_route[i][j+1]])
			maps[l_route[i][j]][l_route[i][j+1]]=l_dis[i][j]
			maps[l_route[i][j+1]][l_route[i][j]]=l_dis[i][j]
			finder[l_route[i][j]][l_route[i][j+1]].add(i*2)
			finder[l_route[i][j+1]][l_route[i][j]].add(i*2+1)
	#print(maps)
	#print(finder)
	for k in range(ktot):
		for i in range(ktot):
			for j in range(ktot):
				if maps[i][j]>maps[i][k]+maps[k][j]:
					#print(i,j,maps[i][j],maps[i][k],maps[k][j])
					maps[i][j]=maps[i][k]+maps[k][j]
					finder[i][j]=finder[i][k]
				elif maps[i][j]==maps[i][k]+maps[k][j]:
					finder[i][j]=finder[i][k]|finder[i][j]
	#print(maps)
	navi=finder
	#print(navi)


def addline():
	global ltot
	if ltot>=len(l_color):
		return 0
	if not pay(50*ltot):
		return 0
	#l_box.append(Entry(root,width=30,bd=0,highlightthickness=4,highlightbackground=l_color[ltot]))
	#l_box[ltot].grid(row=ltot+10,column=2)
	l_route.append([])
	l_ele.append(-1)
	l_dis.append([])
	l_pos.append([])
	l_trnum.append(0)
	l_sch.append([0,0])
	miltot=ltot
	Label(root,text='line'+str(ltot),fg=l_color[ltot]).grid(row=ltot+100,column=2)
	#Button(root,bg='snow',text="edit",width=10,command=lambda:editline(miltot),bd=0).grid(row=ltot+10,column=3)
	#Button(root,bg='snow',text="trolley(Down)",width=15,command=lambda:addtrolley(miltot,0),bd=0).grid(row=ltot+10,column=4)
	#Button(root,bg='snow',text="trolley(Up)",width=15,command=lambda:addtrolley(miltot,1),bd=0).grid(row=ltot+10,column=5,columnspan=2)
	ltot+=1
	return 1

def updknot(num):
	#print('updwk')
	#print(updwk.get())
	if pay(50*k_level[num]):
		k_level[num]+=1
		M.coords(k_ids[num],k_x[num]-6-k_level[num]*2,k_y[num]-6-k_level[num]*2,k_x[num]+6+k_level[num]*2,k_y[num]+6+k_level[num]*2) #resize
		M.tag_raise(k_tagids[num])

def updtr():
	global newtrlev
	if pay(newtrlev*100):
		newtrlev+=1
		updtrb.config(text='train level '+str(newtrlev))


def pay(price):
	global money
	if money >= price:
		money-=price
		message('paid '+str(price),'normal')
		return True
	else:
		message('not enough money '+str(money-price),'warning')
		return False

def changespeed(s):
	global ti
	ti=1-int(s)*0.1

def message(text,type='normal'):
	messagebox.config(text=text)

def exe(x):
	inp=(cmdbox.get()).split(' ')
	if inp[0]=='mod':
		lin=int(inp[1])
		rt=l_route[lin]
		print('r=',rt)
		if inp[2]=='e':
			h=rt.index(int(inp[3]))
			if h==0:
				rt=inp[4:][::-1]+rt
			elif h==len(rt)-1:
				rt+=inp[4:]
		elif inp[2]=='d':
			if len(l_route[lin])>=2:
				h=rt.index(int(inp[3]))
				rt.pop(h)
		else:
			l=int(inp[2])
			m=inp[3:-1]
			r=int(inp[-1])
			lp=rt.index(l)
			rp=rt.index(r)
			if m=='':
				if lp<rp:
					rt[lp+1:rp]=[]
				else:
					rt[rp+1:lp]=[]
			elif lp<rp:
				rt[lp+1:rp]=list(m)
			else:
				rt[rp+1:lp]=list(m)[::-1]
		modline(lin,rt)
		message('line '+str(lin)+' modified','normal')
	elif inp[0]=='new':
		if addline():		
			modline(ltot-1,inp[1:])
			message('new line '+str(ltot-1),'normal')
	elif inp[0]=='adt':
		lin=int(inp[1])
		if l_sch[lin][0]>l_sch[lin][1]:
			addtrolley(lin,1)
		else:
			addtrolley(lin,0)
		#message('added train to line '+str(lin),'normal')
	elif inp[0]=='upd':
		if inp[1]=='train':
			updtr()
		else:
			updknot(int(inp[1]))
	else:
		message('invalid syntax','warning')
	cmdbox.selection_range(0, END)
	
	

_thread.start_new_thread( addknot, (1,) )
_thread.start_new_thread( addpeople, (1,) )
tk_delivered=StringVar()
tk_money=StringVar()
tk_tm=StringVar()
tk_delivered.set(delivered)
tk_money.set(money)
Label(root,bitmap='hourglass',compound='left',textvariable=tk_tm).grid(row=1,column=2,sticky='WE')
Label(root,bitmap='info',compound='left',textvariable=tk_delivered).grid(row=2,column=2,sticky='WE')
Label(root,bitmap='gray75',compound='left',bg='gold',textvariable=tk_money).grid(row=3,column=2,sticky='WE')
#Button(root,text='upgrade station:    ',command=updknot,width=20,bd=0).grid(row=2,column=3,columnspan=2)
#updwk=Entry(root,width=3,bd=0,highlightthickness=1,highlightbackground='gray')
#updwk.grid(row=2,column=4,stick='E',padx=25)
updtrb=Label(root,text='train level 1')
updtrb.grid(row=4,column=2)
#newtrlevel=Entry(root,width=3,bd=0,highlightthickness=1,highlightbackground='gray')
#newtrlevel.grid(row=2,column=2,stick='E',padx=40)
#newtrlevel.insert(0, '1')
#Button(root,text="addline",width=10,command=addline,bd=0).grid(row=2,column=5)
Scale(root,from_=0,to=9,command=changespeed,length=60,orient='horizon').grid(row=5,column=2,sticky='WE')

cmdbox=Entry(root,justify='center',bd=0,highlightthickness=4)
cmdbox.grid(row=201,column=1,sticky='WE',columnspan=20)
cmdbox.bind('<Return>',exe)
messagebox=Label(root)
messagebox.grid(row=202,column=1,sticky='WE',columnspan=20)

#Button(root,text="tx_确定",width=20,command=lambda:editline(0),bd=0).pack()
#Button=(root,text="edit",command=lambda:editline(1)).pack()

def knotchek(num):
	global run,money,delivered
	wcolor=['#FFFFFF','#FFAAAA','#FF9999','#FF8888','#FF7777','#FF6666','#FF5555','#FF4444','#FF3333','#FF2222','#FF0000']
	i=0
	while i<len(k_lis[num]):
		if k_lis[num][i]==num:
			k_lis[num].pop(i)
			delivered+=1
			money+=2
			i-=1
		i+=1
	if len(k_lis[num])>k_level[num]*8:
		if k_full[num]==10:
			run=0
			M.itemconfig(k_txtids[num],text='game over!')
		else:
			k_full[num]+=1/k_level[num]
	else:
		k_full[num]=0
	M.itemconfig(k_ids[num],fill=wcolor[int(k_full[num])])

def pro(x):
	global timet
	while run:
		for i in range(0,ktot):
			knotchek(i)
			#print(k_tagids,k_lis)
			if(len(k_lis[i])<6):
				M.itemconfig(k_tagids[i],text=k_lis[i])
			else:
				M.itemconfig(k_tagids[i],text=k_lis[i][0:5]+['...('+str(len(k_lis[i]))+')'])
		root.update()
		tk_delivered.set(delivered)
		tk_money.set(money)
		tk_tm.set(timet)
		time.sleep(ti*1)
		timet+=1
		if timet%60==35:
			message('rush hour!','normal')
		elif timet%60==50:
			message('rush hour ends','normal')
_thread.start_new_thread( pro, (1,) )




mainloop()
