import pyttsx3
import wikipedia
import pywhatkit 
import speech_recognition as sr
import cv2
import face_recognition
import numpy as np
import time
import os
from datetime import datetime

## MODULES


n=0
def voice(): ## TO SETUP THE VOICE 
    import datetime
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) ## CHANGE THE NUMBER TO CHANGE THE VOICE
    def speak(audio):
        engine.say(audio)
        engine.runAndWait()
    def wishme(): ## USED FOR A WISHING EFFECT MORNING , AFTERNOON OR EVENING
        hour = int(datetime.datetime.now().hour)
        if hour>= 0 or hour<12 :
            speak("Good Morning")
        elif hour>= 12 or hour < 18:
            speak("Good afternoon")
        else:
            speak("Good evening")
        speak("Hi Mr. Param Nainani , What's good")

    def takeCommand():## FOR RECOGNIZING WHAT THE PERSON IS SAYING 
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 0.7
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio , language = 'en-in')
            print(f"User said: {query}\n")
        except Exception as e :
            print("Say that again please...")
            return"None"
        return query
    
    if __name__ == "__main__":
        wishme()

        while True:
            query = takeCommand() ## IMP STEP TO ASSIGN WHAT THE USER IS SAYING TO A VARIABLE NAMED QUERY

            if 'who is' in query:
                speak("Searching wikipedia...")
                query = query.replace("who is" , "") 
                result = wikipedia.summary(query,sentences = 2)
                speak("According to wikipedia")
                speak(result)
                print(result)

            elif 'hey' in query:
                speak ("Hello sir")
                print ("Hello sir")


            elif 'how are you' in query:
                speak("im fine how are you")
                print ("im fine how are you")

            elif 'play' in query:
                query = query.replace("play" , "")
                result = pywhatkit.playonyt(query)
                speak("Playing" + query)
                print ("here you go")

            elif 'search' in query:
                query = query.replace("search","")
                result = pywhatkit.search(query)
                speak ("searching" + query)
                print("here you go")

            elif 'exit' in query:
                speak ("Goodbye for now")
                print("bye")
                break

            elif 'good' in query or 'fine' in query:
                speak("Good to know sir")
                print("Good to know sir")
            else:
                print("uh huh")
def face(): 
    global n
    path = r"C:\Users\Param Nainani\OneDrive\Documents\ImagesAttendence"
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)
    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList
    def markAttendance(name):
        os.remove(r'C:\Users\Param Nainani\OneDrive\Documents\Attendance.csv')
        time.sleep(5)
        with open('Attendance.csv','w+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
    ## FOR CAPTURING SCREEN RATHER THAN WEBCAM
    # def captureScreen(bbox=(300,300,690+300,530+300)):
    #     capScr = np.array(ImageGrab.grab(bbox))
    #     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
    #     return capScr
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')
    cap = cv2.VideoCapture(0)
    while n==0:
        success, img = cap.read()
        #img = captureScreen()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex = np.argmin(faceDis)
    
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                #print(name)
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)      
        cv2.waitKey(1)
        work()
        cv2.destroyAllWindows()
def work():
    global n 
    n+=1
    path = r"C:\Users\Param Nainani\OneDrive\Documents\Attendance.csv"
    f1 = open("Attendance.csv" , 'r')
    a = f1.read()
    b = a.split()
    for i in b:
        if i == "PARAM":
            print("ACCESS GRANTED")
            voice()
        else:
            print('NOT MR.PARAM NAINANI USER ACCESS DENIED')
            break
face()
