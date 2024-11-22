import tkinter as tk
from googletrans import Translator

def translate_text():
    # Get the text from the input field
    text = input_text.get("1.0", tk.END).strip()
    if text:
        translator = Translator()
        translated = translator.translate(text, src='en', dest='si')
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated.text)

# Set up the main application window
root = tk.Tk()
root.title("English to Sinhala Translator")

# Create and place the widgets
tk.Label(root, text="Enter text in English:").pack(pady=10)
input_text = tk.Text(root, height=10, width=50)
input_text.pack(pady=5)

tk.Button(root, text="Translate", command=translate_text).pack(pady=10)

