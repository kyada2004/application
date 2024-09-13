import customtkinter as ctk
from tkinter import scrolledtext, Listbox
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import datetime
import tkinter as tk
import threading
from huggingface_hub import InferenceClient
import requests
import json

# Function to handle text-to-speech
def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Initialize the Inference Client
client = InferenceClient(
    "mistralai/Mistral-Nemo-Instruct-2407",
    token="your_huggingface_api_key_add",
)

# Function to handle voice command recognition
def voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        text_area.insert(ctk.END, "Listening...\n")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            text_area.insert(ctk.END, f"You (Voice): {query}\n")
            text_area.yview_moveto(1)
            text_command(query)
        except sr.UnknownValueError:
            response = "Sorry, I didn't catch that. Please try again."
            text_area.insert(ctk.END, f"Jenny: {response}\n")
            if say_option.get():
                say(response)
        except sr.RequestError:
            response = "Sorry, there was an error with the speech recognition service."
            text_area.insert(ctk.END, f"Jenny: {response}\n")
            if say_option.get():
                say(response)

# Function to handle text commands
def text_command(query):
    text_area.insert(tk.END, f"You: {query}\n")
    text_area.yview_moveto(1)

    if "stop" in query.lower():
        response = "Speech stopped."
        text_area.insert(tk.END, f"Jenny: {response}\n")
        if say_option.get():
            say(response)
        return

    if "reset chat" in query.lower():
        text_area.delete('1.0', tk.END)
        response = "All cleared."
        text_area.insert(tk.END, f"Jenny: {response}\n")
        if say_option.get():
            say(response)
        return

    if handle_website_command(query):
        return

    if handle_application_command(query):
        return

    if handle_time_command(query):
        return

    if "weather" in query.lower():
        city = query.split("in")[-1].strip()
        weather_info = fetch_weather(city)
        text_area.insert(tk.END, f"Jenny: {weather_info}\n")
        if say_option.get():
            say(weather_info)
        return

    # Ensure settings are updated
    settings["recent_commands"].append(query)
    save_settings(settings)

    if ai_command(query):
        return

# Function to handle AI commands
def ai_command(query):
    response = client.chat_completion(
        messages=[{"role": "user", "content": query}],
        max_tokens=500
    ).choices[0]['message']['content']

    text_area.insert(tk.END, f"Jenny: {response}\n")
    text_area.yview_moveto(1)
    
    threading.Thread(target=say, args=(response,)).start()
    return

# Function to handle website commands
def handle_website_command(query):
    sites = {
        "youtube": "https://www.youtube.com",
        "wikipedia": "https://www.wikipedia.com",
        "google": "https://www.google.com",
        "linkedin": "https://www.linkedin.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",
        "telegram": "https://web.telegram.org/a/",
        "whatsapp": "https://web.whatsapp.com/",
        "maps": "https://maps.google.com",
        "drive": "https://drive.google.com/drive/quota",
        "mail": "https://mail.google.com/mail/u",
        "classroom": "https://classroom.google.com/",
        "github": "https://github.com/kyada2004",
    }

    for site, url in sites.items():
        if f"open {site}" in query.lower():
            response = f"Opened {site} for you."
            text_area.insert(ctk.END, f"Jenny: {response}\n")
            if say_option.get():
                say(response)
            webbrowser.open(url)
            return True
        elif f"close {site}" in query.lower():
            response = f"Closed {site}."
            text_area.insert(ctk.END, f"Jenny: {response}\n")
            if say_option.get():
                say(response)
            os.system(f"taskkill /f /im chrome.exe")
            return True
    return False

def handle_application_command(query):
    applications = {
        "demo" : " your apllication in link your device ",
        "chrome": "add your application link ",
        "excel": "add your application link",
        "powerpoint": "add your application link",
        "word": "add your application link",
        "wsl": "add your application link",
        "Visual Studio Installer": "add your application link",
        "vs code": "add your application link",
        "spotify": "add your application link",
        "notepad": "add your application link",
        "calculator": "add your application link",
        "xampp": "add your application link",
        "winrar": "add your application link",
        "pwsh": "add your application link",
        "Task Manager": "add your application link",
        "cursor": "add your application link",
        "browers": "add your application link",
        "pycharm": "add your application link",
    }

    for app, path in applications.items():
        if f"open {app}" in query.lower():
            response = f"Opened {app} for you."
            text_area.insert(ctk.END, f"Jenny: {response}\n")
            if say_option.get():
                say(response)
            os.startfile(path)
            return True
        elif f"close {app}" in query.lower():
            response = f"Closed {app}."
            text_area.insert(ctk.END, f"Jenny: {response}\n")
            if say_option.get():
                say(response)
            os.system(f"taskkill /f /im {app}.exe")
            return True
    return False

# Function to handle time commands
def handle_time_command(query):
    if "this time" in query.lower():
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"Sir, the time is {current_time}"
        text_area.insert(ctk.END, f"Jenny: {response}\n")
        if say_option.get():
            say(response)
        return True
    return False

# Function to fetch weather information
def fetch_weather(city):
    api_key = "your_weather_api_key_add"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"Weather in {city}: {weather_description}, {temperature}°C"
        else:
            return "City not found."
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"

# Function to save settings to a JSON file
def save_settings(data, filename="settings.json"):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)

# Function to load settings from a JSON file
def load_settings(filename="settings.json"):
    try:
        with open(filename, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {"enable_speech": True, "recent_commands": []}  

# Save settings when closing the application
def on_exit():
    settings = {
        "enable_speech": say_option.get(),
        "recent_commands": [] 
    }
    save_settings(settings)
    root.destroy()



words = ["open", "youtube", "google", "linkedin", "facebook", "notepad", "calculator", "spotify", "reset chat"]

# Function to handle key release events for the suggestion list
def on_keyrelease(event):
    value = event.widget.get().strip().lower()
    if value:
        data = [word for word in words if word.startswith(value)]
    else:
        data = []
    listbox_update(data)

# Function to update suggestion listbox
def listbox_update(data):
    listbox.delete(0, ctk.END)
    for item in data:
        listbox.insert(ctk.END, item)
    if data:
        listbox.place(x=text_entry.winfo_x(), y=text_entry.winfo_y() + text_entry.winfo_height(), width=text_entry.winfo_width(), height=100)
    else:
        listbox.place_forget()

# Function to handle listbox selection
def on_select(event):
    selection = listbox.get(ctk.ACTIVE)
    text_entry.delete(0, ctk.END)
    text_entry.insert(0, selection)
    listbox.place_forget()

# Configure customtkinter appearance and settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Jenny AI Assistant")
root.geometry("1820x1000")

# Initialize settings and speech option
settings = load_settings()
say_option = ctk.BooleanVar(value=settings["enable_speech"])

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame = ctk.CTkFrame(root)
frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=0)
frame.grid_columnconfigure(0, weight=1)

text_area = scrolledtext.ScrolledText(frame, wrap=ctk.WORD, font=("Arial", 12))
text_area.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

text_entry = ctk.CTkEntry(frame, placeholder_text="Type your query here...", height=40, font=("Arial", 14))
text_entry.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
text_entry.bind("<Return>", lambda event: text_command(text_entry.get()))

listbox = Listbox(frame)
listbox.bind("<<ListboxSelect>>", on_select)

button_frame = ctk.CTkFrame(frame)
button_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

say_checkbox = ctk.CTkCheckBox(button_frame, text="Enable Speech", variable=say_option)
say_checkbox.grid(row=0, column=0, padx=10, sticky="ew")

voice_button = ctk.CTkButton(button_frame, text="🎤 say", command=voice_command, width=150, height=40, corner_radius=10, font=("Arial", 14))
voice_button.grid(row=0, column=1, padx=10, sticky="ew")

text_button = ctk.CTkButton(button_frame, text="Send", command=lambda: text_command(text_entry.get()), width=150, height=40, corner_radius=10, font=("Arial", 14))
text_button.grid(row=0, column=2, padx=5, sticky="ew")

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
