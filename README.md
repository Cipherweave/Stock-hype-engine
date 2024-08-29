# Stock-hype-engine

An engine that represent how much potential a stock have for traders to trade.
it autmaticly retreves news from finviz website and use NLTK and custom Open Ai assitant to analize it and show it to you.

## INSTALLMENTS

- pip install nltk
  put this on the code and run it:
  import nltk
  nltk.download('vader_lexicon')
- pip install openai

# Use

Run visuals to see the interface.

or:
put the tickers you want in the stocks.csv line by line.
make sure you have your Open Ai API key paced in the api_key.txt
run main.py
you the output would be in results.csv

So you can connect your application to eather change the stocks.csv and tickers.
Also you can connect your appliaction to retreve from results.py
