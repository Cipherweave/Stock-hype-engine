from yahoo_fin import news as yahoo_fin_news

news_data = yahoo_fin_news.get_yf_rss('TSLA')
for article in news_data:
    print(article["title"])