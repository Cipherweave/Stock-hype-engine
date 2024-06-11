        # finviz = 'https://elite.finviz.com/quote.ashx?t='
        # new_tables = {}
        # for stock in stock_list:
        #     url = finviz + stock
        #     req = Request(url, headers={'User-Agent': 'me'})
        #     response = urlopen(req)
        #     html = BeautifulSoup(response, 'html.parser')
        #     new_table = html.find(id='news-table')
        #     new_tables[stock] = new_table

        # self.stocks = []  # list of Stock objects
        # for stock, news_table in new_tables.items():
        #     s = Stock(stock)
        #     for row in news_table.findAll('tr'):

        #         title = row.a.get_text()
        #         date_time = row.td.text.split(" ")
        #         link = row.a.get('href')

        #         if len(date_time) == 1:
        #             time = date_time[0]
        #         else:
        #             time = date_time[1]
        #             date = date_time[0]
        #         s.add_news(News(title, time, date, link))
        #     self.stocks.append(s)


#----------------------------------------------------------

# news_objects = news_df.apply(lambda row: News(row['Title'], row['Date'], row['Link'], 1, 1), axis=1)


#----------------------------------------------------------