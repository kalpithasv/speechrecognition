import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
from transformers import pipeline
from fpdf import FPDF
import os  # Add this to check where the file is saved

# Initialize text-to-speech engine
engine = pyttsx3.init()
recognizer = sr.Recognizer()
transcription = ""

# Load summarization model
summarizer = pipeline("summarization")

def start_transcription():
    global transcription
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            transcription += text + "\n"
            text_area.insert(tk.END, text + "\n")
        except sr.UnknownValueError:
            text_area.insert(tk.END, "Could not understand audio\n")
        except sr.RequestError:
            text_area.insert(tk.END, "Speech recognition service error\n")

def summarize_text():
    global transcription
    if transcription:
        summary = summarizer(transcription, max_length=100, min_length=30, do_sample=False)
        summary_text = summary[0]['summary_text']
        text_area.delete('1.0', tk.END)
        text_area.insert(tk.END, "Summary:\n" + summary_text)
    else:
        text_area.insert(tk.END, "No transcription available to summarize.\n")

# ✅ Replace your old save_as_pdf() function with this updated version
def save_as_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    text_content = text_area.get("1.0", tk.END).strip()  # Get text and remove trailing spaces
    if not text_content:
        text_area.insert(tk.END, "No text to save!\n")
        return
    
    pdf.multi_cell(0, 10, text_content)
    
    save_path = os.path.join(os.getcwd(), "lecture_notes.pdf")  # Save in current working directory
    pdf.output(save_path)
    
    print(f"✅ PDF saved at: {save_path}")  # Print location in console
    text_area.insert(tk.END, "✅ Notes saved as PDF\n")

# GUI Setup
root = tk.Tk()
root.title("Live Speech-to-Text Summarizer")
root.geometry("600x400")

text_area = scrolledtext.ScrolledText(root, width=70, height=15)
text_area.pack()

start_button = tk.Button(root, text="Start Transcription", command=start_transcription)
start_button.pack()

summarize_button = tk.Button(root, text="Summarize", command=summarize_text)
summarize_button.pack()

save_button = tk.Button(root, text="Save as PDF", command=save_as_pdf)  # Calls the updated function
save_button.pack()

root.mainloop()
