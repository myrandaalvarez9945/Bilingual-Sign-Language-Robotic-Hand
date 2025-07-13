import tkinter as tk

class WelcomeScreen(tk.Frame):
    def __init__(self, master, open_text_screen, language="EN", lang_toggle_callback=None):
        super().__init__(master, bg="#1e1e2f")
        self.master = master
        self.language = language
        self.lang_toggle_callback = lang_toggle_callback
        self.open_text_screen = open_text_screen

        self.texts = {
            "EN": {
                "title": "Welcome to the Bilingual Sign Language Robotic Hand!",
                "subtitle": "¡Bienvenido(a) a la Mano Robótica de Lenguaje de Señas Bilingüe!",
                "cam_btn": "📸 Use Camera to Detect Gestures\n\nUsar Cámara para Detectar Gestos",
                "text_btn": "🗣️ Control Robotic Hand with Text/Voice\n\nControlar la Mano Robótica con Texto/Voz",
                "help_btn": "❓ Help / Ayuda",
                "lang_btn": "🌐 Español",
                "help_title": "Help / Ayuda",
                "close": "Close / Cerrar",
                "help_text": (
                    "📸 Use the camera to detect gestures in real-time.\n"
                    "🖋️ Or control the robotic hand with text or voice.\n\n"
                    "📚 Predefined Gestures:\n"
                    "   - hello / hola\n"
                    "   - i love you / te amo\n"
                    "   - why / porque\n\n"
                    "🇪🇸 Spanish Sign Language (LSE) Gestures:\n"
                    "   - numero uno / number one\n"
                    "   - universidad / university\n"
                    "   - escuela / school\n\n"
                    "🔠 Supported Letters: A - Y (excluding J & Z)\n"
                    "   - No accents or punctuation.\n\n"
                    "✨ Tip: You can enter phrases or single words."
                )
            },
            "ES": {
                "title": "¡Bienvenido(a) a la Mano Robótica de Lenguaje de Señas Bilingüe!",
                "subtitle": "Welcome to the Bilingual Sign Language Robotic Hand!",
                "cam_btn": "📸 Usar Cámara para Detectar Gestos\n\nUse Camera to Detect Gestures",
                "text_btn": "🗣️ Controlar la Mano Robótica con Texto/Voz\n\nControl Robotic Hand with Text/Voice",
                "help_btn": "❓ Ayuda / Help",
                "lang_btn": "🌐 English",
                "help_title": "Ayuda / Help",
                "close": "Cerrar / Close",
                "help_text": (
                    "📸 Usa la cámara para detectar gestos en tiempo real.\n"
                    "🖋️ O controla la mano robótica con texto o voz.\n\n"
                    "📚 Gestos predefinidos:\n"
                    "   - hola / hello\n"
                    "   - te amo / i love you\n"
                    "   - porque / why\n\n"
                    "🇺🇸 Gestos del Lenguaje de Señas Español (LSE):\n"
                    "   - number one / numero uno\n"
                    "   - university / universidad\n"
                    "   - school / escuela\n\n"
                    "🔠 Letras compatibles: A - Y (excluyendo J y Z)\n"
                    "   - Sin acentos ni puntuación.\n\n"
                    "✨ Consejo: Puedes escribir frases o palabras individuales."
                )
            }
        }

        self.create_widgets()
        self.update_language()

    def create_widgets(self):
        self.container = tk.Frame(self, bg="#1e1e2f")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.title_label = tk.Label(self.container, font=("Arial", 22, "bold"),
                                    bg="#1e1e2f", fg="white", justify="center")
        self.title_label.pack(pady=(0, 40))

        self.button_frame = tk.Frame(self.container, bg="#1e1e2f")
        self.button_frame.pack(pady=20)

        self.cam_btn = tk.Button(self.button_frame, font=("Arial", 16, "bold"), bg="#4fc3f7",
                                 fg="black", wraplength=260, width=38, height=6, bd=3,
                                 relief="raised", command=self.open_camera_screen)
        self.cam_btn.grid(row=0, column=0, padx=30)

        self.text_btn = tk.Button(self.button_frame, font=("Arial", 16, "bold"), bg="#4fc3f7",
                                  fg="black", wraplength=260, width=38, height=6, bd=3,
                                  relief="raised", command=self.open_text_screen)
        self.text_btn.grid(row=0, column=1, padx=30)

        self.help_btn = tk.Button(self.container, font=("Arial", 14, "bold"), bg="#03dac6",
                                  fg="black", width=20, height=2, bd=2, relief="raised",
                                  command=self.show_help)
        self.help_btn.pack(pady=(30, 10))

        self.lang_btn = tk.Button(self.container, font=("Arial", 12, "bold"), bg="#757575",
                                  fg="black", width=15, command=self.toggle_language)
        self.lang_btn.pack()

    def update_language(self):
        t = self.texts[self.language]
        self.title_label.config(text=f"{t['title']}\n\n{t['subtitle']}")
        self.cam_btn.config(text=t['cam_btn'])
        self.text_btn.config(text=t['text_btn'])
        self.help_btn.config(text=t['help_btn'])
        self.lang_btn.config(text=t['lang_btn'])

    def toggle_language(self):
        self.language = "ES" if self.language == "EN" else "EN"
        if self.lang_toggle_callback:
            self.lang_toggle_callback(self.language)
        self.update_language()

    def open_camera_screen(self):
        print("🎥 Camera detection screen placeholder")

    def show_help(self):
        help_window = tk.Toplevel(self)
        help_window.title(self.texts[self.language]["help_title"])
        help_window.geometry("750x500")
        help_window.configure(bg="#1e1e2f")
        help_window.attributes('-alpha', 0.0)
        self.fade_in_help(help_window)

        tk.Label(help_window, text=self.texts[self.language]["help_title"],
                 font=("Arial", 20, "bold"), bg="#1e1e2f", fg="white").pack(pady=(20, 10))

        tk.Label(help_window, text=self.texts[self.language]["help_text"],
                 font=("Arial", 14), bg="#1e1e2f", fg="white", justify="center",
                 wraplength=700).pack(pady=(0, 30), padx=40)

        tk.Button(help_window, text=self.texts[self.language]["close"],
                  font=("Arial", 14, "bold"), bg="#03dac6", fg="#000000",
                  activebackground="#018786", activeforeground="white",
                  width=18, height=2, bd=2, relief="ridge", cursor="hand2",
                  command=help_window.destroy).pack()

    def fade_in_help(self, window):
        alpha = window.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.05
            window.attributes('-alpha', alpha)
            window.after(30, lambda: self.fade_in_help(window))