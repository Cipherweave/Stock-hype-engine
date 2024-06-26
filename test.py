from transformers import pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# classifier = pipeline('sentiment-analysis')

# res = classifier('I am not sure')

# print(res)





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



classifier = pipeline("text-generation", model='meta-llama/Meta-Llama-3-8B')