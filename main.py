import tkinter as tk
from screens.welcome_screen import WelcomeScreen
from screens.text_input_screen import TextInputScreen
from screens.translation_confirm_screen import TranslationConfirmScreen
from screens.translated_screen import TranslatedScreen
from screens.gesture_sent_screen import GestureSentScreen
from utils.arduino import send_to_arduino
from utils.translation import translate_to_sign_language

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bilingual Sign Language Robotic Hand")
        self.geometry("1100x650")
        self.configure(bg="#1e1e2f")
        self.language = "EN"
        self.attributes('-alpha', 0.0)
        self.fade_in()

        self.current_screen = None
        self.show_welcome_screen()

    def fade_in(self):
        alpha = self.attributes('-alpha')
        if alpha < 1.0:
            alpha += 0.05
            self.attributes('-alpha', alpha)
            self.after(50, self.fade_in)

    def switch_screen(self, new_screen_class, *args, **kwargs):
        if self.current_screen:
            self.current_screen.destroy()
        self.current_screen = new_screen_class(self, *args, **kwargs)
        self.current_screen.pack(fill="both", expand=True)

    def show_welcome_screen(self):
        self.switch_screen(
            WelcomeScreen,
            self.show_text_input_screen,
            self.language,
            self.toggle_language
        )

    def show_text_input_screen(self):
        self.switch_screen(
            TextInputScreen,
            self.show_welcome_screen,
            self.handle_send,
            self.language
        )

    def handle_send(self, text):
        self.switch_screen(
            TranslationConfirmScreen,
            original_text=text,
            on_yes=self.handle_translate_yes,
            on_no=self.handle_translate_no,
            language=self.language
        )

    def handle_translate_yes(self, original_text):
        translated = translate_to_sign_language(original_text, language=self.language)
        self.show_translated_screen(original=original_text, translated=translated)

    def handle_translate_no(self, original_text):
        self.show_translated_screen(original=original_text, translated=None)

    def show_translated_screen(self, original, translated):
        self.switch_screen(
            TranslatedScreen,
            original=original,
            translated=translated,
            go_back_callback=self.show_text_input_screen,
            language=self.language
        )

    def toggle_language(self, new_lang):
        self.language = new_lang
        print(f"Language set to: {new_lang}")  # Removed emoji to prevent UnicodeEncodeError

    def send_gesture(self, translated_text):
        send_to_arduino(translated_text)
        self.show_gesture_sent_screen(translated_text)

    def show_gesture_sent_screen(self, translated_text):
        self.switch_screen(
            GestureSentScreen,
            translated_text=translated_text,
            language=self.language
        )

if __name__ == "__main__":
    app = App()
    app.mainloop()