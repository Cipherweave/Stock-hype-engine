import requests

def get_html_content(url):
    response = requests.get(url)
    return response.text

# Example usage
url = 'https://elite.finviz.com/quote.ashx?t=AAPL&p=d'  # Example Finviz link
html_content = get_html_content(url)
print(html_content)