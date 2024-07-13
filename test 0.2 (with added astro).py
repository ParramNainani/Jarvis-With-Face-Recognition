import pyttsx3
import wikipedia
import pywhatkit 
import speech_recognition as sr
import cv2
import face_recognition
import numpy as np
import time
import os
from datetime import datetime , date , timedelta

## ASTRO PATCH UPDATE
import swisseph as swe
import matplotlib.pyplot as plt

# Function to calculate planetary positions
def calculate_planetary_positions(jd, lat, lon):
    swe.set_topo(lon, lat, 0)
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mercury': swe.MERCURY,
        'Venus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE,  # Rahu
        'Ketu': swe.MEAN_NODE,  # Ketu (opposite Rahu)
    }
    positions = {}
    for name, planet in planets.items():
        pos, _ = swe.calc_ut(jd, planet)
        positions[name] = pos[0]  # Longitude
    positions['Ketu'] = (positions['Rahu'] + 180) % 360  # Ketu is always opposite Rahu
    return positions

# Function to generate growth and fall based on planetary positions
def interpret_positions(positions):
    # Simplified interpretation logic (use real Vedic astrology principles here)
    growth = (positions['Sun'] + positions['Jupiter'] + positions['Venus']) / 3
    fall = (positions['Saturn'] + positions['Mars'] + positions['Rahu']) / 3
    return growth - fall



# Function to visualize predictions
def visualize_predictions(dates, growth_fall):
    categories = ['Bad' if val < -5 else 'Good' if val > 5 else 'Neutral' for val in growth_fall]
    colors = ['red' if cat == 'Bad' else 'green' if cat == 'Good' else 'black' for cat in categories]

    plt.bar(dates, growth_fall, color=colors)
    plt.xlabel('Date')
    plt.ylabel('Growth-Fall Index')
    plt.title('Growth and Fall Predictions')
    plt.xticks(rotation=45)
    plt.show()
n=0
def voice():
    import datetime
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    def speak(audio):
        engine.say(audio)
        engine.runAndWait()
    def wishme():
        hour = int(datetime.datetime.now().hour)
        if hour>= 0 or hour<12 :
            speak("Good Morning")
        elif hour>= 12 or hour < 18:
            speak("Good afternoon")
        else:
            speak("Good evening")
        speak("Hi Mr. Param Nainani , What's good")

    def takeCommand():
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
    
    import datetime 
    # Function to generate predictions for a specified period
    def generate_predictions(start_date, end_date, lat, lon):
        delta = end_date - start_date
        growth_fall = []

        for i in range(delta.days + 1):
            date = start_date + datetime.timedelta(days=i)
            jd = swe.julday(date.year, date.month, date.day)
            positions = calculate_planetary_positions(jd, lat, lon)
            growth_fall.append(interpret_positions(positions))

        return growth_fall
    def menu():
        name = input("Enter your name: ")
        date_of_birth = datetime.datetime.strptime(input("Enter your date of birth (YYYY-MM-DD): "), "%Y-%m-%d").date()
        time_of_birth = datetime.datetime.strptime(input("Enter your time of birth (HH:MM): "), "%H:%M").time()
        latitude = float(input("Enter your birth latitude: "))
        longitude = float(input("Enter your birth longitude: "))

        while True:
            print("\nAstrological Predictions Menu")
            print("1. Daily Predictions")
            print("2. Monthly Predictions")
            print("3. Yearly Predictions")
            print("4. Specific Range of Years Predictions")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                start_date = datetime.date.today()
                end_date = start_date + datetime.timedelta(days=1)
            elif choice == '2':
                year = int(input("Enter the year: "))
                month = int(input("Enter the month (1-12): "))
                start_date = datetime.date(year, month, 1)
                end_date = (start_date.replace(day=28) + datetime.timedelta(days=4)).replace(day=1) - datetime.timedelta(days=1)
            elif choice == '3':
                year = int(input("Enter the year: "))
                start_date = datetime.date(year, 1, 1)
                end_date = datetime.date(year, 12, 31)
            elif choice == '4':
                start_year = int(input("Enter the start year: "))
                end_year = int(input("Enter the end year: "))
                start_date = datetime.date(start_year, 1, 1)
                end_date = datetime.date(end_year, 12, 31)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")
                continue

            dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            growth_fall = generate_predictions(start_date, end_date, latitude, longitude)
            visualize_predictions(dates, growth_fall)
        
    if __name__ == "__main__":
        wishme()

        while True:
            query = takeCommand()
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

            elif 'get my astro' in query or 'can you get my astro' in query or 'find my astrology' in query:
                speak("Sure i'll do just that for you , Here's the menu program for you astrology queries and prediction")
                print("Sure i'll do just that for you , Here's the menu program for you astrology queries and prediction")
                menu()


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
        os.remove(r'C:\Users\Param Nainani\Attendance.csv')
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
            print('Exiting...') or print('Wrong permission')
            break
face()


