import pyperclip
from pynput import keyboard
from string import capwords
import tkinter as tk
import spacy

import warnings
warnings.filterwarnings("ignore", "You are using `torch.load` with `weights_only=False`*.")

class ClipboardManager:
    @staticmethod
    def get_clipboard_text():
        """Retrieve text from the clipboard."""
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"Error: {e}")
            return None

class TextProcessor:
    def __init__(self):
        self.nlp = spacy.load("de_dep_news_trf")

    def process_text(self, text):
        word = text.strip()
        word = capwords(word)
        article = self.find_article(word)
        return article

    def find_article(self, word):
        article = self.search_article(word)
        if article:
            return article

        word_lower = word.lower()
        if word_lower == "t-shirt":
            return "das T-Shirt"
        elif word_lower == "u-bahn":
            return "die U-Bahn"
        else:
            return f"No article found for: {word}"

    def search_article(self, word):
        doc = self.nlp(word)
        for token in doc:
            if token.pos_ == "NOUN":
                noun = token.text
                if "Gender=Masc" in token.morph:
                    return f"der {noun}"
                elif "Gender=Fem" in token.morph:
                    return f"die {noun}"
                elif "Gender=Neut" in token.morph:
                    return f"das {noun}"
        return None

class ArticleFinderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Article Finder")
        self.root.geometry("600x300")
        self.label = None
        self.text_processor = TextProcessor()
        self.listener = None

    def show_message(self, message):
        """Display the message in a window."""
        if self.label:
            self.label.config(text=message)
        else:
            self.label = tk.Label(self.root, text=message, font=("Helvetica", 20))
            self.label.pack(expand=True)
        self.root.update()

    def handle_selected_text(self):
        """Handle the selected text."""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.root.attributes('-topmost', True)
        self.root.attributes('-topmost', False)

        text = ClipboardManager.get_clipboard_text()
        if text:
            article = self.text_processor.process_text(text)
            self.show_message(article)
        else:
            print("No text found in clipboard.")

    def run_tkinter(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()

    def on_activate(self):
        """Callback for hotkey activation."""
        self.handle_selected_text()

    def for_canonical(self, f):
        return lambda k: f(self.listener.canonical(k))

    def start(self):
        """Start the application."""
        with keyboard.GlobalHotKeys({
            '<ctrl>+c+x': self.on_activate
        }) as self.listener:
            self.run_tkinter()

if __name__ == "__main__":
    app = ArticleFinderApp()
    app.start()