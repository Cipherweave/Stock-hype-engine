# Stock-hype-engine

An engine that represent how much potential a stock have for traders to trade.
it autmaticly retreves news from finviz website and use NLTK and custom Open Ai assitant to analize it and show it to you.

## INSTALLMENTS

- pip install nltk
- pip install openai
- put this on the code and run it:
  import nltk
  nltk.download('vader_lexicon')

# Use
All the files are directly or indirectly used in main.py so please dont change anything unless you like ehnhance it. 

main.py: Runs the main application which takes stocks.csv as input and gives results.csv as output.
visuals.py: Runs the main.py but with gui.
stocks.py: Stock object.
news.py: News object.
qoute.py: An overwriten file from Finfizfinance library that extracts news from finance websites. 
finvizAPI.py: I use this file to get the ticker price and its corresponding time. (Refrence to one of Dr Raahemifar's students that made this file) 
api_key: If you wish to use the AI sentiment analysis, please paste your Open Ai api key on the first line. 



Run visuals to see the interface.

or:
put the tickers you want in the stocks.csv line by line.
make sure you have your Open Ai API key paced in the api_key.txt
run main.py
you the output would be in results.csv

So you can connect your application to eather change the stocks.csv and tickers.
Also you can connect your appliaction to retreve from results.py
