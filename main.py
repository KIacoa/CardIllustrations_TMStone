#!/usr/bin/env python
import tkinter as tk
from tkinter import StringVar, ttk, messagebox
import os
import sqlite3
from tkinter.constants import BOTH, BOTTOM, CENTER, DISABLED, X, Y
from tkinter.font import BOLD
from PIL import Image,ImageTk
import math
import build_card_detail as bcd
from functools import cmp_to_key

win=tk.Tk()
win.title("荼曼石圣灵图鉴")
win.geometry("600x450")
win.resizable(0,0)
page=1
page_sum=1
quality={"基础":"q001","普通":"q002","稀有":"q003","史诗":"q004","传说":"q005"}
color={"q001":"white","q002":"white","q003":"deepskyblue","q004":"darkviolet","q005":"orange"}#用于翻译编号
race={"r001":"人族","r002":"兽族","r003":"机械","r004":"亚人族","r005":"巨人族",
    "r006":"无","r007":"植物","r008":"不死族","r009":"怪兽","r010":"恶魔"}
def build_page():
    '''
    构建一遍页面
    利用card列表和page页码定位到该页面上的10张卡牌
    将页面控件destroy，并重新建立
    '''
    global page
    global page_sum
    conn=sqlite3.connect("./tmstone.db")#链接数据库
    cur=conn.cursor()
    for i in range(10):#初始化最开始的页面卡牌信息
        index=i+10*(page-1)
        if index>=len(card):
            index=index%len(card)
        card_type=card[index][0]+card[index][1]#检查卡牌类型
        if(card_type=="mc"):
            select_card="select * from main_hero where id = '"+card[index]+"'"
            query_card=cur.execute(select_card)
            for j in query_card:
                img=j[8]
                card_name[i].set(j[1])
                b_color="firebrick"
        elif(card_type=="es"):
            select_card="select * from exclusive_servant where id = '"+card[index]+"'"
            query_card=cur.execute(select_card)
            for j in query_card:
                img=j[9]
                card_name[i].set(j[1])
                b_color="lightcoral"
        elif(card_type=="s0"):
            select_card="select * from servant where id = '"+card[index]+"'"
            query_card=cur.execute(select_card)
            for j in query_card:
                img=j[8]
                card_name[i].set(j[1])
                b_color=color[j[7]]
        elif(card_type=="m0"):
            select_card="select * from magic where id = '"+card[index]+"'"
            query_card=cur.execute(select_card)
            for j in query_card:
                img=j[3]
                card_name[i].set(j[1])
                b_color=color[j[2]]
        elif(card_type=="t0"):
            select_card="select * from trap where id = '"+card[index]+"'"
            query_card=cur.execute(select_card)
            for j in query_card:
                img=j[3]
                card_name[i].set(j[1])
                b_color=color[j[2]]
        elif(card_type=="e0"):
            select_card="select * from equipment where id = '"+card[index]+"'"
            query_card=cur.execute(select_card)
            for j in query_card:
                img=j[5]
                card_name[i].set(j[1])
                b_color=color[j[4]]
        frame_card_name[i].config(bg=b_color)
        label_card_name[i].config(bg=b_color)
        card_img[i]=get_image(img,106,126)
        button_card[i].destroy()
        button_card[i]=tk.Button(frame_card_img[i],image=card_img[i],command=lambda num=index:onClickCard(num))
        button_card[i].place(relx=0.5,rely=0.5,anchor=CENTER)
    page_sum=math.ceil(1.0*len(card)/10)
    page_foot=str(page)+"/"+str(page_sum)
    str_switch_sum.set(page_foot)
    conn.close()

def onClickSwitch():
    '''
    换页按钮绑定事件
    点击后，换页
    本质上没有改变card列表，（其实什么都没改）
    仅仅是让page+1，改变index
    index=i+10*（page-1）
    然后重新摧毁所有的空间，再重新按上新的。
    '''
    global page
    global page_sum
    page+=1
    if page>page_sum:
        page=1
    build_page()
    
def on_modify_next(event):
    '''
    键盘事件，事件绑定在win主窗口
    只要按下左右键，就会完成换页操作
    '''
    if event.keycode==39:
        onClickSwitch()
    elif event.keycode==37:
        global page
        global page_sum
        page-=1
        if page<1:
            page=page_sum
        build_page()

def onClickScreen():
    '''
    本质上的作用是改变card列表里的卡牌内容id和sum
    page_sum的改变，是因为card列表的长度变化
    page_sum=math.ceil(1.0*len(card)/10)
    其他看起来是他做的，实际上不是的副工作是
    将page改回1，然后再把页面重新建立一遍
    '''
    global page
    global card
    #获取筛选条件
    card_quality=combobox_screen_quality.get()
    card_type=combobox_screen_type.get()
    if (card_type=="主角色" or card_type=="专属仆从")and(card_quality!="全部"):
        messagebox.showinfo('提示','主角色和专属仆从没有卡牌品质属性！')
    else:
        conn=sqlite3.connect("./tmstone.db")#链接数据库
        cur=conn.cursor()
        page=1
        if card_type=="全部" and card_quality=="全部":
            select_all_card="select * from card"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                card.append(i[1])    
        elif card_type=="全部" and card_quality!="全部":
            select_all_card="select * from card"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            temp=list()#存储所有卡牌内容id
            card=list()#初始化card
            for i in s:#执行存储卡牌内容id操作
                temp.append(i[1])  
            for i in temp:#执行存储卡牌内容id操作
                card_type=i[0]+i[1]#检查卡牌类型
                f=False#用于记录该卡牌是否符合要求，false为不符合要求，不插入到card列表
                if(card_type=="s0"):
                    select_card="select * from servant where id = '"+i+"'"
                    query_card=cur.execute(select_card)
                    for j in query_card:
                        if j[7]==quality[card_quality]:
                            f=True
                elif(card_type=="m0"):
                    select_card="select * from magic where id = '"+i+"'"
                    query_card=cur.execute(select_card)
                    for j in query_card:
                        if j[2]==quality[card_quality]:
                            f=True
                elif(card_type=="t0"):
                    select_card="select * from trap where id = '"+i+"'"
                    query_card=cur.execute(select_card)
                    for j in query_card:
                        if j[2]==quality[card_quality]:
                            f=True
                elif(card_type=="e0"):
                    select_card="select * from equipment where id = '"+i+"'"
                    query_card=cur.execute(select_card)
                    for j in query_card:
                        if j[4]==quality[card_quality]:
                            f=True
                else:
                    continue
                if f==True:
                    card.append(i)
        elif card_type=="主角色" and card_quality=="全部":
            select_all_card="select * from main_hero"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                card.append(i[0])   
        elif card_type=="专属仆从" and card_quality=="全部": 
            select_all_card="select * from exclusive_servant"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                card.append(i[0])   
        elif card_type=="仆从" and card_quality=="全部":
            select_all_card="select * from servant"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                card.append(i[0])    
        elif card_type=="仆从" and card_quality!="全部":
            select_all_card="select * from servant"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                if i[7]==quality[card_quality]:
                    card.append(i[0]) 
        elif card_type=="法术" and card_quality=="全部":
            select_all_card="select * from magic"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                card.append(i[0])
        elif card_type=="法术" and card_quality!="全部":
            select_all_card="select * from magic"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                if i[2]==quality[card_quality]:
                    card.append(i[0]) 
        elif card_type=="陷阱" and card_quality=="全部":
            select_all_card="select * from trap"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                card.append(i[0])
        elif card_type=="陷阱" and card_quality!="全部":
            select_all_card="select * from trap"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                if i[2]==quality[card_quality]:
                    card.append(i[0]) 
        elif card_type=="装备" and card_quality=="全部":
            select_all_card="select * from equipment"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                card.append(i[0])
        elif card_type=="装备" and card_quality!="全部":
            select_all_card="select * from equipment"#查找所有卡牌的id
            s=cur.execute(select_all_card)
            card=list()#存储所有卡牌内容id
            for i in s:#执行存储卡牌内容id操作
                if i[4]==quality[card_quality]:
                    card.append(i[0]) 
        build_page()
        conn.close()

def cmp(a,b):
    if a[1]<b[1]:
        return 1
    else:
        return -1

def onClickCard(index):
    '''
    点击后，将card中的索引传来，以此利用card列表获取卡牌内容id
    再根据内容id区分类别，调用函数
    函数的一个参数为card中的索引
    '''
    conn=sqlite3.connect("./tmstone.db")#链接数据库
    cur=conn.cursor()
    if index>=len(card):
        messagebox.showinfo('提示','未找到您查看的卡牌！')
        return
    card_id=card[index]
    card_type=card_id[0]+card_id[1]
    #根据类型调用创建卡牌详情页的函数
    if(card_type=="mc"):
        select_card="select * from main_hero where id = '"+card[index]+"'"
        query_card=cur.execute(select_card)
        for j in query_card:
            bcd.card_mc_detail(j[0],j[1],j[8],j[2],j[3],j[4],j[5],j[6],j[7])
    elif(card_type=="es"):
        select_card="select * from exclusive_servant where id = '"+card[index]+"'"
        query_card=cur.execute(select_card)
        for j in query_card:
            bcd.card_es_detail(j[0],j[1],j[9],j[7],j[2],j[3],j[4],j[5],j[6],j[8])
    elif(card_type=="s0"):
        select_card="select * from servant where id = '"+card[index]+"'"
        query_card=cur.execute(select_card)
        for j in query_card:
            bcd.card_s_detail(j[0],j[1],j[8],j[2],j[3],j[4],j[5],j[6],j[7])
    elif(card_type=="m0"):
        select_card="select * from magic where id = '"+card[index]+"'"
        query_card=cur.execute(select_card)
        for j in query_card:
            bcd.card_mt_detail(j[0],j[1],j[3],j[2])
    elif(card_type=="t0"):
        select_card="select * from trap where id = '"+card[index]+"'"
        query_card=cur.execute(select_card)
        for j in query_card:
            bcd.card_mt_detail(j[0],j[1],j[3],j[2])
    elif(card_type=="e0"):
        select_card="select * from equipment where id = '"+card[index]+"'"
        query_card=cur.execute(select_card)
        for j in query_card:
            bcd.card_e_detail(j[0],j[1],j[5],j[2],j[3],j[4])
    conn.close()

def on_modify(event):
    conn=sqlite3.connect("./tmstone.db")#链接数据库
    cur=conn.cursor()
    global msg
    msg = event.widget.get()
    select_all_card="select * from card"
    s=cur.execute(select_all_card)
    discard=list()
    temp=list()
    new_value=list()
    for i in s:
        temp.append(i[1])  
    for i in temp:#执行存储卡牌内容id操作
        card_type=i[0]+i[1]#检查卡牌类型
        f=False#用于记录该卡牌是否符合要求，false为不符合要求，不插入到card列表
        if(card_type=="mc"):
            select_card="select * from main_hero where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((j[1],cnt))
        elif(card_type=="es"):
            select_card="select * from exclusive_servant where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((j[1],cnt))
        elif(card_type=="s0"):
            select_card="select * from servant where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((j[1],cnt))
        elif(card_type=="m0"):
            select_card="select * from magic where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((j[1],cnt))
        elif(card_type=="t0"):
            select_card="select * from trap where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((j[1],cnt))
        elif(card_type=="e0"):
            select_card="select * from equipment where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((j[1],cnt))
        else:
            continue
    discard.sort(key=cmp_to_key(cmp))
    for i in discard:
        new_value.append(i[0])
    combobox_search["value"]=new_value
    conn.close()

def onClickSearch():
    conn=sqlite3.connect("./tmstone.db")#链接数据库
    cur=conn.cursor()
    global msg
    global card
    msg=combobox_search.get()#获取搜索框的值
    select_all_card="select * from card"
    s=cur.execute(select_all_card)
    discard=list()
    temp=list()
    for i in s:
        temp.append(i[1])  
    for i in temp:#执行存储卡牌内容id操作
        card_type=i[0]+i[1]#检查卡牌类型
        #遍历卡牌名称，每当出现搜索框中的字，权值+1
        if(card_type=="mc"):
            select_card="select * from main_hero where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((i,cnt))
        elif(card_type=="es"):
            select_card="select * from exclusive_servant where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((i,cnt))
        elif(card_type=="s0"):
            select_card="select * from servant where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((i,cnt))
        elif(card_type=="m0"):
            select_card="select * from magic where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((i,cnt))
        elif(card_type=="t0"):
            select_card="select * from trap where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((i,cnt))
        elif(card_type=="e0"):
            select_card="select * from equipment where id = '"+i+"'"
            query_card=cur.execute(select_card)
            cnt=0
            for j in query_card:
                for k in msg:
                    cnt+=j[1].count(k)
            if cnt:
                discard.append((i,cnt))
        else:
            continue
    if len(discard)==0:#等于零，说明没有搜索到卡牌
        messagebox.showinfo('提示','没有搜索到任何卡牌！')
        return
    discard.sort(key=cmp_to_key(cmp))#将未排序的卡牌，按照权值逆序排列
    card=list()#初始化卡牌列表
    for i in discard:
        card.append(i[0])
    build_page()
    conn.close()

#win.attributes("-transparentcolor","red")#设置所有的白色变透明
#创建背景层
def get_image(filename,width,height):
    '''
    获取图片，第一个参数为图片路径
    后两个为图片自动缩放的宽和高
    '''
    im = Image.open(filename).resize((width,height))#打开图片并自动缩放到width，height
    return ImageTk.PhotoImage(im)

#创建背景画布
canvas_background=tk.Canvas(win,width=600,height=450)
im_root=get_image('background.jpg',1200,900)
canvas_background.create_image(0,0,image=im_root)#绘制背景图
canvas_background.create_line(30, 40, 570, 40, fill = "black")#绘制标题图鉴下的直线从(30,40)到(570,40)
canvas_background.create_line(269, 0, 269, 40, fill = "black")
canvas_background.create_line(331, 0, 331, 40, fill = "black")
canvas_background.create_line(269, 0, 331, 0, fill = "black")
canvas_background.pack()
#创建容器用于布局
frame_title=tk.Frame(width=60,height=39,background="white")
frame_search=tk.Frame(width=300,height=40,background="#D59BB6")
frame_screen=tk.Frame(width=200,height=40)
frame_switch=tk.Frame(width=600,height=40)
#创建标题“图鉴”
label_title=tk.Label(frame_title,text="图鉴",font=("黑体",20),justify=CENTER,pady=5,background="white")
#创建搜索框search
str_search=tk.StringVar()#用于获取search文本框中的文字
#entry_search=tk.Entry(frame_search,width=20,textvariable=str_search,highlightcolor='#00BFFF', highlightthickness=1,background="white")
combobox_search=ttk.Combobox(frame_search,width=20,textvariable=str_search,background="white")
#entry_search_text="search"#添加搜索框的默认值
combobox_search.insert(0,"search")#添加搜索默认值
msg="search"
combobox_search.bind('<KeyRelease>',on_modify)
combobox_search.focus_set()
#entry_search.insert(0,entry_search_text)
#创建search搜索框的按钮
button_search=tk.Button(frame_search,text="search",font=('黑体',10),width=10,background="#00BFFF",relief="flat",command=onClickSearch)
#创建筛选用下拉菜单
str_screen_type=tk.StringVar()#用于获取combobox类型筛选出来的值
combobox_screen_type=ttk.Combobox(frame_screen,width=7,textvariable=str_screen_type,state="readonly")
combobox_screen_type["value"]=("全部","主角色","专属仆从","仆从","法术","装备","陷阱")#设置类型筛选菜单的可选值
combobox_screen_type.current(0)#设置初始值为第一个元素
str_screen_quality=tk.StringVar()#用于获取combobox品质筛选出来的值
combobox_screen_quality=ttk.Combobox(frame_screen,width=7,textvariable=str_screen_quality,state="readonly")
combobox_screen_quality["value"]=("全部","基础","普通","稀有","史诗","传说")#设置品质筛选菜单的可选值
combobox_screen_quality.current(0)#设置初始值为第一个元素
#创建下拉菜单的按钮
button_combobox=tk.Button(frame_screen,text="screen",font=("黑体",10),background="#00BFFF",relief="flat",command=onClickScreen,activebackground="#1E90FF")
#创建页脚换页内容
str_switch_sum=tk.StringVar()#页码提示
str_switch_sum.set(str(page)+"/"+str(page_sum))
label_switch=tk.Label(frame_switch,textvariable=str_switch_sum,font=("黑体",10))
button_switch=tk.Button(frame_switch,text="next",font=("黑体",10),command=onClickSwitch,relief="ridge",borderwidth=1)#换页按钮
win.bind('<KeyRelease>',on_modify_next)
win.focus_set()
#利用place给各个容器布局
frame_title.place(x=270,y=1)
label_title.place(relx=0.5,rely=0.5,anchor=CENTER)
frame_search.place(x=27,y=50)
#entry_search.grid(row=0,column=0)
combobox_search.grid(row=0,column=0)
button_search.grid(row=0,column=1)
frame_screen.place(x=370,y=50)
combobox_screen_type.grid(row=0,column=0)
combobox_screen_quality.grid(row=0,column=1)
button_combobox.grid(row=0,column=2)
frame_switch.place(x=0,y=400)
label_switch.place(relx=0.87,rely=0.5,anchor=CENTER)
button_switch.place(relx=0.93,rely=0.5,anchor=CENTER)

#600-50=550 110  25 106 5  h:125 100 250  400
#创建卡牌图鉴主体，卡牌板块
frame_card_img=list()
frame_card_name=list()
label_card_name=list()
card_name=[StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar(),StringVar()]
for i in range(10):
    card_name[i].set("a")
    frame_card_img.append(tk.Frame(width=106,height=125,bg="black"))
    frame_card_name.append(tk.Frame(width=106,height=15,bg="white"))
    label_card_name.append(tk.Label(frame_card_name[i],textvariable=card_name[i],font=("Courier",10),justify=CENTER,background="white"))#,textvariable=card_name[i]

for i in range(5):
    frame_card_img[i].place(x=25+111*i,y=100)   
    frame_card_name[i].place(x=25+111*i,y=225)
    label_card_name[i].place(relx=0.5,rely=0.5,anchor=CENTER)

for i in range(5):
    frame_card_img[i+5].place(x=25+111*i,y=250)
    frame_card_name[i+5].place(x=25+111*i,y=375)
    label_card_name[i+5].place(relx=0.5,rely=0.5,anchor=CENTER)

conn=sqlite3.connect("./tmstone.db")#链接数据库
cur=conn.cursor()
select_all_card="select * from card"#查找所有卡牌的id
s=cur.execute(select_all_card)
card=list()#存储所有卡牌内容id
button_card=list()#存储每页所有卡牌按钮
for i in range(10):#初始化卡牌按钮
    button_card.append(tk.Button(frame_card_img[i]))

for i in s:#执行存储卡牌内容id操作
    card.append(i[1])

card_img=list()#存储每页所有卡牌的图片信息
img="background.jpg"
for i in range(10):#初始化card_img数组，让其长度变为10
    card_img.append(get_image(img,106,126))
    
build_page()
conn.close()
win.mainloop()