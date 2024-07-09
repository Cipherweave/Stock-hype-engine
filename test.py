from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer, BertForSequenceClassification, BertTokenizer
import torch

# classifier = pipeline('sentiment-analysis')

# res = classifier('I am not sure')

# print(res)


# sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

# news_title = "I am not sure"
# result = sentiment_pipeline(news_title)[0]
# print(result)

# score = result['score'] if result['label'] == 'POSITIVE' else -result['score']
# print(f"Sentiment score: {score}")


# classifier = pipeline("text-generation", model='distilgpt2')

# res = classifier(
#     "I am not sure what to do next. I am feeling very",
#     max_length=50,
#     num_return_sequences=2,
#     )

# print(res)


# classifier = pipeline('zero-shot-classification')

# res = classifier(
#     "I am not sure what to do next. I am feeling very good",
#     candidate_labels=['positive', 'negative', 'neutral'],
#     )

# print(res)




# model_name = "distilbert-base-uncased-finetuned-sst-2-english"
# model = AutoModelForSequenceClassification.from_pretrained(model_name) 
# tokenizer = AutoTokenizer.from_pretrained(model_name)

# classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

# res = classifier('I know')

# print(res)



# classifier = pipeline("text-generation", model='meta-llama/Meta-Llama-3-8B')


"""-----------------Finbert-----------------"""

# finbert = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)
# tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

# nlp = pipeline("sentiment-analysis", model=finbert, tokenizer=tokenizer)

# sentences = ["there is a shortage of capital, and we need extra financing",  
#              "growth is strong and we have plenty of liquidity", 
#              "there are doubts about our finances", 
#              "profits are flat", 
#              'AI Is Great for Apple, But Satellites Matter More. SpaceX and These 2 Stocks Benefit.']
# results = nlp(sentences)
# print(results)


'''---------------------LLAMA---------------------'''

model_path = "C:\\ali\\VS Coding\\AIs\\OrengutengLlama-3-8B-Lexi-Uncensored"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

def analyze_stock_news(ticker, news):
    inputs = tokenizer(f"{ticker}: {news}", return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=-1)
    scores = probs.detach().numpy()[0]

    sentiment_score = scores[2] - scores[0]  # Adjust based on your model's output order
    sentiment_score = (2 * (sentiment_score - 0.5))  # Normalize to -1 to 1

    return sentiment_score

ticker = "AAPL"
news_title = "Apple's new product launch boosts market confidence"
score = analyze_stock_news(ticker, news_title)
print(f"Sentiment score for {ticker}: {score}")