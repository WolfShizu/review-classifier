import re
import nltk
nltk.download("stopwords")

from nltk.corpus import stopwords
from unidecode import unidecode
from spellchecker import SpellChecker


class Utils:
    def __init__(self):
        self.data_frame_length = 0
        self.invalid_data_count = 0
        self.total_words = 0
        self.total_texts = 0

        self.pt_stopwords = set(stopwords.words("portuguese"))
        self.pt_stopwords = self.pt_stopwords - {
            "nao", "mas", "porem", "nunca", "jamais", "entretanto", "ate", "talvez", "foi", "tinha", "era", "apenas"
        }

        self.spell = SpellChecker(language= "pt")

    def map_reviews(self, review):
        if "POSITIVO" in review and "NEGATIVO" in review or "NEUTRO" in review:
            return 0.5
        
        if "POSITIVO" in review:
            return 1
        
        if "NEGATIVO" in review:
            return 0 


    def remove_invalid_data(self, topic):
        if "INADEQUADA" in topic:
            self.invalid_data_count += 1
            return False
        return True

    def clear_text(self, text):
        text = str(text).lower()
        text = re.sub(r"[^\w\s]", " ", text) # Remove pontuação
        text = re.sub(r"\d+", "", text) # Remove os números
        text = self._remove_stopwords(text)
        return text
    
    def remove_accent(self, text):
        text = unidecode(text)
        return text
    
    def correct_df_text(self, data_frame):
        self.data_frame_length = len(data_frame)
        data_frame["full_text"].apply(self._correct_text)
        return data_frame

    def _correct_text(self, text):
        tokens = text.split()

        corrected_tokens = []

        for token in tokens:
            corrected_token = self.spell.correction(token)

            if corrected_token is None:
                corrected_token = token

        self.total_texts += 1
        self.total_words += len(tokens)

        corrected_text = " ".join(corrected_tokens)

        self._update_progress_bar()
        return corrected_text

    def _update_progress_bar(self):
        length = 30

        percent = self.total_texts / self.data_frame_length
        filled_length = int(length * percent)

        bar = "#" * filled_length + "-" * (length - filled_length)

        print(f"[{bar}] {percent*100:.1f}% | Total de textos: {self.total_texts} | Total de palavras: {self.total_words}", end= "\r")
        

    def _remove_stopwords(self, text):
        text_tokens = text.split()

        filtered_tokens = [token for token in text_tokens if token not in self.pt_stopwords]

        filtered_text = " ".join(filtered_tokens)
        return filtered_text
    