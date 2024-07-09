from urllib.request import urlopen, Request
# from bs4 import BeautifulSoup # type: ignore
from news import News
from stocks import Stock
# import finviz
# from finvizfinance.quote import finvizfinance # type: ignore
# from finvizfinance.news import News
from finvizfinance_.quote import finvizfinance
# import yfinance as yf
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
        self.stocks = []
        for stock in stock_list:
            s = Stock(stock) # object for stock
            self.stocks.append(s)

    
    def get_past_data(self, s: Stock):
        
        stock_finviz = FinViz()
         
        all_valumes, all_opens, all_closes, all_dates = stock_finviz.get_all_data('i1', s.stock_name)

        stock_finvizfinance = finvizfinance(s.stock_name) # object for news
        news_df = stock_finvizfinance.ticker_news() # news dataframe
        for index, row in news_df.iterrows():
            news_title = row['Title']
            news_date = row['Date'].round("1min")
            news_link = row['Link']
            for date_index in range(len(all_dates)):
                if news_date == all_dates[date_index]:
                    if len(all_opens) - 1 > date_index:  # if the date is not the last date   
                        news = News(news_title, news_date, news_link, 
                                    all_opens[date_index - 1], 
                                    all_opens[date_index + 1], 
                                    all_valumes[date_index - 1],
                                    all_valumes[date_index + 1])
                        s.add_news(news)                                              
                    else: # if the date is the last date
                        news = News(news_title, news_date, news_link,
                                    all_opens[date_index - 1],
                                    all_opens[date_index], 
                                    all_valumes[date_index - 1], 
                                    all_valumes[date_index])
                        s.add_news(news)   
                    break     
        s.timestamp = all_dates[-1]      
        print("Past data has been collected by: ", datetime.now().strftime("%H:%M:%S"))
        
    def update_stocks(self) -> list[Stock]:

        stock_finviz = FinViz()
        updated_stocks = []
        for stock in self.stocks:
            if stock.active == False:
                continue
            # print(stock.stock_name, stock.timestamp, '----------------------------')
            stock_finvizfinance = finvizfinance(stock.stock_name) # object for news
            news_df = stock_finvizfinance.ticker_news()
            all_valumes, all_opens, all_closes, all_dates = stock_finviz.get_all_data('i1', stock.stock_name)
            new_news_lst = []
            new_news = None

            for index, row in news_df.iterrows():

                # ------ CREATE A NEW NEWS OBJECT ------
                news_title = row['Title']
                news_date = row['Date'].round("1min")
                news_link = row['Link']
                for date_index in range(len(all_dates)):
                    
                    if news_date == all_dates[date_index]:
                        if len(all_opens) - 1 > date_index:  # if the date is not the last date   
                            new_news = News(news_title, news_date, news_link, 
                                        all_opens[date_index - 1], 
                                        all_opens[date_index + 1], 
                                        all_valumes[date_index - 1],
                                        all_valumes[date_index + 1])                                            
                        else: # if the date is the last date
                            new_news = News(news_title, news_date, news_link,
                                        all_opens[date_index - 1],
                                        all_opens[date_index], 
                                        all_valumes[date_index - 1], 
                                        all_valumes[date_index])
                            
                        # print(new_news.title, new_news.date)
                        break
                # --------------------------------------
                if new_news is None:
                    break
                elif stock.news == []:
                    new_news_lst.append(new_news)
                elif new_news == stock.news[-1]:
                    break
                else:
                    new_news_lst.append(new_news)
                
            stock.news.extend(new_news_lst)
            stock.timestamp = all_dates[-1]
            if new_news_lst:
                print(f"\033[92mNew news added to {stock.stock_name} \033[0m")
                print("new news:", new_news_lst[-1].title, new_news_lst[-1].date)
                updated_stocks.append(stock)
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"\033[95mAll stocks updated by: {current_time}\033[0m")
        return updated_stocks

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
    # start_time = time.time()
    # stock_list = ['NVOS', 'GPS', 'ADRT', 'SMMT', 'WBUY', 'AAPL']
    # super_crowded_stocks = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA", "GOOGL", "META", "NFLX", "AMD", "BA"]
    # p = Program(super_crowded_stocks)
    # p.get_past_data()
    # # print(p.stocks[0].stock_name, p.stocks[0].news[-1].title, p.stocks[0].news[-1].get_sentiment())
    # # for i in p.stocks:
    # #     if i.stock_name == "AAPL":
    # #         for j in i.news:
    # #             print(j.title, j.date, j.get_sentiment())
    # end_time = time.time()
    # print('Time taken:', end_time - start_time)
        

    
    # while True:
        
    #     updated_stocks = p.update_stocks()
    #     if updated_stocks:    
    #         for stock in updated_stocks:
    #             print(stock.stock_name, stock.timestamp, '----------------------------')
    #             score = stock.get_last_news_stock_hype()
    #             print('Last news score:', score, 'for', stock.stock_name, 'at', stock.timestamp, "title: ", stock.news[-1].title)
    #             print(' --> prev news : ', stock.news[-2].title)
    #     # wait for 1 minuts 
    #     time.sleep(60)
    
    p = Program([])
    
    while True:
        # The program runs by opening the stocks.txt file, read line by line and put all the stocks on a list.
        with open("stocks.txt", "r") as f:
            new_stock_list = f.readlines() # the \n should be removed
            new_stock_list = [stock.strip() for stock in new_stock_list]
        for stock in p.stocks:
            if stock.stock_name not in new_stock_list:
                stock.active = False
            else:
                stock.active = True
        for stock in new_stock_list:
            if stock not in [s.stock_name for s in p.stocks]:
                new_stock = Stock(stock)
                p.stocks.append(new_stock)
                p.get_past_data(new_stock)
        print(new_stock_list, '-------------------')
        print([[x.stock_name, x.active] for x in p.stocks])
        
        # p.update_stocks()
        
        time.sleep(4)


 


    














    # for stock in p.stocks:
    #     print(stock.stock_name, stock.timestamp, '----------------------------')
    # #     for news in stock.news:
    # #         print(news.title, news.date, news.price_before, news.price_after, news.valume_before, news.valume_after)
    #     if stock.stock_name == 'SMMT':
    #         print(stock.news)




    # best_stock = p.get_best_stock()
    # print("-------------------------------------------------------------------")
    # print('Currently the best stock to use is', 
    #       best_stock.stock_name, 'with hype score of', round(best_stock.get_stock_hype(), 3))
    # print("-------------------------------------------------------------------")


    # best_stock_today = p.get_best_stock_today()
    # if best_stock_today:
    #     print("-------------------------------------------------------------------")
    #     print('Currently the best stock to use today is', 
    #         best_stock_today.stock_name, 'with hype score of', round(best_stock_today.get_stock_hype_today(), 3))
    #     print("-------------------------------------------------------------------")
    # end_time = time.time()

    # for stock in p.stocks:
    #     print(stock.stock_name, stock.timestamp, '----------------------------')
    #     for news in stock.news:
    #         if news.date.date() == datetime.today().date():
    #             print(news.title, news.date, news.price_before, news.price_after, news.valume_before, news.valume_after)
    # #     for news in stock.news:
    # #         print(news.title, news.date, news.price_before, news.price_after, news.valume_before, news.valume_after)

    # print('Time taken:', end_time - start_time)
