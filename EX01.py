import tkinter as tk
from tkinter import ttk
from gtts import gTTS
import os
import tempfile

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech Application")

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Language selection dropdown
        self.language_var = tk.StringVar()
        self.language_var.set("English")
        language_options = ["English", "Sinhala", "Tamil"]
        self.language_dropdown = ttk.Combobox(self.root, textvariable=self.language_var, values=language_options)
        self.language_dropdown.pack(pady=10)

        # Text entry
        self.text_entry = tk.Entry(self.root, width=50)
        self.text_entry.pack(pady=10)

        # Convert button
        self.convert_button = tk.Button(self.root, text="Convert to Speech", command=self.convert_to_speech)
        self.convert_button.pack(pady=10)

        # Status label
        self.status_label = tk.Label(self.root, text="")
        self.status_label.pack(pady=10)

    def convert_to_speech(self):
        text = self.text_entry.get()
        if not text:
            self.status_label.config(text="Please enter text.")
            return

        # Get the selected language
        language = self.language_var.get()
        if language == "English":
            lang_code = "en"
        elif language == "Sinhala":
            lang_code = "si"
        elif language == "Tamil":
            lang_code = "ta"
        else:
            self.status_label.config(text="Unsupported language selected!")
            return

        # Convert text to speech
        try:
            tts = gTTS(text=text, lang=lang_code)
            # Save the audio file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                temp_file.close()
                tts.save(temp_file.name)
                # Play the audio file
                os.system(f"start {temp_file.name}" if os.name == 'nt' else f"xdg-open {temp_file.name}")

            self.status_label.config(text="Conversion successful. Playing...")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()
