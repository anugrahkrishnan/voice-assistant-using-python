import speech_recognition as sr # for performing speech recognition.
import pyttsx4 as p #for performing text-to-speech conversion.
import datetime
import pyjokes
import randfacts
import requests #allows you to send HTTP requests.
from tkinter import * #standard GUI library.
from PIL import Image,ImageTk #for bringing images to UI.
import webbrowser #for opening default web broswer.
from sele import *
import wolframalpha #Compute expert-level answers using.
import pyautogui #control the mouse and keyboard, and other GUI automation tasks.
import os #for interacting with OS.
# import smtplib #for sending email.
#==Voice_Properties==
engine=p.init('sapi5') #Provides application access to text-to-speech synthesis.
voices=engine.getProperty('voices') #Gets the current value of an engine property.
engine.setProperty('voice', voices[1].id) #Changing Voices.
#==GUI1==
window=Tk() #Helps to Display the root Window and manage.
window.resizable(TRUE, FALSE) #disabling resize functions
window.geometry('600x750')
window.title('Dolores')
var = StringVar()
var1 = StringVar()
img= PhotoImage(file='va.png', master= window) #setting BG Image.
img_label= Label(window,image=img) #(label)Used to implement display boxes where you can place text or images.
img_label.place(x=0, y=0)
#==Voice_Control==
def speak(text):
    engine.say(text) #Queues a command to speak an statment.
    engine.runAndWait() #Blocks while processing all currently queued commands.
#==Wish_CMD==  
def start():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        var.set("Good Morning!")
        window.update()
        wish = "Good Morning"
    elif hour >= 12 and hour < 18:
        var.set("Good Afternoon!")
        window.update()
        wish = "Good Afternoon"
    else:
        wish = "Good Evening"
        var.set("Good Evening!")
        window.update()
    speak('Hello Sir,'+ wish+',I am Dolores,Please tell me how may I help you')
#==Take_Command==
#client_id='3n4UxMINuXLhpEQusOFF9g=='
#client_key='Wgap3tMtrDgUn6dQCBwps1NIIInP7xyXnp2eXTXR4Lpm3IfmDEhs-18q48EVb3n-CBR-3ynVfnf3ICF_hbCycQ=='
def command(): # Function defined for Activating Microphone.
    r=sr.Recognizer() #Setting speech recognizer to 'r'.
    with sr.Microphone() as source:
        var.set("Listening...")
        window.update()                    
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 400  
        audio=r.listen(source)
    try:
        var.set("Recognizing...") 
        window.update()
        print("Recognizing...")
        #text=r.recognize_houndify(audio,client_id,client_key) #Calling SpeechAPI For Recognizing.
        text=r.recognize_google(audio,language='en-in')
        print(f"User said:{text}\n")
    except Exception as e:
        print(e)
        var.set("Unable to Recognizing your voice.")
        window.update()
        return "None"
    var.set(text) #For updating Text in window in GUI.
    window.update()
    return text
#==Run_Command==
def run(): #Main CMD's 
    button['state']='disabled' #Setting Mic Button Disabled
    start() #Start_wishing
    while True:
            text=command().lower() # Calling & Storing the Text from Voice and converting to lower case.
            if 'who are you' in text:
                speak('I am your personal voice Assistant')
            elif 'what can you do for me' in text:
                speak('tell time,date,weather,news,facts,jokes,doing basic tasks and help you to search in internet')
            elif 'time' in text:
                time = datetime.datetime.now().strftime('%I: %M')
                var.set(time)
                window.update()
                speak('current time is' + time)
            elif 'date' in text:
                date = datetime.datetime.now().strftime("%d: %m: %Y")
                var.set(date)
                window.update()
                speak(date)
            elif 'weather' in text:
                api_key="d9772b5adc1dab9740024738f4554a86"
                base="https://api.openweathermap.org/data/2.5/weather?"
                city=command()
                speak("What's The Location?")
                complete_url = base + "appid=" + api_key + "&q=" + city 
                response = requests.get(complete_url)
                x = response.json()
                if x["cod"] != "404":
                    y = x["main"]
                    temperature = int(y["temp"]-273)
                    humidity = y["humidity"]
                    speak("the weather report of "+city+"  is")
                    var.set("Temperature is "+str(temperature)+"degree celsius"+"\n humidity (in percentage) is " +str(humidity) +"%")
                    window.update()
                    speak("Temperature is "+str(temperature)+"degree celsius"+"\n humidity (in percentage) is " +str(humidity) +"%")
                    speak("have a nice day!")
                else:
                    speak("oops! coudlnt' find the city")
                    print("cant get the report as the city couldnt be found")
            elif ('read' in text) or ("read today's headlines" in text) or ("today's news" in text):
                speak("Please wait, featching the latest news")
                MAIN_URL_= "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=e1fd1603a28b409599faffe6d8e700a5"
                MAIN_PAGE_ = requests.get(MAIN_URL_).json()
                articles = MAIN_PAGE_["articles"]
                headings=[]
                seq = ['first','second','third','fourth','fifth','sixth']
                for ar in articles:
                    headings.append(ar['title'])
                for i in range(len(seq)):
                    print(f"todays {seq[i]} news is: {headings[i]}")
                    speak(f"todays {seq[i]} news is: {headings[i]}")
                speak("I am done, I have read most of the latest news")
            elif 'joke' in text:
                j=pyjokes.get_joke()
                var.set(j)
                window.update()
                speak(j)
            elif 'fact' in text:
                f=randfacts.get_fact()
                var.set(f)
                window.update()
                speak(f)
            elif "what is" in text:
                client = wolframalpha.Client('V68793-L3RT39K3WL')
                res = client.query(text)
                try:
                    var.set(next(res.results).text)
                    window.update()
                    speak(next(res.results).text)
                except StopIteration:
                    var.set("No results")
            elif "calculate" in text:
                client = wolframalpha.Client('V68793-L3RT39K3WL')
                indx = text.lower().split().index('calculate')
                query = text.split()[indx + 1:]
                res = client.query(' '.join(query))
                answer = next(res.results).text
                var.set("The answer is " + answer)
                window.update()
                speak("The answer is " + answer)
            elif 'open google' in text:
                speak("what do you needed to search for?")
                text1=command()
                # A string formatting method.
                speak("Searching {} in google".format(text1))
                var.set(text1)
                window.update() 
                webbrowser.open("www.google.com/search?q="+text1) 
                speak('Here is what i found for'+text1)
                return text1
            elif 'wikipedia' in text:
                speak("What you need?")
                text2=command()
                speak("Searching {} in wikipedia".format(text2))
                var.set(text2)
                window.update() 
                webbrowser.open("https://en.wikipedia.org/wiki/"+text2) 
                speak('Here is what i found for'+text2)
                return text2
            elif 'open youtube' in text:
                speak("what you need?")
                text3=command()
                speak("Searching {} in you tube".format(text3))
                var.set(text3)
                window.update() 
                webbrowser.open("https://www.youtube.com/results?search_query="+text3)
                speak('Here is what i found for'+text3)
                return text3
            elif 'spotify' in text:
                speak("opening")
                webbrowser.open("https://open.spotify.com/")
            elif 'play' and 'video' in text:
                speak("which video you needed to play?")
                txt3=command()
                speak("Searching {} in youtube".format(txt3))
                print(txt3) 
                assist=web()
                assist.youtube(txt3)
            elif 'open map' in text:
                speak('What is your location?')
                text4=command()
                speak('Here is location'+text4)
                var.set(text4)
                window.update() 
                webbrowser.open("https://google.nl/maps/place/"+text4)
                return text4
            elif 'send an email' in text:
                try:
                    speak("what should I say?")
                    content = command()
                    #speak("To whom do u want to send the email?")
                    to = 'visualdiaries015@gmail.com'
                    assist=web()
                    assist.sendEmail(to,content)
                    speak("Email has been sent to "+str(to))
                except Exception as e:
                    print(e)
                    speak("Sorry sir I am not not able to send this email")
            elif 'search in windows' in text:
                speak("what you need to search")
                f = command().lower()
                pyautogui.press('win', interval=0.2)
                pyautogui.typewrite(f, interval=0.4)
                pyautogui.press('enter', interval=0.4)
            elif 'word' in text:
                speak("Opening Microsoft Word")
                os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk")
            elif 'excel' in text:
                speak("Opening Microsoft Excel")
                os.startfile("C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk")
            elif "switch window" in text:
                speak("Okay sir, Switching the window")
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                pyautogui.keyUp("alt")
            elif "close window" in text:
                speak("Closing window")
                pyautogui.keyDown("alt")
                pyautogui.press("f4")
            elif 'stop listening' in text:
                speak("stopped listening")
                x = 2
                break
            elif 'exit' in text or 'quit' in text or 'bye' in text:
                speak("Thanks for giving me your time")
                exit()
                window.destroy()
            speak("what is your next command sir")
#==GUI2==
label2=Label(window,textvariable=var1,bg='black',fg='#ffffff')
label2.config(font=("Coolvetica RG", 20))
var1.set('User Said:')
label2.pack(pady=5)

label1=Label(window,width=50,textvariable=var,bg='black',fg='#ffffff')
label1.config(font=("Coolvetica RG",14))
var.set('')
label1.pack()

bt=Button(text='EXIT',width=10,command=window.destroy,bg='#2196f3',activebackground='#4444ff')
bt.config(font=("Coolvetica RG", 14))
bt.pack(side=BOTTOM,pady=20)

img1=(Image.open("v1.png"))
resized_image=img1.resize((90,90), Image.ANTIALIAS)
new_image=ImageTk.PhotoImage(resized_image)
button=Button(window,command=run,image=new_image,bg='black')
button.pack(side=BOTTOM,pady=0)
#==To_Run _Continuously==
while True:
    window.mainloop()
    if run():
        run()
    else:
        break