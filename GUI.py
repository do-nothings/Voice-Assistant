from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from PIL import ImageTk, Image
import speech_recognition as sr
import pyttsx3 as p  # convert text format into speech format
import os
import smtplib
import pywhatkit as kit
import webbrowser
import datetime
import joke
from PyDictionary import PyDictionary
from turtle import *
from random import randrange
from freegames import square, vector
from todolist import *
from weather import *

engine = p.init( 'sapi5' )  # Microsoft Speech API(SAPI5) technology for voice recognition and synthesis
rate = engine.getProperty( 'rate' )
engine.setProperty( 'rate', 180 )
voices = engine.getProperty( 'voices' )  # gets you the details of current voice
engine.setProperty( 'voice', voices[1].id )  # 0=male voice  1-female voice


def wishme():
    hour = int( datetime.datetime.now().hour )
    if hour > 0 and hour < 12:
        return ("Good morning!")
    elif hour >= 12 and hour < 16:
        return ("Good afternoon!")
    else:
        return ("Good evening!")


# function of output audio
def speak(text, icon=True):
    if icon:
        Label(chat_frame, image=bot_img, bg=chatBgColor).pack(anchor='w', pady=0)
    pinframe(text,True)
    root.update()
    engine.say(text)
    engine.runAndWait()


# read users voice
r = sr.Recognizer()

def record(clearChat=True, iconDisplay=True):
    with sr.Microphone() as source:
        r.energy_threshold = 10000
        r.adjust_for_ambient_noise( source, 1.2 )
        audio = r.listen( source )
        voice = ""

        try:
            voice = r.recognize_google( audio )
            if clearChat:
                clearChatScreen()
            if iconDisplay:
                Label(chat_frame,image=user_img, bg=chatBgColor).pack(anchor='e', pady=0)
            pinframe(voice)

        except sr.UnknownValueError:
            speak( "Sorry, I did not get that" )
            exit()
        except sr.RequestError:
            speak( "Sorry, my service is down" )
        return voice


def action(voice):
    if 'what is the time now' in voice:
        today_date = datetime.datetime.now()
        speak("Today is " + today_date.strftime("%d") + " of " + today_date.strftime("%B"))
        speak("And its currently " + (today_date.strftime("%I")) + ":" + (today_date.strftime("%M")) + (today_date.strftime("%p")), False)


    elif 'search' in voice:
        speak( "What do you want to search for?" )
        search = record()
        url = 'https://www.google.com/search?q=' + search
        webbrowser.get().open( url )
        speak( "This is what I found for " + search, False )


    elif 'video' in voice:
        speak( "What do you want to search for?" )
        search = record()
        kit.playonyt( search )
        speak( "This is video of " + search, False )

    elif 'location' in voice:
        speak("What is the location?")
        search = record()
        url = 'https://www.google.nl/maps/place/' + search
        webbrowser.get().open(url)
        speak("This is the location of " + search, False )


    elif 'send email' in voice:

        Address = os.environ.get('my_email')
        Password = os.environ.get('my_password')

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(Address, Password)

            speak("Who is the receiver?")
            receiver = simpledialog.askstring("Email Bot", "Receiver Email Address")

            if receiver is not None:
                speak("What is your email subject?", False)
                subject = record(False,False)
                speak("What you want to send?", False)
                body = record(False,False)
                message = f'Subject: {subject}\n\n{body}'
                smtp.sendmail(Address, receiver, message)  # sender, receiver, message
                speak("Done sending email.", False)
            else:
                messagebox.showerror("ERROR", "Sorry, I can't send email without receiver.")

    elif 'tell me a joke' in voice:
        jokes = joke.joke()
        speak(jokes)

    elif 'weather' in voice:
        speak( "Temperature in " + str(city) + " now is " + str( temp() ) + "degree celsius. " )
        speak( "The day today will have " + str( status() ) , False)
        pinframe("--------Weather---------" '\n' "Temperature:" + str(temp()) + "degree celcius"'\n' "Status:" + str(status()), True)

    elif 'item' in voice:
        speak( "What do you want to add to to-do list?" )
        i = record()
        speak( f"Add <{i}> to your to-do list" )
        add( i )

    elif 'show' in voice:
        if item != []:
            speak("Your to-do list is as following:")
            speak('\n'.join(item), False)

        else:
            speak( "There is no item in your to-do list." )

    elif 'delete' in voice:
        speak( "What item do you want to delete in to-do list?" )
        i = record()
        speak( f"{i} is deleted from the list" )
        delete(i)

    elif 'meaning' in voice:
        dic = PyDictionary()
        speak("Which word you would like to find meanings?")
        query = record()
        word = dic.meaning(query)

        i = 0
        if i < 1:
            for state in word:
                speak(f"the meaning of {query} is ".format(query) + str((word[state])[:2]))
                i += 1
        speak("If you want to find more meaning please press Yes else press No to exit.", False)
        find_more = messagebox.askyesno("Questions", "Would you like to find more meaning?")

        while find_more:
            clearChatScreen()
            speak("Which word you would like to find meanings?")
            dic = PyDictionary
            query = record()
            word = dic.meaning(query)

            i = 0
            if i < 1:
                for state in word:
                    speak(f"the meaning of {query} is ".format(query) + str((word[state])[:2]))
                    i += 1

            speak("If you want to find more meaning please press Yes else press No to exit.", False)
            find_more = messagebox.askyesno("Questions", "Would you like to find more meaning?")

        speak("Thank you and Hope I was helpful" )

    elif 'play' in voice:
        food = vector(0, 0)
        snake = [vector(10, 0)]
        aim = vector(0, -10)

        def change(x, y):
            "Change snake direction."
            aim.x = x
            aim.y = y

        def inside(head):
            "Return True if head inside boundaries."
            return -200 < head.x < 190 and -200 < head.y < 190

        def move():
            "Move snake forward one segment."
            head = snake[-1].copy()
            head.move(aim)

            if not inside(head) or head in snake:
                square(head.x, head.y, 9, 'red')
                update()
                return

            snake.append(head)

            if head == food:
                food.x = randrange(-15, 15) * 10
                food.y = randrange(-15, 15) * 10
                speak('Length of snake is ' + str(len(snake)))
            else:
                snake.pop(0)

            clear()

            for body in snake:
                square(body.x, body.y, 9, 'green')

            square(food.x, food.y, 9, 'red')
            update()
            ontimer(move, 100)

        hideturtle()
        tracer(False)
        listen()
        onkey(lambda: change(10, 0), 'Right')
        onkey(lambda: change(-10, 0), 'Left')
        onkey(lambda: change(0, 10), 'Up')
        onkey(lambda: change(0, -10), 'Down')
        move()
        done()


    elif 'exit' in voice:
        speak( "Goodbye! Have a nice day!" )
        exit()
    else:
        speak( "Sorry, I don't understand. Can you repeat again?" )


def start():
    speak("Hello, " + wishme() + "! I'm your voice assistant. ")
    while 1:
        speak("What can I help you?", False)
        voice = record()
        action(voice)


def stop():
    exit()


################################## GUI ######################################
botChatTextBg = "#CC9972"
botChatText = "white"
userChatTextBg = "#8C533D"
chatBgColor = '#DFCBB2'
background = '#F1E7D6'
textColor = 'black'

root = Tk()
root.title( 'Voice Assistant' )
w_width, w_height = 500, 700
s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
root.geometry('%dx%d+%d+%d' % (w_width,w_height,x,y-30)) #center location of the screen
root.configure(bg=background)
root.resizable( False, False )

name_label = Label( text='|| Voice Assistant ||', width=300, bg=background, fg="#8C533D", font=("Ink Free", 25, 'bold'))
name_label.pack()

#button
start_button= Button(text='   Start   ', command = start)
start_button.place(x=170, y=650)

stop_button = Button(text='   EXIT   ', command = stop)
stop_button.place(x=270, y=650)


############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########
def pinframe(text,bot=False):
    if bot:
        botchat = Label(chat_frame,text=text, bg=botChatTextBg, fg=botChatText, justify=LEFT, wraplength=300, font=('MV Boli', 12))
        botchat.pack(anchor='w',ipadx=5,ipady=5,pady=5)

    else:
        userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white', justify=RIGHT, wraplength=300, font=('MV Boli', 12))
        userchat.pack(anchor='e',ipadx=2,ipady=2,pady=5)


def clearChatScreen():
    for wid in chat_frame.winfo_children():
        wid.destroy()

#chatframe
chat_frame = Frame(root, width=400,height=580,bg=chatBgColor)
chat_frame.pack(padx=10)
chat_frame.pack_propagate(0)

#bot and user image
botpic = Image.open("robot1.png")
resize_bi = botpic.resize((50,50), Image.ANTIALIAS)
bot_img = ImageTk.PhotoImage(resize_bi)

userpic = Image.open("user1.png")
resize_ui = userpic.resize((50,50), Image.ANTIALIAS)
user_img = ImageTk.PhotoImage(resize_ui)

root.mainloop()