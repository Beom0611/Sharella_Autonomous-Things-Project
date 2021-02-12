# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 15:57:26 2020

@author: psb56
    """

n=input("시작을 원하시면 Enter를 눌러주세요")
if n=='':

    import face_recognition
    import cv2
    import numpy as np
    import serial


    import base64
    import io
    import numpy as np
    import cv2
    from imageio import imread
    import matplotlib.pyplot as plt
    from base64 import b64encode, b64decode

    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db
    from pyrebase import pyrebase

    import time
    import os
    import sys
    import urllib.request
    import pygame
    from PIL import Image

    import hashlib
    import hmac
    import base64
    import requests
    import time, json

    import datetime
    import pickle
    
    print('module complete')

    ###Day setting for sms service###
    now = time.localtime(time.time())
    year = now.tm_year
    month = now.tm_mon
    day = now.tm_mday
    day2= now.tm_mday+int('1')
    hour = now.tm_hour
    t= ['월','화','수','목','금','토','일']
    r = now.tm_wday   
    week = t[r]
    
    week2 =t[r+1]  #일요일에는 +1 하게되면 out of index 뜸 
    
    minute = str(now.tm_min)

    if(hour>=13):
        hour = hour-12
        pmam = 'PM'
    else:
        pmam = 'AM'

    date = str(year) +'년 '+ str(month) + '월 ' + str(day) + '일 ' + str(week) + '요일' + ' '+ str(hour) +':' +  str(minute) + ' ' + pmam
    date2= str(year) +'년 '+ str(month) + '월 ' + str(day2)+ '일 ' + str(week2) + '요일' + ' '+ str(hour) +':' +  str(minute) + ' ' + pmam
    print(date2)
    
    ##Firebase setting##
    cred = credentials.Certificate('appinventor-1-0824-firebase-adminsdk-dff7s-6422b0a12b.json')
    firebase_admin.initialize_app(cred,{
        'databaseURL' :'https://appinventor-1-0824.firebaseio.com/'
        })

    dir = db.reference()

   
    ### Firebase storage Downloads ###
    config = {


        "apiKey" : "AIzaSyBzbqK2y-WywpolQlW_9TQoMRQXAcsYWsE",

     

        "authDomain": "appinventor-1-0824.firbaseapp.com",

     

        "databaseURL" : "https://appinventor-1-0824.firebaseio.com/",

     

        "storageBucket" : "appinventor-1-0824.appspot.com"

     
    }

    firebase = pyrebase.initialize_app(config)

    storage = firebase.storage()

    storage.child("new").download("new" + ".jpg"," ")

    #####Picture image Encoding process####
    filename = "new.jpg"
    with open(filename, "rb") as fid:
        data = fid.read()

    b64_bytes = base64.b64encode(data)
    b64_string = b64_bytes.decode()

    # reconstruct image as an numpy array
    img = imread(io.BytesIO(base64.b64decode(b64_string)))

    # show image
    plt.figure()
    plt.imshow(img, cmap="gray")

    # finally convert RGB image to BGR for opencv
    # and save result
    cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("new_reconstructed.jpg", cv2_img)

    img=Image.open("new.jpg")
    width, height =img.size
    small=img.resize((width//6, height//6), Image.ANTIALIAS) #사진 사이즈 줄이기
    small=img.rotate(90) #회전 90도
    small.save("new2.jpg",'jpeg')

    print("Register new user")
    
    ####Text To Speach####
    
    msgname=dir.get()['message']['name']
    
    client_id = "6escqnyccv"
    client_secret = "gtN7dBGpkqpuiZe42m9yiYIjoEHIO0Fb918iHdnx"

    encText = urllib.parse.quote(msgname+"님 인식을 완료하였습니다.")

    data = "speaker=mijin&speed=0&text=" + encText;

    url1 = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"

    request = urllib.request.Request(url1)

    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)

    request.add_header("X-NCP-APIGW-API-KEY",client_secret)

    response = urllib.request.urlopen(request, data=data.encode('utf-8'))

    rescode = response.getcode()

    if(rescode==200):
        print("TTS mp3 저장")
        response_body = response.read()
        with open('음성녹음subbrella.mp3', 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)
    
    #### Playing sound setting####
        
    def playsound(soundfile):

        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound(soundfile)
        clock = pygame.time.Clock()
        sound.play()
        while pygame.mixer.get_busy():
            print("Playing... - func => playsound")
            clock.tick(1000)

    def playmusic(soundfile):

        pygame.init()
        pygame.mixer.init()
        clock = pygame.time.Clock()
        pygame.mixer.music.load(soundfile)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            print("Playing... - func => playingmusic")
            clock.tick(1000)
             

    def stopmusic():

        pygame.mixer.music.stop()
     
    def getmixerargs():
        pygame.mixer.init()
        freq, size, chan = pygame.mixer.get_init()
        return freq, size, chan
     
     
    def initMixer():
        BUFFER = 3072  # audio buffer size, number of samples since pygame 1.8.
        FREQ, SIZE, CHAN = getmixerargs()
        pygame.mixer.init(FREQ, SIZE, CHAN, BUFFER)

    ##for serial with arduino##
    ard=serial.Serial('COM3',9600) #Arduino port number

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Load a sample picture and learn how to recognize it.
    new_image = face_recognition.load_image_file("new2.jpg")
    new_face_encoding = face_recognition.face_encodings(new_image)[0]


    print('encoding complete')

   ## Playing sound ##
                         
    try:
        initMixer()
        filename = 'camera.mp3'
        playmusic(filename)
    except KeyboardInterrupt:   # to stop playing, press "ctrl-c"
        stopmusic()
        print("\nPlay Stopped by user")
    except Exception:
        print("unknown error")
         
    print("Done")


    # Create arrays of known face encodings and their names
    known_face_encodings = [
        new_face_encoding
    ]

        
    known_face_names = [    
        "new"
        
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
       
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations) 

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "unknown"
               
                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)
                
               
        ## After recognizing users
                
                if name=="new":
                        new=dir.get()['user']['new']
                        print('new info')

                        ## Playing sound ##
                                             
                        try:
                            initMixer()
                            filename = '음성녹음subbrella.mp3'
                            playmusic(filename)
                        except KeyboardInterrupt:   # to stop playing, press "ctrl-c"
                            stopmusic()
                            print("\nPlay Stopped by user")
                        except Exception:
                            print("unknown error")
                             
                        print("Done")
                        
                        
                    
                                #print(i)
                    #####SMS Service####

                        timestamp=int(time.time()*1000)
                        timestamp=str(timestamp)

                        url="https://sens.apigw.ntruss.com" #Api url
                        requesturl="/sms/v2/services/"
                        requesturl2="/messages"

                        serviceId= "ncp:sms:kr:256539275701:psb5657"
                        access_key="McgCbbe1V3nx3GlQNhos"

                        uri=requesturl+serviceId+requesturl2
                        apiurl=url+uri

                        def make_signature(uri,access_key):
                            secret_key="ASVtPi01oxPGghILDblattoEJuNkX0s9G8mgCBKH"
                            secret_key=bytes(secret_key,'UTF-8')
                            method="POST"
                            message= method+" "+uri+"\n"+timestamp+"\n"+access_key
                            message= bytes(message,'UTF-8')
                            signingkey=base64.b64encode(hmac.new(secret_key,message,digestmod=hashlib.sha256).digest())
                            return signingkey

                      

                        msgsms=dir.get()['message']['sms'] # Phone Number
                        num=msgsms.replace(',','').replace('"','')
                        print(num)
                        messages={"to":num} # Phone Number processing
                        body={
                            "type":"SMS",
                            "contentType":"COMM",
                            "countryCode":"82",
                            "from":"01098865657",
                            "content":"이용해주셔서 감사합니다."+date2+"이후 반납시 추가 요금이 부과됩니다",
                            "messages":[messages]
                        }

                        body2=json.dumps(body)

                        headers={
                        'Content-Type': 'application/json; charset=utf-8',
                        'x-ncp-apigw-timestamp':timestamp ,
                        'x-ncp-iam-access-key': access_key,
                        'x-ncp-apigw-signature-v2':make_signature(uri, access_key) 
                        }

                        res=requests.post(apiurl, headers=headers, data=body2)

                        res.request
                        res.status_code
                        res.raise_for_status() # if not 200 0k, gets an error
                        print(res.json()) #if json resposne, changes to dictionary type
                        print(num,'으로 sms 전송완료')
                        
                       
                    
                        info=new.replace(',','').replace('"','')
                        for i in info:
                                print(i)
                                i=i.encode('utf-8')
                                ard.write(i)  #Sending the information to arduino


                if name=="unknown":
                    print('Bye')
                    ard.write(b'0')
                    
        process_this_frame = not process_this_frame
       

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)
        time.sleep(5)
      
        
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
       
   

          
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

  

