#pip install pyttsx3 requests nltk pillow opencv-python PyPDF2 python-docx
#Download NLTK sentiment data:
#import nltk
#nltk.download('vader_lexicon')

import tkinter as tk
from tkinter import scrolledtext, filedialog
import pyttsx3
import requests
from PIL import Image
import cv2
import PyPDF2
from docx import Document
import random
from nltk.sentiment import SentimentIntensityAnalyzer
import os

# Initialize text-to-speech and sentiment analyzer
tts_engine = pyttsx3.init()
sia = SentimentIntensityAnalyzer()

# API Keys and Endpoints
BING_API_KEY = "your_bing_api_key_here"
BING_ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"
GOOGLE_API_KEY = "your_google_api_key_here"
GOOGLE_CX = "your_google_search_engine_id_here"
AZURE_VISION_API = "your_azure_vision_api_key_here"
AZURE_VISION_ENDPOINT = "https://your_endpoint_here.cognitiveservices.azure.com/vision/v3.2/describe"

# Function for text-to-speech
def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Function to analyze sentiment of user messages
def analyze_sentiment(user_message):
    sentiment = sia.polarity_scores(user_message)
    if sentiment["compound"] >= 0.5:
        return "positive"
    elif sentiment["compound"] <= -0.5:
        return "negative"
    else:
        return "neutral"

# Function to process image uploads
def process_image(image_path):
    try:
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_VISION_API,
            "Content-Type": "application/octet-stream",
        }
        with open(image_path, "rb") as image_file:
            response = requests.post(
                AZURE_VISION_ENDPOINT, headers=headers, data=image_file
            )
        response.raise_for_status()
        description = response.json()["description"]["captions"][0]["text"]
        return f"Image Description: {description}"
    except Exception as e:
        return f"Error processing image: {e}"

# Function to process PDF documents
def process_pdf(file_path):
    try:
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text[:500] + "... (truncated)"  # Limit output for display
    except Exception as e:
        return f"Error processing PDF: {e}"

# Function to process Word documents
def process_word(file_path):
    try:
        doc = Document(file_path)
        text = " ".join([paragraph.text for paragraph in doc.paragraphs])
        return text[:500] + "... (truncated)"  # Limit output for display
    except Exception as e:
        return f"Error processing Word document: {e}"

# Function to handle file uploads
def handle_file_upload():
    file_path = filedialog.askopenfilename()
    if file_path.endswith(".pdf"):
        return process_pdf(file_path)
    elif file_path.endswith(".docx"):
        return process_word(file_path)
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        return process_image(file_path)
    else:
        return "Unsupported file type. Please upload a PDF, Word document, or image."

# Function to simulate IoT control
def control_iot(command):
    return f"Simulating IoT control: {command.capitalize()} executed."

# Function to process user input
def process_input(user_message):
    sentiment = analyze_sentiment(user_message)

    if "upload file" in user_message.lower():
        return handle_file_upload()
    elif "control light" in user_message.lower():
        return control_iot("light")
    elif "search with bing" in user_message.lower():
        query = user_message.lower().replace("search with bing", "").strip()
        return search_bing(query)
    elif sentiment == "positive":
        return "I'm glad you're feeling positive today! 😊"
    elif sentiment == "negative":
        return "I'm sorry you're feeling down. I'm here to help if you need me. 💙"
    else:
        return "I can process images, documents, control IoT, and much more! What would you like me to do?"

# Function to fetch Bing search results
def search_bing(query):
    try:
        headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
        params = {"q": query, "count": 3}
        response = requests.get(BING_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        results = response.json()["webPages"]["value"]
        return "\n".join([f"{res['name']}: {res['url']}" for res in results])
    except Exception as e:
        return f"Error fetching Bing results: {e}"

# Function to send user messages
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
root.title("Advanced Multi-Modal Chatbot")
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
