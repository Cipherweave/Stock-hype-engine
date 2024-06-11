# Stock-hype-engine

An engine that represent how much potential a stock have for traders to trade.
This program looks over the given stock/stocks recently news titles and give them an over all score of hype. for example if the owner compony of stock x make an huge update on one of their products and it goes on the news, the program gives a high hype score to that stock and suggests the user to start trading on that sepecific stock. The hype is a number between 0 to 1. As it gets closer to 1, it is more worth it to trade in.

INSTALLMENTS

Terminal:
pip install bs4
pip show bs4
pip install nltk
pip install finvizfinance
pip install yfinance

Code:
import nltk
nltk.download('vader_lexicon')

cmd Run as administrator:
python -m venv myenv
myenv\Scripts\activate
pip install finvizfinance
