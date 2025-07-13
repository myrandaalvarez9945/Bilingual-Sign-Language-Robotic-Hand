import tkinter as tk
from screens.gesture_sent_screen import GestureSentScreen

class TranslatedScreen(tk.Frame):
    def __init__(self, master, original, translated, go_back_callback, language="EN"):
        super().__init__(master, bg="#1e1e2f")
        self.master = master
        self.original = original
        self.translated = translated
        self.go_back_callback = go_back_callback
        self.language = language
        self.labels = self.get_labels()
        self.build_ui()

    def get_labels(self):
        return {
            "EN": {
                "title": "Translation Result",
                "original": "📝 Original:",
                "translated": "🤖 Translation:",
                "send": "✋ Send Gesture to Hand",
                "back": "⬅️ Back"
            },
            "ES": {
                "title": "Resultado de la Traducción",
                "original": "📝 Original:",
                "translated": "🤖 Traducción:",
                "send": "✋ Enviar Gesto a la Mano",
                "back": "⬅️ Atrás"
            }
        }

    def build_ui(self):
        container = tk.Frame(self, bg="#1e1e2f")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        tk.Label(
            container,
            text=self.labels[self.language]["title"],
            font=("Arial", 26, "bold"),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=(0, 30))

        # Original Text
        tk.Label(
            container,
            text=f'{self.labels[self.language]["original"]} {self.original}',
            font=("Arial", 20),
            fg="white",
            bg="#1e1e2f"
        ).pack(pady=10)

        # Decide which sign language to label
        sign_lang = "LSE" if self.language == "EN" else "ASL"

        # Translated Text
        if self.translated:
            display_text = self.translated.split(":")[-1].strip()  # Extract actual translation
            tk.Label(
                container,
                text=f'{self.labels[self.language]["translated"]} {sign_lang}: {display_text}',
                font=("Arial", 20, "bold"),
                fg="#00e5c0",
                bg="#1e1e2f"
            ).pack(pady=10)

        # Send Gesture Button
        tk.Button(
            container,
            text=self.labels[self.language]["send"],
            font=("Arial", 18, "bold"),
            bg="white",
            fg="black",
            padx=30,
            pady=10,
            command=self.send_gesture
        ).pack(pady=(30, 15))

        # Back Button
        tk.Button(
            container,
            text=self.labels[self.language]["back"],
            font=("Arial", 14, "bold"),
            bg="white",
            fg="black",
            padx=20,
            pady=5,
            command=self.go_back_callback
        ).pack()

    def send_gesture(self):
        message = self.translated if self.translated else self.original
        self.master.send_gesture(message)