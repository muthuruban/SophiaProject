import json
import os
import sys
import webbrowser

import pyjokes
import pyttsx3 as tts
import speech_recognition

from assistant_model import ModelAssistant

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty("rate", 150)

voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[1].id)

todo_list = []
reminder_list = []


def generic_respond():
    ints = assistant._predict_class(message)
    intents = json.loads(open('intents.json').read())
    res = assistant._get_response(ints, intents)
    print(res)
    speaker.say(res)
    speaker.runAndWait()


# def name_call():
#     generic_respond()


def create_note():
    global recognizer
    generic_respond()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                note = recognizer.recognize_google(audio)
                note.lower()
                print(note)
                print("Give a file name")
                speaker.say("Give a file name")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)
                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
                print("     " * 8 + filename)
            with open(filename, 'w') as anote:
                anote.write(note)
                done = True
                print(f"Your note {filename} has been created successfully")
                speaker.say(f"Your note {filename} has been created successfully")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            print("I didn't get you. Please try again!")
            speaker.say("I didn't get you. Please try again!")


def about():
    generic_respond()


def jokes():
    generic_respond()
    joke = pyjokes.get_joke(language='en', category='neutral')
    print(joke)
    speaker.say(joke)


def quit():
    generic_respond()
    sys.exit(0)


def greetings():
    generic_respond()


def add_reminders():
    global recognizer
    generic_respond()
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            reminder = recognizer.recognize_google(audio)
            reminder = reminder.lower()
            print(reminder)
        reminder_list.append(reminder)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
    try:
        reminder_dict = json.load(open("reminders.json"))
    except json.JSONDecodeError:
        reminder_dict = dict()
    for i in range(len(reminder_dict), len(reminder_list)):
        reminder_dict[i] = reminder_list[i]
    json.dump(reminder_dict, open("reminders.json", 'w'))


def show_reminders():
    generic_respond()
    reminder_dict = json.load(open("reminders.json"))
    for i in range(len(reminder_dict)):
        print(reminder_dict[str(i)])
        speaker.say(str(reminder_dict[str(i)]))
        speaker.runAndWait()


def add_todo():
    global recognizer
    try:
        todo = open("todo.txt", "r+")
        todo_lst = todo.read().split(',')
        todo.close()
        todo = open("todo.txt", "w")
        print("#", todo_lst)
        todo_list.append(todo_lst)
        print(todo_list)
    except FileNotFoundError:
        todo = open("todo.txt", "w")
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            todos = recognizer.recognize_google(audio)
            todos.lower()
            todo_list.append(todos)
        print(todo_list)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
    for i in range(len(todo_list)):
        temp = str(todo_list[i])
        print(temp)
        todo.write('%s' % temp)
        todo.write(",")
    todo.close()


add_todo()


def shutdown():
    global recognizer
    generic_respond()
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            confirmation = recognizer.recognize_google(audio)
            confirmation.lower()
        print(confirmation)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
    if confirmation in "yes":
        return os.system("shutdown /s /t 1")
    else:
        speaker.say("Confirmation rejected")
        speaker.runAndWait()
        return 0


def restart():
    global recognizer
    generic_respond()
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            confirmation = recognizer.recognize_google(audio)
            confirmation.lower()
        print(confirmation)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
    if confirmation in "yes":
        return os.system("shutdown /r /t 1")
    else:
        speaker.say("Confirmation rejected")
        speaker.runAndWait()
        return 0


def logout():
    global recognizer
    generic_respond()
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            confirmation = recognizer.recognize_google(audio)
            confirmation.lower()
        print(confirmation)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
    if confirmation in "yes":
        return os.system("shutdown -l")
    else:
        speaker.say("Confirmation rejected")
        speaker.runAndWait()
        return 0


def hibernate():
    global recognizer
    generic_respond()
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            confirmation = recognizer.recognize_google(audio)
            confirmation.lower()
        print(confirmation)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
    if confirmation in "yes":
        return os.system("shutdown /h")
    else:
        speaker.say("Confirmation rejected")
        speaker.runAndWait()
        return 0


def lock_screen():
    global recognizer
    generic_respond()
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            confirmation = recognizer.recognize_google(audio)
            confirmation.lower()
        print(confirmation)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
    if confirmation in "yes":
        return os.system("rundll32.exe user32.dll, LockWorkStation")
    else:
        speaker.say("Confirmation rejected")
        speaker.runAndWait()
        return 0


def queries():
    return webbrowser.open_new("www.google.com/search?q=" + message)


mappings = {
    "greetings": greetings,
    "create_note": create_note,
    "jokes": jokes,
    # "name_call": name_call,
    "about": about,
    "exit": quit,
    "add_reminders": add_reminders,
    "show_reminders": show_reminders,
    "shut_down": shutdown,
    "restart": restart,
    "sleep": hibernate,
    "log_out": logout,
    "lock_screen": lock_screen,
    "queries": queries,
}

assistant = ModelAssistant('intents.json', intent_methods=mappings)
assistant.load_model()
speaker.say("I am ready to listen!")
print("I am ready to listen!")

while True:
    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)
            message = recognizer.recognize_google(audio)
            message = message.lower()
            print(message)
        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
    except speech_recognition.RequestError:
        recognizer = speech_recognition.Recognizer()
