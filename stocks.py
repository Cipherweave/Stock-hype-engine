class Stock:
    """ Class to store stock data """

    def __init__(self, stock_name: str) -> None:
        """ Initialize a stock object
        """
        self.timestamp = None
        self.stock_name = stock_name
        self.news = []

    def __str__(self) -> str:
        """ Return a string representation
        """
        return f"{self.stock_name} {self.news}"

    def add_news(self, news: object) -> None:
        """ Add news to the news list
        """
        self.news.append(news)

    def get_news(self) -> list:
        """ Return the news list
        """
        return self.news

    def get_stock_hype(self) -> float:
        """ Return the hype level of the stock
        """
        if len(self.news) == 0:
            return 0
        total = 0
        for news in self.news:
            total += news.get_sentiment()
        return total / len(self.news)


    def get_stock_hype_today(self) -> float:
        """ Return the hype level of the stock today
        """
        if len(self.news) == 0:
            return 0
        total = 0
        count = 0
        for news in self.news:
            if news.date.date() == self.timestamp.date():
                total += news.get_sentiment()
                count += 1
        if count == 0:
            return 0
        return total / count


