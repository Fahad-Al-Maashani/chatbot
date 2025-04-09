import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import requests

# Initialize text-to-speech
tts_engine = pyttsx3.init()

# Bing Search API Configuration
BING_API_KEY = "your_bing_api_key_here"  # Replace with your API Key
BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"

# Function for text-to-speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to fetch search results
def search_web(query):
    try:
        headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
        params = {"q": query, "count": 3}  # Limit to top 3 results
        response = requests.get(BING_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()["webPages"]["value"]
        links = [f"{res['name']}: {res['url']}" for res in results]
        return "\n".join(links)
    except Exception as e:
        return f"Error: Unable to fetch results. {str(e)}"

# Function to process user input
def process_input(user_message):
    if "search for" in user_message.lower():
        query = user_message.lower().replace("search for", "").strip()
        results = search_web(query)
        return f"Here are the top search results:\n{results}"
    elif "hello" in user_message.lower():
        return "Hi there! How can I assist you today?"
    elif "bye" in user_message.lower():
        return "Goodbye! Have a nice day!"
    elif "how are you" in user_message.lower():
        return "I'm just a bot, but I'm doing great! How about you?"
    else:
        return "I'm sorry, I can only search the web or perform specific tasks right now."

# Function to send a user message
def send_message():
    user_message = user_input.get()
    if not user_message.strip():
        return
    chat_window.insert(tk.END, f"You: {user_message}\n", "user_text")
    response = process_input(user_message)
    chat_window.insert(tk.END, f"Bot: {response}\n", "bot_text")
    speak(response)
    user_input.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Task-Oriented Chatbot")
root.configure(bg="#1E1E1E")  # Dark mode background
root.geometry("700x600")

# Chat Window
chat_window = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, bg="#252526", fg="#D4D4D4", font=("Arial", 12)
)
chat_window.tag_configure("user_text", foreground="#00FF00")  # Green for user text
chat_window.tag_configure("bot_text", foreground="#ADD8E6")  # Light blue for bot text
chat_window.pack(pady=10, padx=10)

# User Input Field
user_input = tk.Entry(
    root, bg="#333333", fg="#FFFFFF", insertbackground="#FFFFFF", font=("Arial", 14)
)
user_input.pack(pady=10, padx=10, fill=tk.X)

# Button to Send Text Message
send_button = tk.Button(
    root,
    text="Send Text",
    command=send_message,
    bg="#007ACC",
    fg="#FFFFFF",
    font=("Arial", 12),
    activebackground="#005F9E",
    activeforeground="#FFFFFF",
)
send_button.pack(pady=5)

# Run the GUI
root.mainloop()
