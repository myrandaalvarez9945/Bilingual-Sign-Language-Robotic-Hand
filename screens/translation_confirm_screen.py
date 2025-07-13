import tkinter as tk

class TranslationConfirmScreen(tk.Frame):
    def __init__(self, master, original_text, on_yes, on_no, language="EN"):
        super().__init__(master, bg="#1e1e2f")
        self.master = master
        self.original_text = original_text
        self.on_yes = on_yes
        self.on_no = on_no
        self.language = language
        self.labels = self.get_labels()
        self.build_ui()

    def get_labels(self):
        return {
            "EN": {
                "question": "Would you like to translate this text?",
                "yes": "✅",
                "no": "❌"
            },
            "ES": {
                "question": "¿Quieres traducir este texto?",
                "yes": "✅",
                "no": "❌"
            }
        }

    def build_ui(self):
        container = tk.Frame(self, bg="#1e1e2f")
        container.place(relx=0.5, rely=0.5, anchor="center")

        question = tk.Label(
            container,
            text=self.labels[self.language]["question"],
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1e1e2f"
        )
        question.pack(pady=(0, 10))

        original = tk.Label(
            container,
            text=f'"{self.original_text}"',
            font=("Arial", 16),
            fg="white",
            bg="#1e1e2f"
        )
        original.pack(pady=(0, 20))

        btn_frame = tk.Frame(container, bg="#1e1e2f")
        btn_frame.pack()

        yes_btn = tk.Button(
            btn_frame,
            text=self.labels[self.language]["yes"],
            font=("Arial", 20, "bold"),
            fg="black",
            bg="white",
            width=8,
            height=2,
            command=lambda: self.on_yes(self.original_text)
        )
        yes_btn.grid(row=0, column=0, padx=20)

        no_btn = tk.Button(
            btn_frame,
            text=self.labels[self.language]["no"],
            font=("Arial", 20, "bold"),
            fg="black",
            bg="white",
            width=8,
            height=2,
            command=lambda: self.on_no(self.original_text)
        )
        no_btn.grid(row=0, column=1, padx=20)