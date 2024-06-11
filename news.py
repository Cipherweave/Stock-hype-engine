from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime


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
    date: str
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
        return f"{self.timestamp} {self.title} {self.link}"

    def get_sentiment(self) -> float:
        """ Return the sentiment of the news article

        >>> n = News('I am really happy', 'timestamp', 'date', 'link')
        >>> n.get_sentiment()
        0.6115
        >>> n = News('I am really sad', 'timestamp', 'date', 'link')
        >>> n.get_sentiment()
        -0.5256
        >>> n = News('Move Over, Apple! Nvidia Stock Is '\
        'Coming for the No. 2 Spot.', 'timestamp', 'date', 'link')
        >>> n.get_sentiment()
        -0.3595
        """
        sia = SentimentIntensityAnalyzer()
        return (sia.polarity_scores(self.title)['compound'] + 1) / 2



