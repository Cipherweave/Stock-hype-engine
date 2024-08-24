import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import pytz
from io import StringIO
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer as NLTKSentimentIntensityAnalyzer
import os
from yahoo_fin import news as yahoo_fin_news
from finvizfinance.quote import finvizfinance
import logging

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download necessary NLTK data
nltk.download('vader_lexicon')
nltk.download('movie_reviews')
nltk.download('punkt')

# Function to convert Unix timestamp to human-readable datetime in Eastern Time
def convert_unix_to_datetime(unix_timestamp):
    eastern = pytz.timezone('US/Eastern')
    utc_time = datetime.utcfromtimestamp(unix_timestamp)
    eastern_time = utc_time.replace(tzinfo=pytz.utc).astimezone(eastern)
    return eastern_time

# Function to perform sentiment analysis using VADER
def analyze_vader_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_score = analyzer.polarity_scores(text)
    return sentiment_score['compound']

# Function to perform sentiment analysis using NLTK
def analyze_nltk_sentiment(text):
    sia = NLTKSentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    return sentiment_score['compound']

# Function to store news data in a DataFrame and append to CSV
def store_news_data(ticker, headline, summary, datetime_obj, vader_sentiment, nltk_sentiment, csv_file):
    new_data = {
        'ticker': ticker,
        'headline': headline,
        'summary': summary,
        'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
        'vader_sentiment': vader_sentiment,
        'nltk_sentiment': nltk_sentiment
    }
    df = pd.DataFrame([new_data], columns=['ticker', 'headline', 'summary', 'datetime', 'vader_sentiment', 'nltk_sentiment'])

    # Append data to CSV file
    header = not os.path.isfile(csv_file)
    df.to_csv(csv_file, mode='a', header=header, index=False)

# Function to fetch the latest news for a given stock ticker
def get_latest_news(ticker: str, source: str = 'yf') -> list:
    """
    Fetches the latest news for a given stock ticker using either the yahoo_fin or finviz library.

    :param ticker: The stock ticker symbol.
    :param source: The news source to fetch from. Options are 'yf' for yahoo_fin and 'finviz' for finvizfinance.
                   Default value is 'yf'.
    :return: A list of latest news articles with their titles and URLs.
    """
    news_list = []
    try:
        if source == 'yf':
            logger.info(f'Fetching latest news for {ticker} from Yahoo! Finance')
            news_data = yahoo_fin_news.get_yf_rss(ticker)
            for article in news_data:
                news_list.append({
                    "ticker": ticker,
                    "title": article["title"],
                    "summary": article["summary"],
                    "url": article["link"],
                    "time": article["published"]
                })
        elif source == 'finviz':
            logger.info(f'Fetching latest news for {ticker} from Finviz')
            news_data = finvizfinance(ticker).ticker_news()
            for index, row in news_data.iterrows():
                news_list.append({
                    "ticker": ticker,
                    "title": row["Title"],
                    "summary": None,
                    "url": row["Link"],
                    "time": row["Date"]
                })
        else:
            raise ValueError("Invalid news source. Please choose either 'yf' or 'finviz'.")

        return news_list

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return []

# Function to fetch recent news within the last hour and check for duplicates
def fetch_recent_news(tickers, csv_file, source='yf'):
    eastern = pytz.timezone('US/Eastern')
    now = datetime.now(eastern)
    from_time = now - timedelta(minutes=1)
    print(f"Fetching news for tickers: {tickers}")

    # Load existing headlines from CSV
    if os.path.isfile(csv_file):
        existing_data = pd.read_csv(csv_file)
        existing_headlines = set(existing_data['headline'])
    else:
        existing_headlines = set()

    new_news_found = []

    for ticker in tickers:
        news_list = get_latest_news(ticker, source)
        for article in news_list:
            headline = article["title"]
            if headline and headline not in existing_headlines:
                summary = article.get("summary", "")
                datetime_obj = datetime.strptime(article["time"], '%a, %d %b %Y %H:%M:%S %z').astimezone(eastern) if source == 'yf' else datetime.strptime(article["time"], '%b-%d-%y %I:%M%p').astimezone(eastern)
                if from_time <= datetime_obj <= now:
                    vader_sentiment = analyze_vader_sentiment(summary)
                    nltk_sentiment = analyze_nltk_sentiment(summary)
                    store_news_data(ticker, headline, summary, datetime_obj, vader_sentiment, nltk_sentiment, csv_file)
                    print(f"Fetched new news: {headline}")
                    new_news_found.append((ticker, datetime_obj))
                else:
                    print(f"News item '{headline}' is outside the desired time range. Skipping.")
            else:
                print(f"Skipped duplicate or empty headline news: {headline}")

    return new_news_found

# Function to fetch the data and extract stock prices
def fetch_stock_prices(url):
    response = requests.get(url)
    csv_content = response.content.decode('utf-8')
    df = pd.read_csv(StringIO(csv_content))
    prices = df[["Ticker", "Price"]]
    return prices

# Function to monitor stock prices for 5 minutes from the news release time
def monitor_stock_prices_for_news(news_csv_file, stock_csv_file):
    news_data = pd.read_csv(news_csv_file)

    for index, row in news_data.iterrows():
        ticker = row['ticker']
        news_time_str = row['datetime']
        news_time = datetime.strptime(news_time_str, '%Y-%m-%d %H:%M:%S')

        end_time = news_time + timedelta(minutes=5)
        url = f"https://elite.finviz.com/export.ashx?t={ticker}&auth=9fad0c6b-e75f-4e6d-a4a5-aae9838f9905"
        intervals = 5
        all_prices = []

        for i in range(intervals):
            try:
                current_time = datetime.now()
                if current_time > end_time:
                    break

                prices = fetch_stock_prices(url)
                prices["Time"] = current_time.strftime("%Y-%m-%d %H:%M:%S")
                all_prices.append(prices)
            except KeyError as e:
                print(f"Error: {e}")
            time.sleep(60)

        if all_prices:
            combined_prices = pd.concat(all_prices)
            combined_prices.reset_index(drop=True, inplace=True)
            combined_prices.sort_values(by=["Ticker", "Time"], inplace=True)

            first_prices = combined_prices.groupby('Ticker').first()['Price'].rename('First_Price')
            last_prices = combined_prices.groupby('Ticker').last()['Price'].rename('Last_Price')
            price_changes = last_prices - first_prices
            price_changes_df = price_changes.reset_index().rename(columns={0: 'Price_Change'})

            combined_prices = pd.merge(combined_prices, price_changes_df, on='Ticker')
            combined_prices.to_csv(stock_csv_file, mode='a', header=not os.path.isfile(stock_csv_file), index=False)

# Function to calculate the correlation between price changes and sentiments
def calculate_correlation(news_csv_file, stock_csv_file):
    news_data = pd.read_csv(news_csv_file)
    stock_data = pd.read_csv(stock_csv_file)

    merged_data = pd.merge(news_data, stock_data, on='ticker')
    correlation_vader = merged_data['Price_Change'].corr(merged_data['vader_sentiment'])
    correlation_nltk = merged_data['Price_Change'].corr(merged_data['nltk_sentiment'])

    print(f"Correlation between price change and VADER sentiment: {correlation_vader}")
    print(f"Correlation between price change and NLTK sentiment: {correlation_nltk}")

# Main function to run the monitoring process
def main():
    tickers = ["AAPL", "AMZN", "MSFT", "BYND", "TSLA", "GOOGL", "GOOG", "NVDA", "LMT", "PPG", "BABA", "W", "RCM", "WING", "UBER"]
    news_csv_file = "news_data.csv"
    stock_csv_file = "5_minute_stock_prices.csv"
    session = requests.Session()
    session.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))

    while True:
        now = datetime.now(pytz.timezone('US/Eastern'))
        print(f"Fetching data at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        new_news_list = fetch_recent_news(tickers, news_csv_file, source='yf')  # Set source to 'yf' or 'finviz'
        if new_news_list:
            print(f"Fetched and processed news at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            monitor_stock_prices_for_news(news_csv_file, stock_csv_file)
            calculate_correlation(news_csv_file, stock_csv_file)
        else:
            print(f"No new news found at {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        time.sleep(60)

if __name__ == "__main__":
    main()