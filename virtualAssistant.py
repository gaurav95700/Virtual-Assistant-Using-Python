import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if(hour>=0 and hour <12):
        speak("Good Morning!")
    elif (hour>=12 and hour <18):
        speak("Good Afternoon!")
    else:
        speak('Good Evening!')
    speak("I am your Personal Virtual Assistant! Please tell me how may I help you ?")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1 
        audio=r.adjust_for_ambient_noise(source)
        audio=r.listen(source,10)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio,language='en-in')
        print(f"You said :  {query}\n")
        
    except sr.WaitTimeoutError:
        speak("Couldn't hear you. Did you say anything?")
        
        
    except Exception as e:
        #print(e)
        print("Didn't get that! Please Repeat")
        return "None"
    return query

def addressbook(first_name):
    addDict={}
    with open("addressbook.txt",'r') as f:                          #populate the addressbook.txt with your contacts
        for line in f:
            (name,email)=line.split(" ")
            addDict[name]=email
    return addDict.get(first_name,"Error")
      

def sendEmail(to, message):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    with open('credentials.txt','r') as f:                                 #put your credentials in cred.txt fie as shown in example
        cred=f.read()
    eid,passw=cred.split(" ")[0], cred.split(" ")[1]
    server.login(eid,passw)
    server.sendmail(eid,to,message)


if __name__=="__main__":
    wishMe()
    while True:
        query=takeCommand().lower()
        if 'wikipedia'in query:
            speak("Searching wikipedia......")
            query=query.replace("wikipedia"," ")
            results=wikipedia.summary(query,sentences=2)
            speak("According to Wikipedia...")
            print(results)
            speak(results)
            
        if 'who is'in query:
            speak("Searching wikipedia......")
            query=query.replace("who is"," ")
            results=wikipedia.summary(query,sentences=2)
            speak("According to Wikipedia...")
            print(results)
            speak(results)
        
        elif "open youtube" in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")

        elif "open google" in query:
            speak("opening google")
            webbrowser.open("google.com")        
        
        elif "play music" in query:
            music_dir="E:\\Sunday Suspence"
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,songs[0])) 

        elif "time" in query:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
             
        elif "send email" in query:
            try:
                speak("To whom? (First Name Only)")
                contact=takeCommand().lower()
                if mailid=="Error":
                    speak("You have entered a Invalid name. Please Try again")
                    raise "InvalidEmailIdException"
                speak("what should I say?")
                message=takeCommand()
                mailid=addressbook(contact)
                sendEmail( mailid ,message)
                print("Your email has been sent")
           
            except Exception as e:
                print(e)
                speak("Error sending email")
        
        elif "exit" in query:
                speak("Have a Good day!")
                break