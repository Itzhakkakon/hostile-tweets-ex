import re
import pandas as pd
from app.dependencies import data_loader
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


tweets = data_loader.get_all_data()


def Finding_the_rarest_word_in_any_text(tweets: pd.DataFrame) -> str:

    all_words = []

    for text in tweets['text']:
        words = text.split()
        all_words.extend(words)

    word_counts = pd.Series(all_words).value_counts()
    rarest_word = word_counts.idxmin()

    return rarest_word


def _get_sentiment(tweets):
    nltk.download('vader_lexicon')  # Compute sentiment labels
    tweet = 'Skillcate is a great Youtube Channel to learn Data Science'

    score = SentimentIntensityAnalyzer().polarity_scores(tweet)

    if score['compound'] >= 0.5:
        return "positive"
    elif score['compound'] <= -0.5:
        return "negative"
    else:
        return "neutral"

 def _find_weapons(self, text):
        """find the first weapon in the text."""
        if not isinstance(text, str):
            return ""

        text_lower = text.lower()
        for weapon in self.weapons_list:
            # use regex to check if the weapon is in the text
            if re.search(r'\b' + re.escape(weapon) + r'\b', text_lower):
                return weapon
        return ""
