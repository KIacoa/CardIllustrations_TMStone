
import tkinter as tk
import os
import sqlite3
from tkinter.constants import BOTH, BOTTOM, CENTER, DISABLED, X, Y
from PIL import Image,ImageTk
import math
color={"q001":"white","q002":"white","q003":"deepskyblue","q004":"darkviolet","q005":"orange"}#用于翻译编号
quality={"q001":"基础","q002":"普通","q003":"稀有","q004":"史诗","q005":"传说"}#用于翻译编号
race={"r001":"人族","r002":"兽族","r003":"机械","r004":"亚人族","r005":"巨人族",#用于翻译编号
    "r006":"无","r007":"植物","r008":"不死族","r009":"怪兽","r010":"恶魔"}
def get_image(filename,width,height):
    '''
    获取图片，第一个参数为图片路径
    后两个为图片自动缩放的宽和高
    '''
    im = Image.open(filename).resize((width,height))
    return ImageTk.PhotoImage(im)


def draw_base(top,card_name,card_img,b_color):
    '''
    绘制每个卡面的基础，有图像名称
    第一个参数为绘制的实体，后两个分别为，卡面的图像和名称
    '''
    global img
    img=get_image(card_img,200,300)
    image_img=tk.Label(top,image=img)
    label_name=tk.Label(top,text=card_name,width=14,font=("黑体",20),background=b_color)
    image_img.place(rely=0,relx=0)
    label_name.place(relx=0,rely=0.5)

def card_mc_detail(card_id,card_name,card_img,hp=-1,attack=-1,strength1=-1,strength2=-1,strength3=-1,race_id=-1):
    '''
    展示主角色卡详情
    参数分别为主角色卡的各种属性
    卡牌id，卡牌名称，卡牌图像路径，生命，攻击，三阶段体力值，种族id
    '''
    conn=sqlite3.connect("./tmstone.db")#链接数据库
    cur=conn.cursor()
    top=tk.Toplevel()#顶级窗口作为卡牌详情展示容器
    top.title(card_name)
    top.geometry("400x600")
    top.resizable(0,0)
    draw_base(top,card_name,card_img,"firebrick")
    select_standard_strength="select * from race where id='"+race_id+"'"
    query_select_standard_strength=cur.execute(select_standard_strength)
    for i in query_select_standard_strength:#计算每个主角色的实际体力
        strength1+=i[2]
        strength2+=i[3]
        strength3+=i[4]
    #text="血量: "+str(hp)+"\n攻击: "+str(attack)+"\n幼体体力: "+str(strength1)+"\n进化体体力: "+\
        #str(strength2)+"\n完全体体力: "+str(strength3)+"\n种族: "+race[race_id]
    label_hp=tk.Label(top,text="血量: "+str(hp),font=("黑体",15))
    label_attack=tk.Label(top,text="攻击: "+str(attack),font=("黑体",15))
    label_strength1=tk.Label(top,text="幼体体力: "+str(strength1),font=("黑体",15))
    label_strength2=tk.Label(top,text="进化体体力: "+str(strength2),font=("黑体",15))
    label_strength3=tk.Label(top,text="完全体体力: "+str(strength3),font=("黑体",15))
    label_race=tk.Label(top,text="种族: "+race[race_id],font=("黑体",15))
    #label_sum=tk.Label(top,text=text,font=("黑体",15),anchor="e")
    #label_sum.place(relx=0.53,rely=0.05)
    label_hp.place(relx=0.53,rely=0.05)
    label_attack.place(relx=0.53,rely=0.1)
    label_strength1.place(relx=0.53,rely=0.15)
    label_strength2.place(relx=0.53,rely=0.2)
    label_strength3.place(relx=0.53,rely=0.25)
    label_race.place(relx=0.53,rely=0.3)
    #技能板块
    label_skill=tk.Label(top,text="技能: ",font=("黑体",15))
    label_skill.place(relx=0.02,rely=0.57)
    text_skill=tk.Text(top,width=38,height=11,font=("黑体",15))
    text_skill.place(relx=0.02,rely=0.61)
    select_skill="select * from skill where holder_id = '"+card_id+"'"
    s=cur.execute(select_skill)
    cnt=0
    for i in s:#依次输出该单位的技能
        text_skill.insert("end",i[1]+":"+i[2]+"。消耗:"+str(i[3])+"冷却:"+str(i[4])+"\n")
        cnt+=1
    if cnt==0:#如果找不到该单位的技能，则输出无技能
        text_skill.insert("0.0","无技能")
    text_skill.config(state=DISABLED)#将技能板块的text设置为不可用
    conn.close()
    top.mainloop()

def card_es_detail(card_id,card_name,card_img,m_id,card_type,hp=-1,attack=-1,strength=-1,effect=-1,race_id=-1):
    '''
    展示主专属仆从卡详情
    参数分别为主角色卡的各种属性
    卡牌id，卡牌名称，卡牌图像路径，主角色id，卡牌类型，生命，攻击，体力值，卡牌效果，种族id
    '''
    conn=sqlite3.connect("./tmstone.db")#链接数据库
    cur=conn.cursor()
    top=tk.Toplevel()
    top.title(card_name)
    top.geometry("400x600")
    top.resizable(0,0)
    draw_base(top,card_name,card_img,"lightcoral")
    select_master="select * from main_hero where id = '"+m_id+"'"
    query_select_master=cur.execute(select_master)
    for i in query_select_master:
        master_name=i[1]
    label_master=tk.Label(top,text="主英雄: "+master_name,font=("黑体",15))
    label_master.place(relx=0.53,rely=0.05)
    #判断仆从类型，来规划基础属性
    if card_type=="servant":
        label_type=tk.Label(top,text="仆从类型: 仆从",font=("黑体",15))
        label_hp=tk.Label(top,text="血量: "+str(hp),font=("黑体",15))
        label_attack=tk.Label(top,text="攻击: "+str(attack),font=("黑体",15))
        label_strength=tk.Label(top,text="体力: "+str(strength),font=("黑体",15))
        label_race=tk.Label(top,text="种族: "+race[race_id],font=("黑体",15))
        label_type.place(relx=0.53,rely=0.1)
        label_hp.place(relx=0.53,rely=0.15)
        label_attack.place(relx=0.53,rely=0.2)
        label_strength.place(relx=0.53,rely=0.25)
        label_race.place(relx=0.53,rely=0.3)
    elif card_type=="skill":
        label_type=tk.Label(top,text="仆从类型: 技能",font=("黑体",15))
        label_strength=tk.Label(top,text="体力: "+str(strength),font=("黑体",15))
        label_type.place(relx=0.53,rely=0.1)
        label_strength.place(relx=0.53,rely=0.15)
    else:
        label_type=tk.Label(top,text="仆从类型: 装备",font=("黑体",15))
        label_attack=tk.Label(top,text="攻击: "+str(attack),font=("黑体",15))
        label_strength=tk.Label(top,text="体力: "+str(strength),font=("黑体",15))
        label_type.place(relx=0.53,rely=0.1)
        label_attack.place(relx=0.53,rely=0.15)
        label_strength.place(relx=0.53,rely=0.2)
    #技能模块
    label_skill=tk.Label(top,text="技能: ",font=("黑体",15))
    label_skill.place(relx=0.02,rely=0.57)
    text_skill=tk.Text(top,width=38,height=11,font=("黑体",15))
    text_skill.place(relx=0.02,rely=0.61)
    select_skill="select * from skill where holder_id = '"+card_id+"'"
    s=cur.execute(select_skill)
    cnt=0
    for i in s:
        text_skill.insert("end",i[1]+":"+i[2]+"。消耗:"+str(i[3])+"冷却:"+str(i[4])+"\n")
        cnt+=1
    if cnt==0:
        text_skill.insert("0.0","无技能")
    text_skill.config(state=DISABLED)
    conn.close()
    top.mainloop()

def card_s_detail(card_id,card_name,card_img,is_hero,hp,attack,strength,race_id,quality_id):
    '''
    展示仆从卡详情
    参数分别为主角色卡的各种属性
    卡牌id，卡牌名称，卡牌图像路径，是否为英雄，生命，攻击，体力值，种族id，卡牌品质
    '''
    conn=sqlite3.connect("./tmstone.db")#链接数据库
    cur=conn.cursor()
    top=tk.Toplevel()
    top.title(card_name)
    top.geometry("400x600")
    top.resizable(0,0)
    draw_base(top,card_name,card_img,color[quality_id])
    if is_hero:
        hero_type="英雄"
    else:
        hero_type="普通"
    label_hp=tk.Label(top,text="血量: "+str(hp),font=("黑体",15))
    label_attack=tk.Label(top,text="攻击: "+str(attack),font=("黑体",15))
    label_strength=tk.Label(top,text="体力: "+str(strength),font=("黑体",15))
    label_race=tk.Label(top,text="种族: "+race[race_id],font=("黑体",15))
    label_is_hero=tk.Label(top,text="单位类型: "+hero_type,font=("黑体",15))
    label_type=tk.Label(top,text="卡牌类型: 仆从",font=("黑体",15))
    label_quality=tk.Label(top,text="卡牌品质: "+quality[quality_id],font=("黑体",15))
    label_hp.place(relx=0.53,rely=0.05)
    label_attack.place(relx=0.53,rely=0.1)
    label_strength.place(relx=0.53,rely=0.15)
    label_race.place(relx=0.53,rely=0.2)
    label_is_hero.place(relx=0.53,rely=0.25)
    label_type.place(relx=0.53,rely=0.3)
    label_quality.place(relx=0.53,rely=0.35)
    #技能模块
    label_skill=tk.Label(top,text="技能: ",font=("黑体",15))
    label_skill.place(relx=0.02,rely=0.57)
    text_skill=tk.Text(top,width=38,height=11,font=("黑体",15))
    text_skill.place(relx=0.02,rely=0.61)
    select_skill="select * from effect where card_id = '"+card_id+"'"
    s=cur.execute(select_skill)
    cnt=0
    for i in s:
        text_skill.insert("end",i[1]+":"+i[2]+","+i[3]+"\n")
        cnt+=1
    if cnt==0:
        text_skill.insert("0.0","无技能")
    text_skill.config(state=DISABLED)
    conn.close()
    top.mainloop()

def card_mt_detail(card_id,card_name,card_img,quality_id):
    '''
    展示魔法陷阱卡详情
    参数分别为主角色卡的各种属性
    卡牌id，卡牌名称，卡牌图像路径，卡牌品质
    '''
    conn=sqlite3.connect("./tmstone.db")#链接数据库
    cur=conn.cursor()
    top=tk.Toplevel()
    top.title(card_name)
    top.geometry("400x600")
    top.resizable(0,0)
    draw_base(top,card_name,card_img,color[quality_id])
    card_type=card_id[0]+card_id[1]
    if card_type=="m0":
        card_type="法术"
    else:
        card_type="陷阱"
    label_type=tk.Label(top,text="卡牌类型: "+card_type,font=("黑体",15))
    label_quality=tk.Label(top,text="卡牌品质: "+quality[quality_id],font=("黑体",15))
    label_type.place(relx=0.53,rely=0.1)
    label_quality.place(relx=0.53,rely=0.15)
    #卡牌效果模块
    label_skill=tk.Label(top,text="卡牌效果: ",font=("黑体",15))
    label_skill.place(relx=0.02,rely=0.57)
    text_skill=tk.Text(top,width=38,height=11,font=("黑体",15))
    text_skill.place(relx=0.02,rely=0.61)
    select_skill="select * from effect where card_id = '"+card_id+"'"
    s=cur.execute(select_skill)
    cnt=0
    for i in s:
        text_skill.insert("end",i[1]+":"+i[2]+","+i[3]+"\n")
        cnt+=1
    if cnt==0:
        text_skill.insert("0.0","无效果")
    text_skill.config(state=DISABLED)
    conn.close()
    top.mainloop()

def card_e_detail(card_id,card_name,card_img,attack,type_id,quality_id):
    '''
    展示装备卡详情
    参数分别为主角色卡的各种属性
    卡牌id，卡牌名称，卡牌图像路径，攻击，装备类型，卡牌品质
    '''
    conn=sqlite3.connect("./tmstone.db")#链接数据库
    cur=conn.cursor()
    top=tk.Toplevel()
    top.title(card_name)
    top.geometry("400x600")
    top.resizable(0,0)
    draw_base(top,card_name,card_img,color[quality_id])
    #调出装备类型数据
    select_type="select * from equipment_type where id = '"+type_id+"'"
    query_select_type=cur.execute(select_type)
    for i in query_select_type:
        etype_name=i[1]
        econsumption=i[2]
        edescription=i[3]
    label_attack=tk.Label(top,text="攻击: "+str(attack),font=("黑体",15))
    label_etype=tk.Label(top,text="装备类型: "+etype_name,font=("黑体",15))
    label_consumption=tk.Label(top,text="攻击额外消耗: "+str(econsumption),font=("黑体",15))
    label_type=tk.Label(top,text="卡牌类型: 装备",font=("黑体",15))
    label_quality=tk.Label(top,text="卡牌品质: "+quality[quality_id],font=("黑体",15))
    label_attack.place(relx=0.53,rely=0.05)
    label_etype.place(relx=0.53,rely=0.1)
    label_consumption.place(relx=0.53,rely=0.15)
    label_type.place(relx=0.53,rely=0.2)
    label_quality.place(relx=0.53,rely=0.25)
    #卡牌效果模块
    label_skill=tk.Label(top,text="卡牌效果: ",font=("黑体",15))
    label_skill.place(relx=0.02,rely=0.57)
    text_skill=tk.Text(top,width=38,height=11,font=("黑体",15))
    text_skill.place(relx=0.02,rely=0.61)
    select_skill="select * from effect where card_id = '"+card_id+"'"
    s=cur.execute(select_skill)
    cnt=0
    text_skill.insert("end","装备限制描述:"+edescription+"\n")
    for i in s:
        text_skill.insert("end",i[1]+":"+i[2]+","+i[3]+"\n")
        cnt+=1
    if cnt==0:
        text_skill.insert("end","无效果")
    text_skill.config(state=DISABLED)
    conn.close()
    top.mainloop()