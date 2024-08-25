from urllib.request import urlopen, Request
from bs4 import BeautifulSoup # type: ignore
from news import News
from stocks import Stock
# import finviz
# from finvizfinance.quote import finvizfinance # type: ignore
# from finvizfinance.news import News
from finvizfinance_.quote import finvizfinance
# import yfinance as yf
from datetime import datetime
import pandas as pd
from finvizAPI import FinViz  #IMPORT FINNHUB API, FinVader API
import time
from typing import Optional
import time
import csv
import requests


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
        
    # def get_past_data(self, s: Stock):
    #     # Fetch historical data using BeautifulSoup
    #     url = f"https://finviz.com/quote.ashx?t={s.stock_name}"
    #     response = requests.get(url) # send a get request to the url
    #     soup = BeautifulSoup(response.content, 'html.parser') # parse the html content of the page

    #     stock_finviz = FinViz() 
    #     all_valumes, all_opens, all_closes, all_dates = stock_finviz.get_all_data('i1', s.stock_name)

    #     # Scrape news data
    #     news_table = soup.find('table', class_='fullview-news-outer') # find the news table
    #     news_df = [] # list to store news data
    #     if news_table: # if the news table is found
    #         for row in news_table.find_all('tr'): 
    #             cols = row.find_all('td') # find all the columns in the row
    #             news_date = cols[0].text.strip() # get the date of the news
    #             news_title = cols[1].a.text.strip() # get the title of the news
    #             news_link = "https://finviz.com/" + cols[1].a['href'] # get the link of the news
    #             news_df.append({'Date': news_date, 'Title': news_title, 'Link': news_link}) # append the news data to the list
        
    #     # Processing news and matching with historical data
    #     for news_item in news_df:
    #         news_date = datetime.strptime(news_item['Date'], '%b-%d-%y %I:%M%p').round("1min")
    #         news_title = news_item['Title']
    #         news_link = news_item['Link']

    #         for date_index in range(len(all_dates)):
    #             if news_date == all_dates[date_index]:
    #                 if len(all_opens) - 1 > date_index:  # if the date is not the last date   
    #                     news = News(news_title, news_date, news_link, 
    #                                 all_opens[date_index - 1], 
    #                                 all_opens[date_index + 1], 
    #                                 all_valumes[date_index - 1],
    #                                 all_valumes[date_index + 1])
    #                     s.add_news(news)                                              
    #                 else: # if the date is the last date
    #                     news = News(news_title, news_date, news_link,
    #                                 all_opens[date_index - 1],
    #                                 all_opens[date_index], 
    #                                 all_valumes[date_index - 1], 
    #                                 all_valumes[date_index])
    #                     s.add_news(news)   
    #                 break     

    #     s.timestamp = all_dates[-1]      
    #     print("Past data has been collected by: ", datetime.now().strftime("%H:%M:%S"))
        
    # def get_date_time(self, url):
        

    
        
    def update_stocks(self) -> list[Stock]:

        stock_finviz = FinViz()
        updated_stocks = {}
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
                updated_stocks[stock] = new_news_lst
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
    


def run_program():
    p = Program([])
    with open("results.csv", "w") as f:
        writer = csv.writer(f)
        # Write headers if needed
        writer.writerow(["Stock Name", "Title", "Date", "Sentiment", "AI Sentiment"])

    while True:
        # The program runs by opening the stocks.txt file, read line by line and put all the stocks on a list.
        with open("stocks.csv", "r") as f:
            reader = csv.reader(f)
            new_stock_list = [row[0].strip() for row in reader]
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
                print("here")
        updated_stocks = p.update_stocks()
        with open("results.csv", "a", newline='') as f:
            writer = csv.writer(f)
            for key, value in updated_stocks.items():
                print(key.stock_name)  
                writer.writerow([key.stock_name])  # Write stock name
                
                for v in value:
                    print(v.title, v.date, v.get_sentiment(), v.get_ai_sentiment(key.stock_name))
                    writer.writerow([v.title, v.date, v.get_sentiment(), v.get_ai_sentiment(key.stock_name)])
        
        
        
        # print(new_stock_list, '-------------------')
        # print([[x.stock_name, x.active] for x in p.stocks])

        time.sleep(5)
    
    




if __name__ == '__main__':
    run_program()

    
    


 


    












