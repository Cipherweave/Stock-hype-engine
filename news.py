from nltk.sentiment.vader import SentimentIntensityAnalyzer


class News:
    """ A class to represent a news article """

    def __init__(self, title: str, timestamp: str, date: str, link: str) -> None:
        """ Initialize a news article

        """
        self.title = title
        self.timestamp = timestamp
        self.date = date
        self.link = link

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



