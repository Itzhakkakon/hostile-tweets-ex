import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
from typing import List
nltk.download("vader_lexicon")
sid = SentimentIntensityAnalyzer()
class DataProcessor:

    @staticmethod
    def convert_to_df(data: List[dict]) -> pd.DataFrame:
        """convert the data to a pandas DataFrame"""
        return pd.DataFrame(data)

    @staticmethod
    def find_first_rarest_word(text: str):
        words = text.split()
        count = Counter(words)
        if not words:
            return None
        min_freq = min(count.values())
        for word in words:
            if count[word] == min_freq:
                return word
        return None

    @staticmethod
    def find_weapons(text: str, weapons:set):
        list_weapons = []
        for word in text.split():
            if word in weapons:
                list_weapons.append(word)
        if len(list_weapons) > 0:
            return list_weapons[0]
        else:
            return None

    @staticmethod
    def get_sentiment(text: str):
        score = sid.polarity_scores(text)['compound']
        if score >= 0.5:
            return "positive"
        elif score <= -0.5:
            return "negative"
        else:
            return "neutral"
