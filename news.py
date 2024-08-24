from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import os
from openai import OpenAI


# API_KEY = 'sk-proj-dQP4LNfKld1ElhklGMCMT3BlbkFJY1zOL3dwtuKFX5fsxJRt'
try:
    with open ('api_key.txt', 'r') as file:
        API_KEY = file.read().strip()
    client = OpenAI(api_key=API_KEY)
except:
    print("API key not found, AI features will not work")
    client = None
    API_KEY = None

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
        
     
    
    def get_ai_sentiment(self, ticker) -> str:
        try:
            assistant = client.beta.assistants.retrieve(assistant_id='asst_shj1iUIPJa5TGGcy6OXuIEEp')
            thread = client.beta.threads.create()
            user_input = str(self.url) + " " + str(ticker)
            message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
            )

            run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            )


            # then, list the messages in the thread
            messages = client.beta.threads.messages.list( 
                thread_id = thread.id,
            ) 

            # Print the messages
            message = messages.data[0]
            # print(message.content)
            # print(message.role + ": " + message.content[0].text.value)
            return message.content[0].text.value
        except:
            return "Wrong API key, In in order to use this feature, please enter a valid API key"
        
        

if __name__ == '__main__':
    news = News('I am really happy', 'timestamp', 'link', 1.0, 2.0, 3.0, 4.0)
    print(news.get_sentiment())
    print(news.get_ai_sentiment())
    
