from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from news import News
from stocks import Stock


class Program:
    """ A class to represent a program """

    def __init__(self, stock_list: list) -> None:
        """ Initialize a program

        """
        finviz = 'https://finviz.com/quote.ashx?t='
        new_tables = {}
        for stock in stock_list:
            url = finviz + stock
            req = Request(url, headers={'User-Agent': 'me'})
            response = urlopen(req)
            html = BeautifulSoup(response, 'html.parser')
            new_table = html.find(id='news-table')
            new_tables[stock] = new_table

        # aapl_data = new_tables['AAPL']
        # aapl_rows = aapl_data.findAll('tr')

        self.stocks = []  # list of Stock objects
        for stock, news_table in new_tables.items():
            s = Stock(stock)
            for row in news_table.findAll('tr'):

                title = row.a.get_text()
                date = row.td.text.split(" ")
                link = row.a.get('href')

                if len(date) == 1:
                    time = date[0]
                else:
                    time = date[1]
                    date = date[0]
                k = News(title, time, date, link)
                s.add_news(News(title, time, date, link))
            self.stocks.append(s)

    def get_best_stock(self) -> Stock:
        """ Return the stock with the highest hype level
        """
        best_stock = self.stocks[0]
        for stock in self.stocks:
            if stock.get_stock_hype() > best_stock.get_stock_hype():
                best_stock = stock
        return best_stock


if __name__ == '__main__':
    stock_list = ['AAPL']
    p = Program(stock_list)
    best_stock = p.get_best_stock()
    print('currently the best stock to use is ' best_stock.stock_name, 'with hype score of', best_stock.get_stock_hype())
