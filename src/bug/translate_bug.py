from googletrans import Translator
from googletrans import LANGUAGES
from src.models import MessageModel
import random


class TranslateBug:
    def __init__(self):
        self.language_dict, self.language_list = self.generate_language_data()

    def translate_to(self, message: MessageModel, language: str):
        language_code = self.language_dict[language]["code"]
        translator = Translator()
        message.body = translator.translate(message.body, dest=language_code).text

    def translate_to_random_language(self, message: MessageModel):
        self.translate_to(message, self.choose_random_language())

    def choose_random_language(self):
        return random.choice(self.language_list)

    def generate_language_data(self):
        language_dict = {}
        language_list = []
        for key, value in LANGUAGES.items():
            language_dict[value] = {"code": key, "name": value}
            language_list.append(value)
        return language_dict, language_list
