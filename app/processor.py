import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter
import re

# dwl vader_lexicon
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')


class DataProcessor:

    def __init__(self, weapons_file_path='../data/weapons.txt'):
        self.sid = SentimentIntensityAnalyzer()
        self.weapons_list = self._load_weapons(weapons_file_path)

    def _load_weapons(self, file_path):
        """load the weapons list from a file"""
        try:
            with open(file_path, 'r') as f:
                # read the file line by line
                return [line.strip().lower() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"worning:wheapons file not found: {file_path}")
            return []

    def _find_rarest_word(self, df):
        if df.empty:
            print("no data to process")
            return pd.Series()
        print("finding rarest word...")
        print(df.columns)
        all_words = ' '.join(df['original_text'].dropna()).lower().split()
        # count the frequency of each word
        word_counts = Counter(all_words)

        def get_rarest_for_text(text):
            if not isinstance(text, str) or not text.strip():
                return ""

            words_in_text = list(set(text.lower().split()))
            rarest_word = None
            min_count = float('inf')

            for word in words_in_text:
                if word_counts[word] < min_count:
                    min_count = word_counts[word]
                    rarest_word = word
            return rarest_word

        return df['original_text'].apply(get_rarest_for_text)

    def _get_sentiment(self, text):
        """calculate the sentiment of the text"""
        if not isinstance(text, str):
            return "neutral"

        score = self.sid.polarity_scores(text)['compound']

        if score >= 0.5:
            return "positive"
        elif score <= -0.5:
            return "negative"
        else:
            return "neutral"

    def _find_weapons(self, text):
        """find the first weapon in the text."""
        if not isinstance(text, str):
            return ""
        text_lower = text.lower()
        weapons_found = []

        for weapon in self.weapons_list:
            # use regex to check if the weapon is in the text
            if re.search(r'\b' + re.escape(weapon) + r'\b', text_lower):
                weapons_found.append(weapon)
        return ", ".join(weapons_found)

    def process_data(self, df):
        """
        the main function of the class. process the data and return a DataFrame.
        """
        if df.empty:
            return df

        processed_df = df.copy()

        # 1. finding the rarest word
        processed_df['rarest_word'] = self._find_rarest_word(processed_df)

        # 2. finding the sentiment
        processed_df['sentiment'] = processed_df['original_text'].apply(self._get_sentiment)

        # 3. finding the weapons name
        processed_df['weapons_detected'] = processed_df['original_text'].apply(self._find_weapons)

        return processed_df