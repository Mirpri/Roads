from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import random
import time
import _thread
from icon import img
import base64
import os

try:
    os.mkdir("roads_data")
except:
    pass

tmp = open("roads_data\\ .ico","wb+")
tmp.write(base64.b64decode(img))


name='game'+str(random.randint(1000,9999))
root = Tk()
root.title("Roads - "+name)
root.iconbitmap("roads_data\\ .ico")



root.resizable(0,0)
#root['bg']='grey'
root.option_add('*Font', 'Consolas 15')
#root.option_add('*Background', 'ivory')
M=Canvas(root,height=650,width=700)
M.grid(row=1,column=1,rowspan=200)

timet=0
ti=1
run=1
rtot=0
ltot=0
money=100
gem=0
delivered=0
avgspd=0
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
l_route=[]
l_pos=[]
l_color=[]
l_dis=[]
l_color=     ['#B30820','#74A609','#B09400','#461C73','#934c9a','#8C0144','#A34501','#006B9C','#4D88A1','#756387','#541821','#005443','#AD6C95','#5C5504','#7A6C57','#1F9C92']
l_colorlight=['#EA0B2A','#94D40B','#F8D000','#60269E','#643469','#D80169','#FE6B01','#00A0E8','#6FC5E8','#C3A5E1','#792330','#007A61','#F095CE','#827805','#BDA686','#2AD2C5']
l_box=[]
l_ele=[]
l_trnum=[]
l_sch=[]
l_lv=[]
ktot=0
navi=[]
cnnmap=[]
l_ids=[]
msgtime=0
trains=0
pool=[]
l_tag=[]
cities=0

def addknot(i):
    global ktot,cities
    if len(pool[i])<=10:
        return
    rd=random.randint(0, min(10,len(pool[i])))
    x,y=pool[i][0]
    pool[i].pop(rd)#skip! 
    pool[i].pop(0)
    k_x.append(x+random.randint(-10,10))
    k_y.append(y+random.randint(-10,10))
    k_lis.append([])
    k_level.append(1)
    k_occ.append([])
    k_tagids.append(M.create_text(k_x[ktot],k_y[ktot]+15,text=k_lis[ktot],font='Consolas 7'))
    k_full.append(0)
    k_ids.append(M.create_oval(k_x[ktot]-9,k_y[ktot]-9,k_x[ktot]+9,k_y[ktot]+9,width=1,outline='silver'))
    k_txtids.append(M.create_text(k_x[ktot],k_y[ktot],text=ktot,fill='#777777'))
    ktot+=1
    if ktot==35:
        cities+=1
        M.config(width=1400)
    floyed()

def poolini(x):
    global ktot,run,money,pool
    pool=[[],[]]
    x=350
    y=300
    l=1
    for j in range(5):
        for i in range(0,l):
            pool[0].append((x,y))
            pool[1].append((x+700,y))
            x+=60
        for i in range(0,l):
            pool[0].append((x,y))
            pool[1].append((x+700,y))
            y+=60
        l+=1
        for i in range(0,l):
            pool[0].append((x,y))
            pool[1].append((x+700,y))
            x-=60
        for i in range(0,l):
            pool[0].append((x,y))
            pool[1].append((x+700,y))
            y-=60
        l+=1
    
    #print("pool:  ",pool)
    for i in range(3):
        addknot(0)
    
    '''while(1):
        addknot(random.randint(0,cities))
    '''

def addpeople(x):
    global timet
    time.sleep(ti*10)
    while run>0:
        where=random.randint(0,ktot-1)
        towhere=random.randint(0,ktot-1)
        if where!=towhere:
            k_lis[where].append((towhere,timet,where))
            if int(timet/10)%6==4:
                time.sleep(ti*15/ktot**2)
            else:
                time.sleep(ti*20/ktot)

def dist(a,b):
    return((k_x[a]-k_x[b])**2+(k_y[a]-k_y[b])**2)**0.5

def drawlines():
    #print(cnnmap)
    for i in l_ids:
        M.delete(i)
    for i in range(ktot):
        M.itemconfig(k_ids[i],width=1,outline='silver')
        M.itemconfig(k_txtids[i],fill='gray')
    for i in range(ktot):
        for j in range(i):
            num=len(cnnmap[i][j])
            if not num:
                continue
            M.itemconfig(k_ids[i],width=1,outline='black')
            M.itemconfig(k_ids[j],width=1,outline='black')
            M.itemconfig(k_txtids[i],fill='black')
            M.itemconfig(k_txtids[j],fill='black')
            d=((k_y[i]-k_y[j])**2+(k_x[i]-k_x[j])**2)**0.5
            deltx=(k_y[i]-k_y[j])*5/d
            delty=(k_x[j]-k_x[i])*5/d
            cnum=0
            for k in cnnmap[i][j]:
                if l_lv[k]==0:
                    l_ids.append(M.create_line(k_x[i]+deltx*(cnum-(num-1)/2),k_y[i]+delty*(cnum-(num-1)/2),k_x[j]+deltx*(cnum-(num-1)/2),k_y[j]+delty*(cnum-(num-1)/2),fill=l_colorlight[k],width=3))
                else:
                    l_ids.append(M.create_line(k_x[i]+deltx*(cnum-(num-1)/2),k_y[i]+delty*(cnum-(num-1)/2),k_x[j]+deltx*(cnum-(num-1)/2),k_y[j]+delty*(cnum-(num-1)/2),fill=l_colorlight[k],width=3,dash=(2,2,2,3)))
                
                M.lower(l_ids[-1])
                cnum+=1

    

def modline(line,route):
    print(line,"line edited")
    if l_ele[line]!=-1:
        M.delete(l_ele[line])
    l_route[line]=route
    l_pos[line]=[]
    l_dis[line]=[]
    for i in range(0,len(l_route[line])):
        l_route[line][i]=int(l_route[line][i])
        #M.itemconfig(k_ids[l_route[line][i]],outline=l_color[line])
        l_pos[line].append((k_x[l_route[line][i]],k_y[l_route[line][i]]))
    #print(k_x)
    for i in range(0,len(l_route[line])-1):
        #print(i,l_route[line])
        l_dis[line].append(int(((k_x[l_route[line][i]]-k_x[l_route[line][i+1]])**2+(k_y[l_route[line][i]]-k_y[l_route[line][i+1]])**2)**0.5))
    #l_ele[line]=M.create_line(l_pos[line],fill=l_color[line],width=4)
    M.tag_lower(l_ele[line])
    print(l_route,end='~')
    floyed()
    drawlines()

def addtrolley(line,d):
    try:
        level=newtrlev
    except:
        return
    if pay(30*level):
        _thread.start_new_thread( trolley,(line,d,level))
        l_trnum[line]+=1

def tagify(lis):
    txt=""
    if len(lis)<=5:
        for i in lis:
            txt+=str(i[0])+' '
    else:
        for i in lis[:4]:
            txt+=str(i[0])+' '
        txt+='('+str(len(lis))+') '
    return txt[:-1]

        


def trolley(line,dire,level,atk=-1,pas=[-1],pstp=0):
    def printtag():
        M.itemconfig(tag,text=tagify(pas))
    global trains
    if pas==[-1]:
        pas=[]
    trains+=1
    w=0
    if atk==-1:
        if dire:
            atk=l_route[line][-1]
        else:
            atk=l_route[line][0]
        w=1
        x=k_x[atk]
        y=k_y[atk]
        tro=M.create_polygon(x,y,x-6,y-10,x+6,y-10,fill=l_color[line])
        tag=M.create_text(x,y-15,text=pas,fill=l_color[line],font='Consolas 7')
        tagn=M.create_text(x,y-6,text=level,fill='white',font='Consolas 7')
    else:
        x=k_x[atk]
        y=k_y[atk]
        tro=M.create_polygon(x,y,x-6,y-10,x+6,y-10,fill=l_color[line])
        tag=M.create_text(x,y-15,text=pas,fill=l_color[line],font='Consolas 7')
        tagn=M.create_text(x,y-6,text=level,fill='white',font='Consolas 7')
        time.sleep(ti*random.random()+pstp)
    
    if w:
        while timet<l_sch[line][dire]:
            time.sleep(ti*1)
            if run<=0:
                s_train.append([line,dire,level,atk,pas,tmexceed])
                trains-=1
                return
        l_sch[line][dire]=timet+10
    #time.sleep(ti*random.randint(3,15))
    while True:
        if run<=0:
            s_train.append([line,dire,level,atk,pas,tmexceed])
            trains-=1
            if line in k_occ[atk]:
                k_occ[atk].remove(line)
            return
        
        while line in k_occ[atk] or len(k_occ[atk])>=k_level[atk]:
            time.sleep(ti*1)
            if run<=0:
                s_train.append([line,dire,level,atk,pas,tmexceed])
                trains-=1
                return
        
        k_occ[atk].append(line)
        #M.itemconfig(k_ids[atk],outline=l_color[line])
        i=0
        while i<len(pas):
            if line*2+dire not in navi[atk][pas[i][0]]:
                k_lis[atk].append(pas[i])
                pas.pop(i)
                printtag()
                #M.itemconfig(k_tagids[atk],text=k_lis[atk][0:min(6,len(k_lis[atk]))])
                time.sleep(ti*0.5)
                i-=1
            i+=1
        i=0
        while i <len(k_lis[atk]) and len(pas)<level*6:
            if line*2+dire in navi[atk][k_lis[atk][i][0]]:
                pas.append(k_lis[atk][i])
                k_lis[atk].pop(i)
                printtag()
                #M.itemconfig(k_tagids[atk],text=k_lis[atk][0:min(6,len(k_lis[atk]))])
                time.sleep(ti*0.5)
                i-=1
            i+=1
        #print(pas)
        if run<=0:
            s_train.append([line,dire,level,atk,pas,tmexceed])
            trains-=1
            return
        time.sleep(ti*1/level)
        if line in k_occ[atk]:
            k_occ[atk].remove(line)
        try:
            at=l_route[line].index(atk)
        except:
            break
        if (at==0 and dire==1) or (at==len(l_route[line])-1 and dire==0):
            break
        else:
            natk=l_route[line][at+1-dire*2]
        #dash=M.create_line(k_x[atk],k_y[atk],k_x[natk],k_y[natk],fill=l_color[line])
        #print(at,dire)
        dist=int(l_dis[line][at-dire])
        i=0
        time.sleep(ti*l_lv[line]*3)
        while i < dist:
            d=min(0.7+1.3*l_lv[line],0.05*i+0.1,0.05*(dist-i)+0.2)
            M.move(tro,(k_x[natk]-x)/dist*d,(k_y[natk]-y)/dist*d)
            M.move(tag,(k_x[natk]-x)/dist*d,(k_y[natk]-y)/dist*d)
            M.move(tagn,(k_x[natk]-x)/dist*d,(k_y[natk]-y)/dist*d)
            time.sleep(ti*0.02)
            i+=d
        #M.delete(dash)
        x=(k_x[natk])
        y=(k_y[natk])
        time.sleep(ti*0.5)
        atk=natk
    while len(pas):
        k_lis[atk].append(pas[0])
        pas.pop(0)
        printtag()
        #M.itemconfig(k_tagids[atk],text=k_lis[atk][0:min(6,len(k_lis[atk]))])
        time.sleep(ti*0.5)
    M.delete(tro)
    M.delete(tag)
    M.delete(tagn)
    trains-=1
    if run>0:
        trolley(line,1-dire,level)

def floyed():
    maps=[]
    finder=[]
    global navi,cnnmap
    cnnmap=[]
    for i in range(ktot+1):
        maps.append([])
        finder.append([])
        cnnmap.append([])
        for j in range(ktot+1):
            if i==j:
                maps[i].append(0)
            else:
                maps[i].append(10000000000)
            finder[i].append(set())
            cnnmap[i].append(set())
    for i in range(ltot):
        for j in range(len(l_dis[i])):
            #print(i,j,l_route[i][j],l_route[i][j+1],maps[l_route[i][j]][l_route[i][j+1]])
            maps[l_route[i][j]][l_route[i][j+1]]=l_dis[i][j]/(l_lv[i]+1)+10+30*l_lv[i]
            maps[l_route[i][j+1]][l_route[i][j]]=l_dis[i][j]/(l_lv[i]+1)+10+30*l_lv[i]
            finder[l_route[i][j]][l_route[i][j+1]].add(i*2)            
            finder[l_route[i][j+1]][l_route[i][j]].add(i*2+1)
            cnnmap[l_route[i][j]][l_route[i][j+1]].add(i)
            cnnmap[l_route[i][j+1]][l_route[i][j]].add(i)
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


def addline(lv=0):
    global ltot,l_tag,newtrlev,money
    if ltot>=len(l_color):
        return 0
    if not pay(50*ltot+30*newtrlev,lv*5):
        return 0
    #l_box.append(Entry(root,width=30,bd=0,highlightthickness=4,highlightbackground=l_color[ltot]))
    #l_box[ltot].grid(row=ltot+10,column=2)
    l_route.append([])
    l_ele.append(-1)
    l_dis.append([])
    l_pos.append([])
    l_trnum.append(0)
    l_sch.append([0,0])
    l_lv.append(lv)
    l_tag.append(Label(root,text='line '+str(ltot),foreground=l_color[ltot]))
    l_tag[-1].grid(row=ltot+100,column=2)
    #Button(root,bg='snow',text="edit",width=10,command=lambda:editline(miltot),bd=0).grid(row=ltot+10,column=3)
    #Button(root,bg='snow',text="trolley(Down)",width=15,command=lambda:addtrolley(miltot,0),bd=0).grid(row=ltot+10,column=4)
    #Button(root,bg='snow',text="trolley(Up)",width=15,command=lambda:addtrolley(miltot,1),bd=0).grid(row=ltot+10,column=5,columnspan=2)
    ltot+=1
    return 1

def updknot(num):
    if pay(50*k_level[num]):
        k_level[num]+=1
        M.coords(k_ids[num],k_x[num]-7-k_level[num]*2,k_y[num]-7-k_level[num]*2,k_x[num]+7+k_level[num]*2,k_y[num]+7+k_level[num]*2) #resize
        M.tag_raise(k_tagids[num])

'''
def updtr():
    global newtrlev
    if pay(newtrlev*100):
        newtrlev+=1
        updtrb.config(text='🚊 '+str(newtrlev))
'''


def pay(price,gems=0):
    global money,gem
    if money >= price and gem>=gems:
        money-=price
        gem-=gems
        if gems:
            message('paid money '+str(price)+' and gem '+str(gems),'normal')
        else:
            message('paid '+str(price),'normal')
        return True
    else:
        if money< price:
            message('not enough money '+str(money-price),'warning')
        else:
            message('not enough gems '+str(gem-gems),'normal')
        return False

def changespeed():
    global ti
    if ti==0.5:
        ti=0.25
        spb.config(text='x4')
    elif ti==1:
        ti=0.5
        spb.config(text='x2')
    elif ti==0.25:
        ti=2
        spb.config(text='x0.5')
    elif ti==2:
        ti=1
        spb.config(text='x1')

def message(text,tpe='normal'):
    global msgtime
    if tpe=='warning':
        messageboxx.config(foreground='red')
    elif tpe=='special':
        messageboxx.config(foreground='#b16584')
    elif tpe=='normal':
        messageboxx.config(foreground='black')
    messageboxx.config(text=text)
    msgtime=timet

def exe(x):
    global newtrlev,money
    if not run>0:
        messagebox.showerror("","Restart the program to perform new tasks.")
        return
    inp=(cmdbox.get()).split(' ')
    try:
        if inp[0]=='mod':
            lin=int(inp[1])
            rt=l_route[lin]
            #print('r=',rt)
            if inp[2]=='r':
                rt=inp[3:]
            elif inp[2]=='e':
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
            tmpf=[]            
            isedit=1
            for i in range(len(rt)):
                rt[i]=int(rt[i])
            for i in rt :
                if i in tmpf:
                    message('invalid route','warning')
                    isedit=0
                    break
                tmpf.append(i)
            if isedit:
                modline(lin,rt)
                message('line '+str(lin)+' modified','normal')
        elif inp[0]=='new':
            tmpf=[]
            isedit=1
            for i in inp[1:] :
                if i in tmpf:
                    message('invalid route','warning')
                    isedit=0
                    break
                tmpf.append(i)
            if isedit:        
                if addline():
                    modline(ltot-1,inp[1:])
                    money+=30*newtrlev
                    addtrolley(ltot-1,0)
                    message('new line '+str(ltot-1),'normal')
        elif inp[0]=='*new':
            tmpf=[]
            isedit=1
            for i in inp[1:] :
                if i in tmpf:
                    message('invalid route','warning')
                    isedit=0
                    break
                tmpf.append(i)
            if isedit:        
                if addline(1):
                    modline(ltot-1,inp[1:])
                    money+=30*newtrlev
                    addtrolley(ltot-1,0)
                    message('new highspeed line '+str(ltot-1),'normal')
        elif inp[0]=='adt':
            if len(inp)==3:
                newtrlev=int(inp[2])
                updtrb.config(text='🚊 '+str(newtrlev))
            lin=int(inp[1])
            if l_sch[lin][0]>l_sch[lin][1]:
                addtrolley(lin,1)
            else:
                addtrolley(lin,0)
            #message('added train to line '+str(lin),'normal')
        elif inp[0]=='upd':
            updknot(int(inp[1]))
        elif inp[0]=='*upd':
            k=int(inp[1])
            if pay(0,1):
                k_lis[k]=[]
                k_full[k]=-15
                money+=50*k_level[k]
                updknot(k)
        elif inp[0]=='*pro':
            if pay(0,int(ktot/20)+1):
                for i in range(ktot):
                    k_full[i]=-10
        elif inp[0]=='load':        
            try:
                global name
                name=inp[1]
                path='roads_data\\'+inp[1]+'.rds'
                message('loading '+path)
                if load(path):
                    name=inp[1]
                    path=inp[1]+'.rds'
                    root.title("Roads - "+name)
                    message('loaded '+path)
            except:
                message('failed','warning')
        elif inp[0]=='rename':
            name=inp[1]
            root.title("Roads - "+name)
        else:
            message('invalid syntax','warning')
    except:
        message('invalid syntax','warning')
    cmdbox.selection_range(0, END)
    
    

_thread.start_new_thread( poolini, (1,) )
_thread.start_new_thread( addpeople, (1,) )
tk_delivered=StringVar()
tk_avgspd=StringVar()
tk_money=StringVar()
tk_gem=StringVar()
tk_tm=StringVar()
tk_delivered.set('🚹'+str(delivered))
tk_avgspd.set('⏱️'+str(int(avgspd)))
tk_money.set('🪙'+str(money))
tk_gem.set('💎'+str(gem))
Label(root,textvariable=tk_tm).grid(row=1,column=2,padx=7)
Label(root,textvariable=tk_delivered).grid(row=2,column=2)
Label(root,textvariable=tk_avgspd).grid(row=3,column=2)
Label(root,textvariable=tk_money,foreground='#ddaa00').grid(row=4,column=2)
Label(root,textvariable=tk_gem,foreground='#00ddcc').grid(row=5,column=2)
#Button(root,text='upgrade station:    ',command=updknot,width=20,bd=0).grid(row=2,column=3,columnspan=2)
#updwk=Entry(root,width=3,bd=0,highlightthickness=1,highlightbackground='gray')
#updwk.grid(row=2,column=4,stick='E',padx=25)
updtrb=Label(root,text='🚊 1')
updtrb.grid(row=6,column=2)
#newtrlevel=Entry(root,width=3,bd=0,highlightthickness=1,highlightbackground='gray')
#newtrlevel.grid(row=2,column=2,stick='E',padx=40)
#newtrlevel.insert(0, '1')
#Button(root,text="addline",width=10,command=addline,bd=0).grid(row=2,column=5)
spb=Button(root,command=changespeed,text='x1')
spb.grid(row=7,column=2)

cmdbox=Entry(root,justify='center')
cmdbox.grid(row=201,column=1,sticky='WE',columnspan=20)
cmdbox.bind('<Return>',exe)
messageboxx=Label(root)
messageboxx.grid(row=202,column=1,columnspan=20)
#Button(root,text="tx_确定",width=20,command=lambda:editline(0),bd=0).pack()
#Button=(root,text="edit",command=lambda:editline(1)).pack()

wcolor=['#FFFFFF','#FFAAAA','#FF9999','#FF8888','#FF7777','#FF6666','#FF5555','#FF4444','#FF3333','#FF2222','#FF0000']
def knotchek(num):
    global run,money,delivered,avgspd,gem
    i=0
    while i<len(k_lis[num]):
        if k_lis[num][i][0]==num:
            delivered+=1
            money+=2
            spd=dist(num,k_lis[num][i][2])/(timet-k_lis[num][i][1])*10
            avgspd=avgspd*0.9+spd*0.1
            print(spd)
            k_lis[num].pop(i)
            if random.randint(0,500)==0:
                gem+=1
            i-=1
        i+=1
    if k_full[num]<0:
        k_full[num]+=0.25
        M.itemconfig(k_ids[num],fill='#ccffee')
        return
    if len(k_lis[num])>k_level[num]*8:
        if k_full[num]>=10:
            run=-1
            M.itemconfig(k_txtids[num],text='!',font='Consolas 15 bold',fill='white')
            message('game over')
        else:
            k_full[num]+=0.1/ti/k_level[num]
    else:
        k_full[num]=0
    M.itemconfig(k_ids[num],fill=wcolor[int(k_full[num])])

def timefy(sec):
    sec=int(sec)
    h=str(sec//3600)
    m=str((sec//60)%60)
    s=str(sec%60)
    if len(h)==1:
        h='0'+h
    if len(m)==1:
        m='0'+m
    if len(s)==1:
        s='0'+s
    return h+':'+m+':'+s

def pro():
    global timet,money
    while run>0:
        for i in range(0,ktot):
            knotchek(i)
            M.itemconfig(k_tagids[i],text=tagify(k_lis[i]),font='Consolas 7')
       
        time.sleep(0.25/ti)
_thread.start_new_thread( pro, () )


def timetick():
    global timet,money
    while run>0:
        root.update()
        tk_delivered.set('🚹'+str(delivered))
        tk_avgspd.set('⏱️'+str(int(avgspd)))
        tk_money.set('🪙'+str(money))
        tk_gem.set('💎'+str(gem))
        tk_tm.set(timefy(timet))
        time.sleep(0.25)
        timet+=0.25/ti
        #print(timet,timet%1,0.25/ti)
        if timet%1<0.25/ti:
            t=int(timet)
            if t%60==35:
                message('rush hour!','normal')
            elif t%60==50:
                message('rush hour ends','normal')
            elif t%60==0:
                addknot(random.randint(0,cities))
                money+=10

        if timet-msgtime>3:
            message('')

_thread.start_new_thread( timetick, () )

s_train=[]

def Hash(string):
    s=list(string)
    hv=0
    bs=1
    for i in range(len(s)):
        if s[i]==' ':
            continue
        hv+=ord(s[i])*bs
        bs*=9991
        bs%=9999199999999991
        hv%=9999199999999991
    #print(len(s),hv)
    return hv

tmexceed=0
def save(x):
    global run,ti,s_train,tmexceed
    if run>0:
        run=0
        ti=0.1
        while trains:
            #print(trains)
            time.sleep(0.25*ti)
            tmexceed+=0.25
        #print(str(s_train))
    else:
        if run==-1 or messagebox.askokcancel("Warning","Force quit will delete all trains!"):
            s_train=[]
        else:
            return
    for i in range(len(k_occ)):
        k_occ[i].clear()
    with open('roads_data\\'+name+'.rds','w') as f:
        data={'trains':s_train,'n':[timet,rtot,ltot,money,gem,delivered,avgspd,newtrlev,ktot],'l':[k_lis,k_x,k_y,k_level,k_full,l_route,l_pos,l_color,l_box,l_ele,l_trnum,l_sch,l_dis,l_lv,pool]}
        txt=str(data)
        code=str(Hash(txt))
        f.write(txt+'\n'+code)
    root.destroy()


def load(path):
    global run,timet,rtot,ltot,money,gem,delivered,avgspd,newtrlev,ktot,k_lis,k_x,k_y,k_level,k_full,k_occ,l_route,l_pos,l_color,l_box,l_ele,l_trnum,l_sch,l_dis,l_lv,pool,k_ids,k_tagids,k_txtids,l_tag,cities
    with open(path,'r') as f:
        txt=f.readline()
        code=int(f.readline())
        if code!=Hash(txt[0:-1]):
            message('fake file','warning')
            return 0
        
    data=eval(txt)
    timet,rtot,ltot,money,gem,delivered,avgspd,newtrlev,ktot=data['n']
    k_lis,k_x,k_y,k_level,k_full,l_route,l_pos,l_color,l_box,l_ele,l_trnum,l_sch,l_dis,l_lv,pool=data['l']
    if ktot>=35:
        cities=2
        M.config(width=1400)
    k_occ=[]
    for i in range(ktot):
        k_occ.append([])

    for itm in k_ids:
        M.delete(itm)
    for itm in k_tagids:
        M.delete(itm)
    for itm in k_txtids:
        M.delete(itm)
    #print('@')
    k_txtids=[]
    k_ids=[]
    k_tagids=[]

    #run=1 #revival

    for itm in l_tag:
        itm.destroy()
    l_tag=[]
    for i in range(ltot):
        l_tag.append(Label(root,text='line '+str(i),foreground=l_colorlight[i]))
        l_tag[-1].grid(row=i+100,column=2)

    for itm in range(ktot):
        k_ids.append(M.create_oval(k_x[itm]-7-k_level[itm]*2,k_y[itm]-7-k_level[itm]*2,k_x[itm]+7+k_level[itm]*2,k_y[itm]+7+k_level[itm]*2,width=1,outline='silver'))
        k_txtids.append(M.create_text(k_x[itm],k_y[itm],text=itm,fill='#777777'))
        k_tagids.append(M.create_text(k_x[itm],k_y[itm]+15,text=k_lis[itm],font='Consolas 7'))
    updtrb.config(text='🚊 '+str(newtrlev))
    floyed()
    drawlines()
    #time.sleep(3*ti)
    for itm in data['trains']:
        _thread.start_new_thread(trolley,(itm[0],itm[1],itm[2],itm[3],itm[4],itm[5]))
    return 1
    
        
message('Roads version 1.4 by Mirpri, 2024','special')

def on_closing():
    _thread.start_new_thread( save, (1,) )

root.protocol('WM_DELETE_WINDOW', on_closing)
mainloop()

#python -m Pyinstaller roads-1.4.py -w -F -i metro.ico