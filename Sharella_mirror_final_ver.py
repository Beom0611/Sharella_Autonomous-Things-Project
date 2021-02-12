from __future__ import print_function
import datetime
import pickle
import os.path
from tkcalendar import *
from tkinter import *
import time
import json
import requests
try:
    from PIL import Image
    from PIL import ImageTk
except ImportError:
    import Image

from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from pyrebase import pyrebase

##Firebase setting
cred = credentials.Certificate('appinventor-1-0824-firebase-adminsdk-dff7s-6422b0a12b.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' :'https://appinventor-1-0824.firebaseio.com/'
    })
    
while True:
    dir = db.reference()

    a=dir.get()['message']['mirror']
    print(a)
          
    info=a.replace(',','').replace('"','')
    if info=='a':     # if any user uses Sharella app, the mirror changes to smart mode

                     
            root = Tk()
            root.attributes('-fullscreen', True)
            root.configure(background='black')

            bgcolor = 'black'

        
            ### Time, Date setting ###
            now = time.localtime(time.time())
            year = now.tm_year
            month = now.tm_mon
            day = now.tm_mday
            hour = now.tm_hour
            minute = str(now.tm_min)
            if(len(minute) == 1):
                minute = '0'+ minute

            t= ['월','화','수','목','금','토','일']
            r = now.tm_wday
            week = t[r]


            #Display Width, Height

            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()



            ### textLabel ###


            textLabel1=Label(root, text="            AT Brothers",font=('tahoma',20,'bold'),fg='white',bg=bgcolor)

            textLabel2=Label(root, text="       Sharerella",font=('tahoma',38,'bold'),fg='white',bg=bgcolor)

            textLabel3=Label(root, text="  충무로역 대여소",font=('tahoma',30,'bold'),fg='orange',bg=bgcolor)

            textLabel4=Label(root, text="    1.Enter를 눌러주세요.",font=('tahoma',20,'bold'),fg='white',bg=bgcolor)

            textLabel5=Label(root, text="    2.카메라를 응시해주세요.",font=('tahoma',20,'bold'),fg='white',bg=bgcolor)

            textLabel6=Label(root, text="    3.얼굴인식 후  q버튼을 눌러주세요.",font=('tahoma',20,'bold'),fg='white',bg=bgcolor)

            textLabel1.place(x=screen_width/2.8,y=screen_height/1.1)

            textLabel2.place(x=screen_width/3.1,y=screen_height/1.25)

            textLabel3.place(x=screen_width/30,y=screen_height/2.8)

            textLabel4.place(x=screen_width/2.8,y=screen_height/1.8)

            textLabel5.place(x=screen_width/2.8,y=screen_height/1.65)

            textLabel6.place(x=screen_width/2.8,y=screen_height/1.53)

            # Display Time, Date


            date = str(year) +'년 '+ str(month) + '월 ' + str(day) + '일 ' + str(week) + '요일'
            if(hour>=13):
                hour = hour-12
                pmam = 'PM'
            else:
                pmam = 'AM'

            time =  str(hour) +':' +  str(minute) + ' ' + pmam 

            date_label = Label(root, text=date,font=('tahoma',50,'bold'),fg='white',bg=bgcolor)



            date_label.place(x=screen_width/25,y=screen_height/10)


            # Weather Imange Function

            def checking_weather(w):

                if '맑' in w:
                    answer = 'sun.png'
                elif '비' in w:
                    answer = 'rain.png'
                else:
                    answer = 'cloudy.png'
                return answer

            def checking_weather_mini(w):

                if '맑' in w:
                    answer = 'minisun.png'
                elif '비' in w:
                    answer = 'minirain.png'
                else:
                    answer = 'minicloudy.png'

                return answer

            def setting_mini(w):
                if '맑' in w:
                    width = 120
                    height = 75
                elif '비' in w:
                    width = 120
                    height = 75
                else:
                    width = 120
                    height = 75

                return width, height



            #### Crawling Weather Information from Naver Weather News ####

            url = "https://weather.naver.com/rgn/cityWetrCity.nhn?naverRgnCd=09140104"

            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            tem = soup.find_all("div", {"class" : "cell_temperature"}) # Temperature
            weather = soup.find_all("span", {"class" : "rainfall"}) # Rainfall
            wicon=soup.find_all("p", {"class" : "summary"}) # Weather Image
            dust= soup.find_all("div", {"class" : "ttl_area"})

            # Temperature parsing
  
            tem_tm = tem[0].find('strong' , {"class":"temperature"}).text


            # Weather Image
            wicon_tm=wicon[0].find('span', {"class":"weather before_slash"}).text
            print(wicon_tm)

            
            # Rainfall

            rp_tm = weather[0].find('span' , {"class" : "blind"}).text

     
            # Dust
            dust_tm=dust[0].find('em',{"class":"level_text"}).text
            print(dust_tm)


            # Weather Image
                
            file = checking_weather(wicon_tm)
            width, height = setting_mini(wicon_tm)
            wicon_tm = PhotoImage(file = file)     # png 파일로 그림 저장
            wicon_tm_label = Label(root, image = wicon_tm, bd = 0, bg = bgcolor, width = width, height= height)
            wicon_tm_label.place(x=screen_width/1.3,y=screen_height/3.6)

            # Date + Today's Weather Image


            to_date = str(month)+' 월' +' ' + str(day) +' 일'  

            tem_tm_label = Label(root, text=to_date, font=('tahoma',20,'bold'),fg='white',bg=bgcolor)            # 오늘 날짜 - 오늘
            tem_tm_label.place(x=screen_width/1.3,y=screen_height/2.5)


            # Temperature

            tem_tm= tem_tm
            tem_tm_label = Label(root, text=tem_tm, font=('tahoma',15,'bold'),fg='white',bg=bgcolor)
            tem_tm_label.place(x=screen_width/1.3,y=screen_height/2.2)



            #Rainfall
            rp_tm='강수확률: 0%'
            rp_tm_label= Label(root, text=rp_tm, font=('tahoma',15,'bold'),fg='white',bg=bgcolor)
            rp_tm_label.place(x=screen_width/1.3,y=screen_height/2.05)

            #Dust
            dust_tm='미세먼지 농도: '+ dust_tm
            rp_tm_label= Label(root, text=dust_tm, font=('tahoma',15,'bold'),fg='white',bg=bgcolor)
            rp_tm_label.place(x=screen_width/1.3,y=screen_height/1.92)

            try:
                import Tkinter as tk
            except:
                import tkinter as tk

            ### Clock Class  ###
            import time

            class Clock():
                def __init__(self):
                    self.root = tk.Tk()
                    self.label = tk.Label(root,text="", font=('tahoma',50,'bold'),fg='white',bg=bgcolor)
                    self.label.place(x=screen_width/25,y=screen_height/4.5)
                    self.update_clock()
                    self.root.mainloop()

                def update_clock(self):
                    now = time.strftime("%H시 %M분 %S초")
                    self.label.configure(text=now)
                    self.root.after(1000, self.update_clock)

            app=Clock()


      








