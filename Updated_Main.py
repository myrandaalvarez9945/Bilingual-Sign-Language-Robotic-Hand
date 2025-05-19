from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from deep_translator import GoogleTranslator
import speech_recognition as sr
import serial
import time
import string
import unicodedata
from datetime import datetime
import cv2
import subprocess
import platform
from threading import Thread

current_language = "asl"
arduino = None
silent = False 
camera_running = False

def remove_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')

def clean_text(text):
    text = remove_accents(text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.lower().strip()

gesture_mappings = {
    "asl": {
        "hello": "hello",
        "i love you": "i_love_you",
        "why": "why"
    },
    "lse": {
        "numero uno": "number_one",
        "universidad": "university",
        "escuela": "school"
    }
}

def connect_to_arduino():
    global arduino
    try:
        arduino = serial.Serial('/dev/tty.usbmodem21201', 9600, timeout=1)
        time.sleep(2)
        print("Connected to Arduino!")
        return arduino
    except Exception as e:
        show_error_popup(f"Error connecting to Arduino: {e}")
        return None

def show_error_popup(message):
    layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
    message_label = Label(
        text=message,
        font_size=28,
        halign='center',
        valign='middle',
        color=(1, 0, 0, 1)
    )
    message_label.bind(size=message_label.setter('text_size'))
    layout.add_widget(message_label)

    dismiss_btn = Button(text="OK", size_hint=(None, None), size=(200, 80), font_size=28)
    popup = Popup(
        title="Connection Error",
        content=layout,
        size_hint=(None, None),
        size=(900, 350),
        auto_dismiss=False,
        title_color=(1, 0, 0, 1),
        separator_color=(1, 0, 0, 1)
    )
    dismiss_btn.bind(on_press=popup.dismiss)
    layout.add_widget(dismiss_btn)
    popup.open()

def send_gesture_to_arduino(gesture):
    global arduino
    if arduino:
        print(f"Sending gesture '{gesture}' to Arduino...")
        arduino.write(f"{gesture}\n".encode())
        time.sleep(1)
        response = arduino.readline().decode().strip()
        print(f"[DEBUG] Arduino response: {response}")

        with open("gesture_log.txt", "a") as log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] Gesture sent: {gesture}\n")
    else:
        print("[ERROR] Arduino not connected.")

def translate_text(text, to_language):
    try:
        if to_language == "es":
            return GoogleTranslator(source='en', target='es').translate(text).strip().lower()
        else:
            return GoogleTranslator(source='es', target='en').translate(text).strip().lower()
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def show_help_popup():
    help_text = (
    "HELP / AYUDA\n\n"
    "Welcome to the Bilingual Sign Language Robotic Hand App!\n"
    "¡Bienvenido(a) a la Mano Robótica de Lenguaje de Señas Bilingüe!\n\n"

    "- Options / Opciones:\n"
    "  * Use the camera to detect gestures / Usar la cámara para detectar gestos\n"
    "  * Or type or speak a phrase / O escribir o decir una frase\n\n"

    "- Predefined Gestures / Gestos Predefinidos:\n"
    "  * hello --> hola\n"
    "  * i love you --> te amo\n"
    "  * why --> porque\n\n"

    "- LSE Gestures / Gestos en LSE:\n"
    "  * numero uno --> number_one\n"
    "  * universidad --> university\n"
    "  * escuela --> school\n\n"

    "- Supported Letters / Letras Soportadas:\n"
    "  * A to Y (excluding J and Z)\n"
    "  * No accents, punctuation, or uppercase\n"
    "  * A a Y (sin J ni Z)\n"
    "  * Sin acentos, puntuación, o mayúsculas\n\n"

    "Tip: You can enter full words or phrases and choose whether to translate them.\n"
    "Consejo: Puede escribir frases completas y elegir si desea traducirlas."
)

    content = BoxLayout(orientation='vertical', spacing=20, padding=20)

    # Scrollable label
    scrollview = ScrollView(size_hint=(1, 1))
    label = Label(
        text=help_text,
        font_size=26,
        halign='left',
        valign='top',
        size_hint_y=None
    )
    label.bind(texture_size=lambda instance, value: setattr(label, 'height', value[1]))
    label.text_size = (800, None)
    scrollview.add_widget(label)

    content.add_widget(scrollview)

    # Dismiss button
    dismiss_btn = Button(
        text="OK / Cerrar",
        size_hint=(None, None),
        size=(200, 80),
        font_size=24
    )
    dismiss_btn.bind(on_press=lambda instance: popup.dismiss())
    content.add_widget(dismiss_btn)

    popup = Popup(
        title="Help / Ayuda",
        content=content,
        size_hint=(None, None),
        size=(900, 600),
        auto_dismiss=False
    )
    popup.open()

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)

        layout.add_widget(Widget(size_hint_y=1))  # Spacer above

        label = Label(
            text="Welcome to the Bilingual Sign Language Robotic Hand!\n\n¡Bienvenido(a) a la Mano Robótica de Lenguaje de Señas Bilingüe!",
            font_size=40,
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))
        layout.add_widget(label)

        layout.add_widget(Widget(size_hint_y=None, height=50))

        button_layout = BoxLayout(orientation='horizontal', spacing=50, size_hint_y=None, height=200, padding=[100, 0])

        cam_btn = Button(
            text="Use Camera to Detect Gestures\n(Detect signs using webcam)\n\nUsar Cámara para Detectar Gestos\n(Detectar señas con cámara)",
            font_size=28,
            size_hint=(None, None),
            width=700,
            height=200,
            halign='center',
            valign='middle'
        )
        cam_btn.text_size = (cam_btn.width - 20, None)
        cam_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'camera_input'))

        hand_btn = Button(
            text="Control Robotic Hand with Text/Voice\n(Type or Speak your phrase)\n\nControlar la Mano Robótica con Texto/Voz\n(Escribe o di tu frase)",
            font_size=28,
            size_hint=(None, None),
            width=700,
            height=200,
            halign='center',
            valign='middle'
        )
        hand_btn.text_size = (hand_btn.width - 20, None)
        hand_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'language'))

        button_layout.add_widget(cam_btn)
        button_layout.add_widget(hand_btn)

        layout.add_widget(button_layout)

        # 📍 Add Help button centered beneath the two main buttons
        help_btn_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=100)
        help_btn_container.add_widget(Widget(size_hint_x=1))

        help_btn = Button(
            text="Help / Ayuda",
            font_size=28,
            size_hint=(None, None),
            width=300,
            height=80,
            on_press=lambda x: show_help_popup()
        )
        help_btn_container.add_widget(help_btn)

        help_btn_container.add_widget(Widget(size_hint_x=1))
        layout.add_widget(help_btn_container)

        layout.add_widget(Widget(size_hint_y=1))  # Spacer below

        self.add_widget(layout)

class LanguageSelection(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=60)
        label_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=100)
        label = Label(text="Choose a Sign Language / Elija un Lenguaje de Señas", font_size=48,
                      size_hint=(None, None), height=100, width=1570, halign='center', valign='middle')
        label_layout.add_widget(label)
        layout.add_widget(Widget(size_hint_y=1))
        layout.add_widget(label_layout)
        layout.add_widget(Widget(size_hint_y=None, height=50))
        btn_layout = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=150)
        asl_btn = Button(text="American Sign Language (ASL)", font_size=36)
        asl_btn.bind(on_press=lambda x: self.set_language('asl'))
        lse_btn = Button(text="Lengua de Señas Española (LSE)", font_size=36)
        lse_btn.bind(on_press=lambda x: self.set_language('lse'))
        btn_layout.add_widget(asl_btn)
        btn_layout.add_widget(lse_btn)
        layout.add_widget(btn_layout)
        layout.add_widget(Widget(size_hint_y=1))
        self.add_widget(layout)

    def set_language(self, language):
        global current_language, arduino
        current_language = language
        arduino = connect_to_arduino()
        self.manager.current = 'text_input'

class CameraInputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.status_label = Label(
            text="Press the button below to open the webcam.\nPresione el botón para abrir la cámara.",
            font_size=36,
            halign='center',
            valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        layout.add_widget(self.status_label)

        open_camera_btn = Button(
            text="Open Camera / Abrir Cámara",
            font_size=36,
            size_hint=(None, None),
            width=700,
            height=120
        )
        open_camera_btn.bind(on_press=self.open_camera)
        layout.add_widget(open_camera_btn)

        # 📍 ADD THE HELP BUTTON HERE
        help_btn = Button(
            text="Help / Ayuda",
            font_size=28,
            size_hint=(None, None),
            height=80,
            width=300,
            on_press=lambda x: show_help_popup()
        )
        layout.add_widget(help_btn)

        back_btn = Button(
            text="Back to Home / Volver al Inicio",
            font_size=36,
            size_hint=(None, None),
            width=700,
            height=100,
            on_press=lambda x: setattr(self.manager, 'current', 'welcome')
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def open_camera(self, instance):
        self.status_label.text = "Opening camera... please wait."

        camera_script = '''
import cv2
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow("Camera Feed - Press ESC to Exit", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
'''

        command = ['python3', '-c', camera_script] if platform.system() == 'Darwin' else ['python', '-c', camera_script]
        subprocess.Popen(command)

class TextInputScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.error_label = Label(text="", font_size=36, color=(1, 0, 0, 1), size_hint_y=None, height=50)
        self.text_input = TextInput(hint_text="Enter text/Ingrese texto", font_size=48)
        layout.add_widget(self.text_input)
        layout.add_widget(self.error_label)
        row1 = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=100)
        row2 = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=100)
        clear = Button(text="Clear / Borrar", font_size=48, size_hint=(None, None), height=100, width=500)
        clear.bind(on_press=self.clear_text)
        home = Button(text="Home / Inicio", font_size=48, size_hint=(None, None), height=100, width=500)
        home.bind(on_press=self.go_home)
        next_btn = Button(text="Next / Siguiente", font_size=48, size_hint=(None, None), height=100, width=500)
        next_btn.bind(on_press=self.process_text)
        speak = Button(text="Speak / Hablar", font_size=48, size_hint=(None, None), height=100, width=1570)
        speak.bind(on_press=self.recognize_speech)
        row1.add_widget(clear)
        row1.add_widget(home)
        row1.add_widget(next_btn)
        row2.add_widget(speak)
        layout.add_widget(row1)
        layout.add_widget(row2)
        self.add_widget(layout)

    def recognize_speech(self, instance):
        self.error_label.text = "Listening... / Escuchando..."
        Clock.schedule_once(self._do_recognition, 0.3)

    def _do_recognition(self, dt):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.energy_threshold = 150
                recognizer.dynamic_energy_threshold = True
                self.error_label.text = "Listening... / Escuchando..."
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                self.error_label.text = "Processing... / Procesando..."
                lang = 'en-US' if current_language == 'asl' else 'es-ES'
                result = recognizer.recognize_google(audio, language=lang)
                cleaned = clean_text(result)
                print(f"You said: {cleaned}")
                self.text_input.text = cleaned
                self.error_label.text = "Speech recognized! / ¡Voz reconocida!"
        except sr.WaitTimeoutError:
            self.error_label.text = "No speech detected. / No se detectó voz."
        except sr.UnknownValueError:
            self.error_label.text = "Could not understand audio. / No se entendió el audio."
        except sr.RequestError as e:
            self.error_label.text = f"Recognition error: {e}"
        except Exception as e:
            self.error_label.text = f"[Unexpected Error] {e}"

    def clear_text(self, instance):
        self.text_input.text = ""
        self.error_label.text = ""

    def go_home(self, instance):
        self.text_input.text = ""
        self.error_label.text = ""
        self.manager.current = 'welcome'

    def process_text(self, instance):
        user_text = self.text_input.text.strip()
        if not user_text:
            self.error_label.text = "Enter text, please / Por favor, ingrese texto"
        else:
            self.error_label.text = ""
            self.manager.get_screen('translate').user_text = user_text
            self.manager.current = 'translate'

class TranslationScreen(Screen):
    user_text = ""
    translation_requested = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        layout.add_widget(Widget(size_hint_y=1))
        layout.add_widget(Label(text="Translate text?\n\n¿Traducir texto?", font_size=48,
                                halign='center', valign='middle', size_hint_y=None, height=300))
        layout.add_widget(Widget(size_hint_y=1))
        btns = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=100)
        yes = Button(text="Yes / Sí", font_size=48, size_hint=(None, None), height=250, width=770,
                     on_press=lambda x: self.translate_text(True))
        no = Button(text="No", font_size=48, size_hint=(None, None), height=250, width=770,
                    on_press=lambda x: self.translate_text(False))
        btns.add_widget(yes)
        btns.add_widget(no)
        layout.add_widget(btns)
        self.add_widget(layout)

    def translate_text(self, translate):
        self.translation_requested = translate
        user_text = self.user_text
        translated_screen = self.manager.get_screen('translated')
        translated_screen.original_text = user_text
        if translate:
            translated_text = translate_text(user_text, 'es' if current_language == 'asl' else 'en')
        else:
            translated_text = user_text
        translated_screen.translated_text = translated_text
        self.manager.current = 'translated'
        

class TranslatedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.translated_text = ""
        self.original_text = ""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.original_label = Label(text="", font_size=40, halign='center', valign='middle', color=(0.6,0.6,0.6,1))
        self.translated_label = Label(text="", font_size=48, halign='center', valign='middle')
        layout.add_widget(Widget(size_hint_y=1))
        layout.add_widget(self.original_label)
        layout.add_widget(self.translated_label)
        layout.add_widget(Widget(size_hint_y=1))
        btns = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=20)
        send_btn = Button(text="Send Gesture / Enviar Gesto", font_size=48, size_hint=(None, None), height=250, width=1570,
                          on_press=self.send_gesture)
        btns.add_widget(send_btn)
        layout.add_widget(btns)
        self.add_widget(layout)

    def send_gesture(self, instance):
        confirmation_screen = self.manager.get_screen('confirmation')
        confirmation_screen.gesture_to_send = clean_text(self.original_text)
        self.manager.current = 'confirmation'

    def on_pre_enter(self):
        self.original_label.text = f"Original: {self.original_text}"
        self.translated_label.text = f"Translation: {self.translated_text}"

class ConfirmationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gesture_to_send = ""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.confirmation_label = Label(text="", font_size=48, halign='center', valign='middle', size_hint_y=None, height=800)
        layout.add_widget(self.confirmation_label)
        btns = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=100)
        yes_btn = Button(text="Yes / Sí", font_size=48, size_hint=(None, None), height=250, width=770, on_press=self.send_gesture)
        no_btn = Button(text="No / No", font_size=48, size_hint=(None, None), height=250, width=770, on_press=self.cancel_and_go_home)
        btns.add_widget(yes_btn)
        btns.add_widget(no_btn)
        layout.add_widget(btns)
        self.add_widget(layout)

    def on_pre_enter(self):
        self.confirmation_label.text = f"Do you want to send this gesture to the robotic hand?\n\n{self.gesture_to_send.title()} -> Gesture in {current_language.upper()}"

    def send_gesture(self, instance):
        if not arduino:
            print("[ERROR] Cannot send gesture: Arduino not connected.")
            show_error_popup("Arduino not connected. Please reconnect and try again.")
            return

        gesture_text = clean_text(self.gesture_to_send)
        predefined = gesture_mappings.get(current_language, {})
        words = gesture_text.split()
        handled_words = set()

        print(f"[INFO] Full input: '{gesture_text}'")

        # 1. Check each consecutive group of words to see if it's predefined
        i = 0
        while i < len(words):
            matched = False
            for j in range(len(words), i, -1):  # Try longest phrases first
                phrase = ' '.join(words[i:j])
                if phrase in predefined:
                    print(f"[PREDEFINED] '{phrase}' → '{predefined[phrase]}'")
                    send_gesture_to_arduino(predefined[phrase])
                    handled_words.update(range(i, j))
                    i = j - 1  # skip ahead
                    matched = True
                    break
            i += 1 if not matched else 1

        # 2. Fingerspell anything not matched
        leftover_letters = ''
        for idx, word in enumerate(words):
            if idx not in handled_words:
                leftover_letters += word

        if leftover_letters:
            print(f"[FINGERSPELLING] Leftover letters: '{leftover_letters}'")
            for char in leftover_letters:
                if char.isalpha():
                    print(f" --> Sending letter: '{char}'")
                    send_gesture_to_arduino(char)
                    time.sleep(1)

        send_gesture_to_arduino("reset")
        print("[INFO] Reset command sent to Arduino.")

        # Reset UI
        self.manager.get_screen('text_input').text_input.text = ""
        self.manager.get_screen('text_input').error_label.text = ""
        self.manager.current = 'welcome'

    def cancel_and_go_home(self, instance):
        reset_app_state(self.manager)
        self.manager.current = 'welcome'

def reset_app_state(manager):
    manager.get_screen('text_input').text_input.text = ""
    manager.get_screen('text_input').error_label.text = ""
    t = manager.get_screen('translated')
    t.translated_text = ""
    t.original_text = ""
    t.translated_label.text = ""
    t.original_label.text = ""
    manager.get_screen('translate').translation_requested = False

class SignLanguageApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(CameraInputScreen(name="camera_input"))
        sm.add_widget(LanguageSelection(name="language"))
        sm.add_widget(TextInputScreen(name="text_input"))
        sm.add_widget(TranslationScreen(name="translate"))
        sm.add_widget(TranslatedScreen(name="translated"))
        sm.add_widget(ConfirmationScreen(name="confirmation"))
        return sm

if __name__ == "__main__":
    SignLanguageApp().run()