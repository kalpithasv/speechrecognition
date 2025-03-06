import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline
from fpdf import FPDF
import threading
import os

# Initialize speech recognition, text-to-speech, and summarization
engine = pyttsx3.init()
recognizer = sr.Recognizer()
transcription = ""
listening = False  # Flag to track listening state
summarizer = pipeline("summarization")

def listen_continuous():
    """Continuously listens and transcribes speech until stopped."""
    global listening, transcription
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        text_area.insert(tk.END, "Listening...\n")
        while listening:
            try:
                audio = recognizer.listen(source, timeout=None)
                text = recognizer.recognize_google(audio)
                transcription += text + "\n"
                text_area.insert(tk.END, text + "\n")
                text_area.yview(tk.END)  # Auto-scroll
            except sr.UnknownValueError:
                text_area.insert(tk.END, "Could not understand audio\n")
            except sr.RequestError:
                text_area.insert(tk.END, "Speech recognition service error\n")

def start_transcription():
    """Starts continuous speech recognition in a separate thread."""
    global listening
    if not listening:
        listening = True
        threading.Thread(target=listen_continuous, daemon=True).start()
    else:
        text_area.insert(tk.END, "Already listening...\n")

def stop_transcription():
    """Stops the speech recognition loop."""
    global listening
    listening = False
    text_area.insert(tk.END, "Transcription stopped.\n")

def summarize_text():
    """Summarizes the transcribed text."""
    global transcription
    if transcription:
        summary = summarizer(transcription, max_length=100, min_length=30, do_sample=False)
        summary_text = summary[0]['summary_text']
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "Summary:\n" + summary_text)
    else:
        text_area.insert(tk.END, "No transcription available to summarize.\n")

def save_as_pdf():
    """Saves transcribed text as a PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    text_content = text_area.get("1.0", tk.END).strip()
    if not text_content:
        text_area.insert(tk.END, "No text to save!\n")
        return

    pdf.multi_cell(0, 10, text_content)

    save_path = os.path.join(os.getcwd(), "lecture_notes.pdf")
    pdf.output(save_path)

    text_area.insert(tk.END, "✅ Notes saved as PDF\n")

# GUI Setup
root = tk.Tk()
root.title("Live Speech-to-Text Summarizer")
root.geometry("600x400")

# Text area
text_area = scrolledtext.ScrolledText(root, width=70, height=15)
text_area.pack(pady=10)

# Button frame for Start & Stop
button_frame1 = tk.Frame(root)
button_frame1.pack()

start_button = tk.Button(button_frame1, text="▶ Start Transcription", command=start_transcription, width=20, bg="green", fg="white")
start_button.grid(row=0, column=0, padx=10, pady=5)

stop_button = tk.Button(button_frame1, text="⏹ Stop Transcription", command=stop_transcription, width=20, bg="red", fg="white")
stop_button.grid(row=0, column=1, padx=10, pady=5)

# Button frame for Summarize & Save
button_frame2 = tk.Frame(root)
button_frame2.pack()

summarize_button = tk.Button(button_frame2, text="📝 Summarize", command=summarize_text, width=20, bg="blue", fg="white")
summarize_button.grid(row=1, column=0, padx=10, pady=5)

save_button = tk.Button(button_frame2, text="💾 Save as PDF", command=save_as_pdf, width=20, bg="purple", fg="white")
save_button.grid(row=1, column=1, padx=10, pady=5)

root.mainloop()
