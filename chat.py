import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
import random

# Initialize Text-to-Speech Engine
tts_engine = pyttsx3.init()

# Predefined intents and responses
intents = {
    "greeting": ["Hi there!", "Hello! How can I assist you?", "Hey! What's up?"],
    "how_are_you": ["I'm doing great! How about you?", "I'm fantastic, thank you!"],
    "name": ["I’m ChatBot3000!", "My name is ChatBuddy.", "You can call me ChatBot!"],
    "goodbye": ["Goodbye! Have a nice day!", "Bye! Take care!", "See you next time!"],
}

# Function for Text-to-Speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function for Speech-to-Text
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            chat_window.insert(tk.END, "Chatbot: Listening...\n", "bot_text")
            root.update()  # Update GUI while listening
            audio = recognizer.listen(source)
            user_input = recognizer.recognize_google(audio)
            chat_window.insert(tk.END, f"You (Voice): {user_input}\n", "user_text")
            return user_input.lower()
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
        except sr.RequestError:
            return "There was an issue with the speech recognition service."

# Function to handle chatbot responses
def chatbot_response(user_input):
    if "hello" in user_input or "hi" in user_input:
        return random.choice(intents["greeting"])
    elif "how are you" in user_input:
        return random.choice(intents["how_are_you"])
    elif "your name" in user_input:
        return random.choice(intents["name"])
    elif "bye" in user_input:
        return random.choice(intents["goodbye"])
    return "I'm sorry, I don't understand that."

# Function to handle text input
def send_message():
    user_message = user_input.get()
    if not user_message.strip():
        return
    chat_window.insert(tk.END, f"You: {user_message}\n", "user_text")
    response = chatbot_response(user_message)
    chat_window.insert(tk.END, f"Chatbot: {response}\n", "bot_text")
    speak(response)
    user_input.delete(0, tk.END)

# Function to handle voice input
def send_voice_message():
    user_message = listen()
    if not user_message.strip():
        response = "I couldn't catch that. Please try again."
    else:
        response = chatbot_response(user_message)
    chat_window.insert(tk.END, f"Chatbot: {response}\n", "bot_text")
    speak(response)

# GUI Setup with Dark Mode
root = tk.Tk()
root.title("Chatbot - Dark Mode")
root.configure(bg="#1E1E1E")  # Dark background
root.geometry("600x500")

# Chat Window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, bg="#252526", fg="#D4D4D4", insertbackground="#D4D4D4", font=("Arial", 12))
chat_window.tag_configure("user_text", foreground="#00FF00")  # Green for user text
chat_window.tag_configure("bot_text", foreground="#ADD8E6")  # Light blue for bot text
chat_window.pack(pady=10, padx=10)

# User Input Field
user_input = tk.Entry(root, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Arial", 14))
user_input.pack(pady=10, padx=10, fill=tk.X)

# Send Text Button
send_button = tk.Button(root, text="Send Text", command=send_message, bg="#007ACC", fg="#FFFFFF", font=("Arial", 12), activebackground="#005F9E", activeforeground="#FFFFFF")
send_button.pack(pady=5)

# Send Voice Button
voice_button = tk.Button(root, text="Send Voice", command=send_voice_message, bg="#005F9E", fg="#FFFFFF", font=("Arial", 12), activebackground="#007ACC", activeforeground="#FFFFFF")
voice_button.pack(pady=5)

# Run the GUI
root.mainloop()
