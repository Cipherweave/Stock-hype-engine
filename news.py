from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import os
from openai import OpenAI



class News:
    """ A class to represent a news article
     
    ==== Attributes ====
    title: title of the news article
    date: date of the news article
    link: link to the news article
    date: date of the news article
    price_before: price of the stock one minute before the news article
    price_after: price of the stock one minute after the news article
    valume_before: volume of the stock one minute before the news article
    valume_after: volume of the stock one minute after the news article
    """
    title: str
    link: str
    date: datetime
    price_before: float
    price_after: float
    valume_before: float
    valume_after: float

    def __init__(self, title: str, date: datetime, link: str, price_before: float, price_after: float, valume_before: float, valume_after: float) -> None:
        """ Initialize a news article

        """
        self.title = title
        self.date = date
        self.link = link
        self.price_before = price_before
        self.price_after = price_after
        self.valume_before = valume_before
        self.valume_after = valume_after

    def __str__(self) -> str:
        """ Return a string representation

        """
        return f"{self.date} {self.title} {self.link}"
    
    def __eq__(self, value: object) -> bool:
        """ Return True if the news articles are equal
        >>> n = News('title', 'date', 'link', 1.0, 2.0, 3.0, 4.0)
        >>> n == News('title', 'date', 'link', 1.0, 2.0, 3.0, 4.0)
        True
        """
        if not isinstance(value, News):
            return False
        return self.title == value.title and self.date.round("1min") == value.date.round("1min") and self.link == value.link

    def get_sentiment(self) -> float:
        """ Return the sentiment of the news article

        # >>> n = News('I am really happy', 'timestamp', 'date', 'link')
        # >>> n.get_sentiment()
        # 0.6115
        # >>> n = News('I am really sad', 'timestamp', 'date', 'link')
        # >>> n.get_sentiment()
        # -0.5256
        # >>> n = News('Move Over, Apple! Nvidia Stock Is '\
        # 'Coming for the No. 2 Spot.', 'timestamp', 'date', 'link')
        # >>> n.get_sentiment()
        # -0.3595
        """
        sia = SentimentIntensityAnalyzer()
        return (sia.polarity_scores(self.title)['compound'] + 1) / 2
        
     
    
    def get_ai_sentiment(self):
        # openai.api_key = 'sk-proj-O9DC1FpGLgawsyf8UwvmT3BlbkFJinkwlq7GTDz3RiWF1yMb'
        client = OpenAI(
            # This is the default and can be omitted
            api_key=os.environ.get("sk-proj-O9DC1FpGLgawsyf8UwvmT3BlbkFJinkwlq7GTDz3RiWF1yMb"),
        )
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model="gpt-3.5-turbo",
        )
        sentiment_score = float(chat_completion['choices'][0]['text'].strip())
        return sentiment_score


if __name__ == '__main__':
    news = News('I am really happy', 'timestamp', 'link', 1.0, 2.0, 3.0, 4.0)
    print(news.get_sentiment())
    print(news.get_ai_sentiment())
    
