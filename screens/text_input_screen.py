import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr

STANDARD_WIDTH = 22
STANDARD_HEIGHT = 3

class TextInputScreen(tk.Frame):
    def __init__(self, master, go_home_callback, confirm_callback, language="EN"):
        super().__init__(master, bg="#1e1e2f")
        self.master = master
        self.go_home_callback = go_home_callback
        self.confirm_callback = confirm_callback
        self.language = language
        self.labels = self.get_labels()
        self.placeholder_text = "Enter text or speak..." if self.language == "EN" else "Escriba o hable..."
        self.create_widgets()

    def get_labels(self):
        return {
            "EN": {
                "title": "Text / Voice Control\n\nTexto / Voz para Controlar",
                "speak": "🎙️ Speak",
                "clear": "🧹 Clear",
                "send": "🌐 Translate",
                "home": "🏠 Back to Home",
                "toggle": "🇪🇸 Español",
                "listening": "Listening...",
                "error_recognition": "Could not understand audio.",
                "error_service": "Speech recognition service unavailable.",
                "warn_empty": "Please enter or say something first."
            },
            "ES": {
                "title": "Control de Texto / Voz\n\nText / Voice Control",
                "speak": "🎙️ Hablar",
                "clear": "🧹 Borrar",
                "send": "🌐 Traducir",
                "home": "🏠 Volver al Inicio",
                "toggle": "🇺🇸 English",
                "listening": "Escuchando...",
                "error_recognition": "No se pudo entender el audio.",
                "error_service": "Servicio de reconocimiento no disponible.",
                "warn_empty": "Por favor ingresa o di algo primero."
            }
        }

    def create_widgets(self):
        self.main_frame = tk.Frame(self, bg="#1e1e2f")
        self.main_frame.pack(expand=True)

        self.lang_toggle = tk.Button(
            self.main_frame,
            text=self.labels[self.language]["toggle"],
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="black",
            width=12,
            height=1,
            command=self.toggle_language
        )
        self.lang_toggle.pack(anchor="ne", pady=10, padx=10)

        self.title = tk.Label(
            self.main_frame,
            text=self.labels[self.language]["title"],
            font=("Arial", 24, "bold"),
            bg="#1e1e2f",
            fg="white"
        )
        self.title.pack(pady=(10, 30))

        self.text_entry = tk.Text(
            self.main_frame,
            height=6,
            width=72,
            font=("Arial", 16),
            bg="#f4f4f4",
            fg="gray",
            wrap="word",
            bd=3,
            relief="sunken"
        )
        self.text_entry.pack(pady=10)
        self.text_entry.insert("1.0", self.placeholder_text)
        self.text_entry.bind("<FocusIn>", self.clear_placeholder)
        self.text_entry.bind("<FocusOut>", self.restore_placeholder_if_empty)

        self.btn_frame = tk.Frame(self.main_frame, bg="#1e1e2f")
        self.btn_frame.pack(pady=30)

        self.speak_btn = tk.Button(
            self.btn_frame,
            text=self.labels[self.language]["speak"],
            font=("Arial", 14, "bold"),
            bg="#4fc3f7",
            fg="black",
            activebackground="#29b6f6",
            activeforeground="white",
            width=STANDARD_WIDTH,
            height=STANDARD_HEIGHT,
            command=self.speak_input
        )
        self.speak_btn.grid(row=0, column=0, padx=15)

        self.clear_btn = tk.Button(
            self.btn_frame,
            text=self.labels[self.language]["clear"],
            font=("Arial", 14, "bold"),
            bg="#fbbc04",
            fg="black",
            activebackground="#e0a800",
            activeforeground="white",
            width=STANDARD_WIDTH,
            height=STANDARD_HEIGHT,
            command=self.clear_input
        )
        self.clear_btn.grid(row=0, column=1, padx=15)

        self.send_btn = tk.Button(
            self.btn_frame,
            text=self.labels[self.language]["send"],
            font=("Arial", 14, "bold"),
            bg="#03dac6",
            fg="black",
            activebackground="#018786",
            activeforeground="white",
            width=STANDARD_WIDTH,
            height=STANDARD_HEIGHT,
            command=self.send_to_confirm_screen
        )
        self.send_btn.grid(row=0, column=2, padx=15)

        self.home_btn = tk.Button(
            self.main_frame,
            text=self.labels[self.language]["home"],
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            fg="black",
            activebackground="#c62828",
            activeforeground="white",
            width=STANDARD_WIDTH * 2,
            height=STANDARD_HEIGHT,
            bd=3,
            relief="ridge",
            cursor="hand2",
            command=self.go_home_callback
        )
        self.home_btn.pack(pady=(10, 40))

    def toggle_language(self):
        self.language = "ES" if self.language == "EN" else "EN"
        self.update_labels()

    def update_labels(self):
        old_placeholder = self.placeholder_text
        self.labels = self.get_labels()

        self.lang_toggle.config(text=self.labels[self.language]["toggle"])
        self.title.config(text=self.labels[self.language]["title"])
        self.speak_btn.config(text=self.labels[self.language]["speak"])
        self.clear_btn.config(text=self.labels[self.language]["clear"])
        self.send_btn.config(text=self.labels[self.language]["send"])
        self.home_btn.config(text=self.labels[self.language]["home"])

        self.placeholder_text = "Enter text or speak..." if self.language == "EN" else "Escriba o hable..."
        current_text = self.text_entry.get("1.0", tk.END).strip()
        if not current_text or current_text == old_placeholder:
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert("1.0", self.placeholder_text)
            self.text_entry.config(fg="gray")

    def clear_input(self):
        self.text_entry.delete("1.0", tk.END)

    def clear_placeholder(self, event):
        current_text = self.text_entry.get("1.0", tk.END).strip()
        if current_text == self.placeholder_text:
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.config(fg="black")

    def restore_placeholder_if_empty(self, event):
        current_text = self.text_entry.get("1.0", tk.END).strip()
        if not current_text:
            self.text_entry.insert("1.0", self.placeholder_text)
            self.text_entry.config(fg="gray")

    def speak_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("🎙️ Please speak now...")
            try:
                audio = recognizer.listen(source, timeout=10)
            except sr.WaitTimeoutError:
                print("⏰ Timed out — no speech detected.")
                return
        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            self.text_entry.delete("1.0", tk.END)
            self.text_entry.insert("1.0", text)
            self.text_entry.config(fg="black")
        except sr.UnknownValueError:
            print("🤷 Speech was unclear.")
        except sr.RequestError:
            print("🌐 Could not request results.")

    def send_to_confirm_screen(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text and text != self.placeholder_text:
            self.confirm_callback(text)
        else:
            messagebox.showwarning("Empty", self.labels[self.language]["warn_empty"])