import re

import joblib
from unidecode import unidecode
from spellchecker import SpellChecker

import config

class Utils:
    def __init__(self):
        self.spell = SpellChecker(language= "pt")
        
        self.pt_stopwords = joblib.load(config.STOPWORDS_PATH)

    def process_text(self, text):
        text = str(text).lower()
        text = re.sub(r"[^\w\s]", " ", text) # Remove pontuação
        text = re.sub(r"\d+", "", text) # Remove os números
        text = self._remove_stopwords(text)
        text = self._correct_text(text)
        text = unidecode(text)
        return text

    def _remove_stopwords(self, text):
        text_tokens = text.split()

        filtered_tokens = [token for token in text_tokens if token not in self.pt_stopwords]

        filtered_text = " ".join(filtered_tokens)
        return filtered_text

    def _correct_text(self, text):
        tokens = text.split()

        corrected_tokens = [
            self.spell.correction(token) if self.spell.correction(token) is not None else token
            for token in tokens
            ]

        corrected_text = " ".join(corrected_tokens)

        return corrected_text