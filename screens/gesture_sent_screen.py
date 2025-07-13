import tkinter as tk

class GestureSentScreen(tk.Frame):
    def __init__(self, master, translated_text, language="EN"):
        super().__init__(master, bg="#1e1e2f")
        self.master = master
        self.translated_text = translated_text
        self.language = language
        self.labels = self.get_labels()
        self.build_ui()

    def get_labels(self):
        return {
            "EN": {
                "message": f'✅ "{self.translated_text}" sent to robotic hand!',
                "back": "⬅️ Back to Home"
            },
            "ES": {
                "message": f'✅ ¡"{self.translated_text}" enviado a la mano robótica!',
                "back": "⬅️ Volver al Inicio"
            }
        }

    def build_ui(self):
        container = tk.Frame(self, bg="#1e1e2f")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Confirmation message
        tk.Label(
            container,
            text=self.labels[self.language]["message"],
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#1e1e2f",
            wraplength=800,
            justify="center"
        ).pack(pady=(0, 30))

        # Back button
        tk.Button(
            container,
            text=self.labels[self.language]["back"],
            font=("Arial", 16, "bold"),
            bg="white",
            fg="black",
            padx=30,
            pady=10,
            command=self.back_to_home
        ).pack()

    def back_to_home(self):
        # Let App class handle proper screen switching
        self.master.show_welcome_screen()