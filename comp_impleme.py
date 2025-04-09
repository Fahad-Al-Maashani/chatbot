import tkinter as tk
from tkinter import scrolledtext
import requests
import pyttsx3

# Initialize text-to-speech
tts_engine = pyttsx3.init()

# API Keys and Endpoints
BING_API_KEY = "your_bing_api_key_here"
BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
GOOGLE_API_KEY = "your_google_api_key_here"
GOOGLE_CX = "your_google_search_engine_id_here"
GPT_ENDPOINT = "https://api.openai.com/v1/completions"  # Example for OpenAI GPT

# Function for text-to-speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to search with Bing
def search_bing(query):
    try:
        headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
        params = {"q": query, "count": 3}
        response = requests.get(BING_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()["webPages"]["value"]
        return [f"{res['name']}: {res['url']}" for res in results]
    except Exception as e:
        return [f"Error fetching Bing results: {e}"]

# Function to search with Google
def search_google(query):
    try:
        url = f"https://www.googleapis.com/customsearch/v1"
        params = {"q": query, "key": GOOGLE_API_KEY, "cx": GOOGLE_CX}
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()["items"]
        return [f"{res['title']}: {res['link']}" for res in results[:3]]
    except Exception as e:
        return [f"Error fetching Google results: {e}"]

# Function to process GPT responses
def process_gpt(query):
    try:
        headers = {"Authorization": f"Bearer your_openai_api_key_here"}
        data = {
            "model": "text-davinci-003",
            "prompt": f"Provide a detailed search result for: {query}",
            "max_tokens": 100,
        }
        response = requests.post(GPT_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
    except Exception as e:
        return f"Error fetching GPT response: {e}"

# Function to process user input
def process_input(user_message):
    if "search with bing" in user_message.lower():
        query = user_message.lower().replace("search with bing", "").strip()
        results = search_bing(query)
        return f"Bing Search Results:\n" + "\n".join(results)
    elif "search with google" in user_message.lower():
        query = user_message.lower().replace("search with google", "").strip()
        results = search_google(query)
        return f"Google Search Results:\n" + "\n".join(results)
    elif "use gpt" in user_message.lower():
        query = user_message.lower().replace("use gpt", "").strip()
        result = process_gpt(query)
        return f"GPT Response:\n{result}"
    elif "open safari" in user_message.lower():
        import os
        url = user_message.lower().replace("open safari", "").strip()
        os.system(f'open -a "Safari" {url}')  # macOS-specific
        return f"Opening {url} in Safari..."
    else:
        return "I'm sorry, I can't understand that request."

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
root.title("Multi-Search Chatbot")
root.configure(bg="#1E1E1E")  # Dark mode
root.geometry("800x600")

# Chat Window
chat_window = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, bg="#252526", fg="#D4D4D4", font=("Arial", 12)
)
chat_window.tag_configure("user_text", foreground="#00FF00")
chat_window.tag_configure("bot_text", foreground="#ADD8E6")
chat_window.pack(pady=10, padx=10)

# User Input Field
user_input = tk.Entry(root, bg="#333333", fg="#FFFFFF", font=("Arial", 14))
user_input.pack(pady=10, padx=10, fill=tk.X)

# Send Button
send_button = tk.Button(
    root, text="Send", command=send_message, bg="#007ACC", fg="#FFFFFF", font=("Arial", 12)
)
send_button.pack(pady=5)

# Run the GUI
root.mainloop()
