from urllib.request import urlopen, Request
from bs4 import BeautifulSoup # type: ignore
from news import News
from stocks import Stock
# import finviz
# from finvizfinance.quote import finvizfinance # type: ignore
# from finvizfinance.news import News
from finvizfinance_.quote import finvizfinance
import yfinance as yf
from datetime import datetime
import pandas as pd
from finvizAPI import FinViz
import time
from typing import Optional



class Program:
    """ A class to represent a program """

    def __init__(self, stock_list: list) -> None:
        """ Initialize a program

        """
        stock_finviz = FinViz()
        self.stocks = []

        for stock in stock_list:    
            
            all_valumes, all_opens, all_closes, all_dates = stock_finviz.get_all_data('i1', stock)

            stock_finvizfinance = finvizfinance(stock) # object for news
            news_df = stock_finvizfinance.ticker_news() # news dataframe
            s = Stock(stock) # object for stock
            for index, row in news_df.iterrows():
                news_title = row['Title']
                news_date = row['Date']
                news_date = news_date.round("1min")
                news_link = row['Link']
                for date_index in range(len(all_dates)):
                    if news_date == all_dates[date_index]:
                        if len(all_opens) - 1 > date_index:     
                            news = News(news_title, news_date, news_link, 
                                        all_opens[date_index - 1], 
                                        all_opens[date_index + 1], 
                                        all_valumes[date_index - 1],
                                        all_valumes[date_index + 1])
                            s.add_news(news)                                              
                        else:
                            news = News(news_title, news_date, news_link,
                                         all_opens[date_index - 1],
                                        all_opens[date_index + 1], 
                                        all_valumes[date_index - 1], 
                                        all_valumes[date_index])
                            s.add_news(news)   
                        break     
            s.timestamp = all_dates[-1]      
            self.stocks.append(s)
        

    def get_best_stock(self) -> Optional[Stock]:
        """ Return the stock with the highest hype level
        """
        if len(self.stocks) == 0:
            print('No stocks found')
            return None
        stocks_with_news = []
        for stock in self.stocks:
            if len(stock.news) > 0:
                stocks_with_news.append(stock)
        if len(stocks_with_news) == 0:
            print('No stocks found with news')
            return None
        best_stock = stocks_with_news[0]
        for stock in stocks_with_news:
            if stock.get_stock_hype() > best_stock.get_stock_hype():
                best_stock = stock
        return best_stock
    
    def get_best_stock_today(self) -> Optional[Stock]:
        """ Return the stock with the highest hype level today
        """
        if len(self.stocks) == 0:
            print('No stocks found')
            return None
        stocks_with_news = []
        for stock in self.stocks:
            for news in stock.news:
                if news.date.date() == datetime.today().date():
                    stocks_with_news.append(stock)
                    break
        if len(stocks_with_news) == 0:
            print('No stocks found with news today')
            return None
        best_stock = stocks_with_news[0]
        for stock in stocks_with_news:
            if stock.get_stock_hype_today() > best_stock.get_stock_hype_today():
                best_stock = stock
        return best_stock

    
# TODO how to get the data with API instead of HTML scraping.   CHECK!
# TODO get the hourly interval Score.
# TODO get the last news score.
# TODO get the todays news score.
# TODO use API script for finviz. Add change in stock attribute for every news atribute    CHECK!
# TODO pyqt5 (Package) for visualazion. tableau (Package)


if __name__ == '__main__':
    start_time = time.time()
    stock_list = ['NVOS', 'GPS', 'ADRT', 'SMMT', 'WBUY', 'AAPL']
    p = Program(stock_list)
    best_stock = p.get_best_stock()
    # print("-------------------------------------------------------------------")
    # print('Currently the best stock to use is', 
    #       best_stock.stock_name, 'with hype score of', round(best_stock.get_stock_hype(), 3))
    # print("-------------------------------------------------------------------")


    best_stock_today = p.get_best_stock_today()
    if best_stock_today:
        print("-------------------------------------------------------------------")
        print('Currently the best stock to use today is', 
            best_stock_today.stock_name, 'with hype score of', round(best_stock_today.get_stock_hype_today(), 3))
        print("-------------------------------------------------------------------")
    end_time = time.time()

    # for stock in p.stocks:
    #     print(stock.stock_name, stock.timestamp, '----------------------------')
    #     for news in stock.news:
    #         if news.date.date() == datetime.today().date():
    #             print(news.title, news.date, news.price_before, news.price_after, news.valume_before, news.valume_after)
    #     for news in stock.news:
    #         print(news.title, news.date, news.price_before, news.price_after, news.valume_before, news.valume_after)

    print('Time taken:', end_time - start_time)
