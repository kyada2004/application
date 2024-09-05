import customtkinter as ctk
import requests
from tkinter import scrolledtext, Listbox
import speech_recognition as sr

# Function to fetch weather data
def fetch_weather(city):
    api_key = "7d328d3002be2c7a0828b77b7f2c0de9"
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

# Function to handle text command
def text_command_weather(event=None):
    user_input = text_entry.get().strip()
    if user_input:
        if 'weather' in user_input.lower():
            city = user_input.split('weather')[-1].strip()  # Extract city from input
            weather_info = fetch_weather(city)
            text_area.insert(ctk.END, f"User: {user_input}\n")
            text_area.insert(ctk.END, f"Jenny: {weather_info}\n\n")
        else:
            # Other command processing can be added here
            text_area.insert(ctk.END, f"User: {user_input}\n")
            text_area.insert(ctk.END, "Jenny: Command not recognized.\n\n")
        text_entry.delete(0, ctk.END) 

# Function to handle voice command
def voice_command_weather():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        text_area.insert(ctk.END, "Jenny: Listening...\n")
        try:
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            text_area.insert(ctk.END, f"User: {user_input}\n")
            if 'weather' in user_input.lower():
                city = user_input.split('weather')[-1].strip()  # Extract city from input
                weather_info = fetch_weather(city)
                text_area.insert(ctk.END, f"Jenny: {weather_info}\n\n")
            else:
                text_area.insert(ctk.END, "Jenny: Command not recognized.\n\n")
        except sr.UnknownValueError:
            text_area.insert(ctk.END, "Jenny: Sorry, I did not understand that.\n\n")
        except sr.RequestError as e:
            text_area.insert(ctk.END, f"Jenny: Sorry, there was an error with the request: {e}\n\n")

# Setting up the CustomTkinter application
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Jenny AI Assistant")
root.geometry("700x600")

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
text_entry.bind("<Return>", text_command_weather)

listbox = Listbox(frame)
listbox.bind("<<ListboxSelect>>")

button_frame = ctk.CTkFrame(frame)
button_frame.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

speak_option = ctk.BooleanVar(value=True)
speak_checkbox = ctk.CTkCheckBox(button_frame, text="Enable Speech", variable=speak_option)
speak_checkbox.grid(row=0, column=0, padx=10, sticky="ew")

voice_button = ctk.CTkButton(button_frame, text="🎤 Speak", command=voice_command_weather, width=150, height=40, corner_radius=10, font=("Arial", 14))
voice_button.grid(row=0, column=1, padx=10, sticky="ew")

text_button = ctk.CTkButton(button_frame, text="Send", command=text_command_weather, width=150, height=40, corner_radius=10, font=("Arial", 14))
text_button.grid(row=0, column=2, padx=5, sticky="ew")

root.mainloop()
