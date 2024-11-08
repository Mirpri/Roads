import tkinter

import random
import time
import _thread

root = tkinter.Tk()
root.title("metro")
M=tkinter.Canvas(root,height=650,width=700,bg="white")
M.grid(row=1,column=1,rowspan=2000)

ti=1
run=1
rtot=0
ltot=0
money=150
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
	for i in range(3):
		rd=random.randint(0, min(10,len(pool)))
		x,y=pool[rd]
		pool.pop(rd)
		k_x.append(x+random.randint(-10,10))
		k_y.append(y+random.randint(-10,10))
		k_lis.append([])
		k_level.append(1)
		k_occ.append([])
		k_tagids.append(M.create_text(k_x[ktot],k_y[ktot]+15,text=str(k_lis[ktot])))
		k_full.append(0)
		k_ids.append(M.create_oval(k_x[ktot]-7,k_y[ktot]-7,k_x[ktot]+7,k_y[ktot]+7))
		k_txtids.append(M.create_text(k_x[ktot],k_y[ktot],text=ktot))
		ktot+=1
		floyed()
	while run and len(pool):
		for i in range(30):
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
		k_tagids.append(M.create_text(k_x[ktot],k_y[ktot]+15,text=str(k_lis[ktot])))
		k_full.append(0)
		k_ids.append(M.create_oval(k_x[ktot]-7,k_y[ktot]-7,k_x[ktot]+7,k_y[ktot]+7,fill='black'))
		k_txtids.append(M.create_text(k_x[ktot],k_y[ktot],text=ktot))
		ktot+=1
		money+=10
		floyed()

def addpeople(x):
	time.sleep(ti*2)
	while run:
		where=random.randint(0,ktot-1)
		towhere=random.randint(0,ktot-1)
		if where!=towhere:
			k_lis[where].append(towhere)
			time.sleep(ti*15/ktot)  #速率

def editline(line):
	print(line,"line edited")
	if l_ele[line]!=-1:
		#print(l_ele[line])
		M.delete(l_ele[line])
		#M.tag_lower(M.create_line(l_pos[line],fill=l_color[line],dash=(2,2)))
	l_pos[line]=[]
	l_route[line]=(l_box[line].get()).split("-")
	l_dis[line]=[]
	for i in range(0,len(l_route[line])):
		l_route[line][i]=int(l_route[line][i])
		M.itemconfig(k_ids[l_route[line][i]],outline=l_color[line])
		l_pos[line].append((k_x[l_route[line][i]],k_y[l_route[line][i]]))
	#print(k_x)
	for i in range(0,len(l_route[line])-1):
		#print(i,l_route[line])
		l_dis[line].append(int(((k_x[l_route[line][i]]-k_x[l_route[line][i+1]])**2+(k_y[l_route[line][i]]-k_y[l_route[line][i+1]])**2)**0.5))
	l_ele[line]=M.create_line(l_pos[line],fill=l_color[line],width=2)
	M.tag_lower(l_ele[line])
	#print(l_route,l_dis)
	floyed()

def addtrolley(line,d):
	try:
		level=newtrlev
	except:
		return
	if pay(20*level+10*l_trnum[line]):
		_thread.start_new_thread( trolley,(line,d,level))
		l_trnum[line]+=1

def trolley(line,dire,level):
	if dire:
		route=l_route[line][::-1]
		dis=l_dis[line][::-1]
	else:
		route=l_route[line]
		dis=l_dis[line]
	pas=[]
	print(route)
	x=k_x[route[0]]
	y=k_y[route[0]]
	tro=M.create_polygon(x,y,x-5,y-10,x+5,y-10,fill=l_color[line])
	tag=M.create_text(x,y-20,text=pas,fill=l_color[line])
	#time.sleep(ti*random.randint(3,15))
	for at in range(len(route)-1):
		while line in k_occ[route[at]] or len(k_occ[route[at]])>=k_level[route[at]]:
			time.sleep(ti*1)
		k_occ[route[at]].append(line)
		M.itemconfig(k_ids[route[at]],outline=l_color[line])
		i=0
		while i<len(pas):
			if line*2+dire not in navi[route[at]][pas[i]]:
				k_lis[route[at]].append(pas[i])
				pas.pop(i)
				M.itemconfig(tag,text=pas)
				M.itemconfig(k_tagids[route[at]],text=str(k_lis[route[at]]))
				time.sleep(ti*0.5/level)
				i-=1
			i+=1
		i=0
		while i <len(k_lis[route[at]]) and len(pas)<level*3+3:
			#print(i,len(k_lis[route[at]]),route[at])
			#print(k_lis[route[at]][i])
			#print(navi)
			if line*2+dire in navi[route[at]][k_lis[route[at]][i]]:
				pas.append(k_lis[route[at]][i])
				k_lis[route[at]].pop(i)
				M.itemconfig(tag,text=pas)
				M.itemconfig(k_tagids[route[at]],text=str(k_lis[route[at]]))
				time.sleep(ti*0.5/level)
				i-=1
			i+=1
		print(pas)
		time.sleep(ti*1/level)
		k_occ[route[at]].remove(line)

		dash=M.create_line(k_x[route[at]],k_y[route[at]],k_x[route[at+1]],k_y[route[at+1]],fill=l_color[line])
		dist=int(dis[at])
		for i in range(dist):
			M.move(tro,(k_x[route[at+1]]-x)/dist,(k_y[route[at+1]]-y)/dist)
			M.move(tag,(k_x[route[at+1]]-x)/dist,(k_y[route[at+1]]-y)/dist)
			time.sleep(ti*0.02)
		M.delete(dash)
		x=(k_x[route[at+1]])
		y=(k_y[route[at+1]])
		time.sleep(ti*0.5)
	while len(pas):
		k_lis[route[-1]].append(pas[0])
		pas.pop(0)
		M.itemconfig(tag,text=pas)
		M.itemconfig(k_tagids[route[at]],text=str(k_lis[route[at]]))
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
		return
	if not pay(50*ltot):
		return
	l_box.append(tkinter.Entry(root,width=30,bd=0,highlightthickness=4,highlightbackground=l_color[ltot]))
	l_box[ltot].grid(row=ltot+10,column=2)
	l_route.append([])
	l_ele.append(-1)
	l_dis.append([])
	l_pos.append([])
	l_trnum.append(0)
	miltot=ltot
	tkinter.Button(root,bg='snow',text="edit",width=10,command=lambda:editline(miltot),bd=0).grid(row=ltot+10,column=3)
	tkinter.Button(root,bg='snow',text="trolley(Down)",width=15,command=lambda:addtrolley(miltot,0),bd=0).grid(row=ltot+10,column=4)
	tkinter.Button(root,bg='snow',text="trolley(Up)",width=15,command=lambda:addtrolley(miltot,1),bd=0).grid(row=ltot+10,column=5,columnspan=2)
	ltot+=1

def updknot():
	#print('updwk')
	#print(updwk.get())
	try:
		num=int(updwk.get())
	except:
		return
	if pay(50*k_level[num]):
		k_level[num]+=1
		M.coords(k_ids[num],k_x[num]-6-k_level[num]*2,k_y[num]-6-k_level[num]*2,k_x[num]+6+k_level[num]*2,k_y[num]+6+k_level[num]*2) #resize
		M.tag_raise(k_tagids[num])

def updtr():
	global newtrlev
	if pay(newtrlev*100):
		newtrlev+=1
		updtrb.config(text='upgrade train (level '+str(newtrlev)+')')


def pay(price):
	global money
	if money >= price:
		money-=price
		return True
	else:
		l=tkinter.Label(root,bg='red',text=money-price)
		l.grid(row=1,column=4,sticky='WE',columnspan=2)
		root.update()
		time.sleep(ti*0.5)
		l.destroy()
		root.update()
		return False

def changespeed(s):
	global ti
	ti=1-int(s)*0.1

_thread.start_new_thread( addknot, (1,) )
_thread.start_new_thread( addpeople, (1,) )
tk_delivered=tkinter.StringVar()
tk_money=tkinter.StringVar()
tk_delivered.set(delivered)
tk_money.set(money)
tkinter.Label(root,bg='white',textvariable=tk_delivered).grid(row=1,column=2,sticky='WE',columnspan=2)
tkinter.Label(root,bg='gold',textvariable=tk_money).grid(row=1,column=4,sticky='WE',columnspan=2)
tkinter.Button(root,text='upgrade station:    ',command=updknot,width=20,bd=0).grid(row=2,column=3,columnspan=2)
updwk=tkinter.Entry(root,width=3,bd=0,highlightthickness=1,highlightbackground='gray')
updwk.grid(row=2,column=4,stick='E',padx=25)
updtrb=tkinter.Button(root,text='upgrade train (level 1)',command=updtr,bd=0)
updtrb.grid(row=2,column=2)
#newtrlevel=tkinter.Entry(root,width=3,bd=0,highlightthickness=1,highlightbackground='gray')
#newtrlevel.grid(row=2,column=2,stick='E',padx=40)
#newtrlevel.insert(0, '1')
tkinter.Button(root,text="addline",width=10,command=addline,bd=0).grid(row=2,column=5)
tkinter.Scale(root,from_=0,to=9,command=changespeed,length=60).grid(row=1,column=6,sticky='E',rowspan=2)
addline()
#tkinter.Button(root,text="tx_确定",width=20,command=lambda:editline(0),bd=0).pack()
#tkinter.Button=(root,text="edit",command=lambda:editline(1)).pack()

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
	while run:
		for i in range(0,ktot):
			knotchek(i)
			#print(k_tagids,k_lis)
			M.itemconfig(k_tagids[i],text=str(k_lis[i]))
		root.update()
		tk_delivered.set(delivered)
		tk_money.set(money)
		time.sleep(ti*1)
_thread.start_new_thread( pro, (1,) )




tkinter.mainloop()
