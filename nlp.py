from pymongo import MongoClient
import pandas as pd
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

# nltk.download()

client = MongoClient("mongodb+srv://admin:admin@cluster0.zljbf.mongodb.net/test?retryWrites=true&w=majority")

db = client["test"]

collection = db["test"]

results = collection.find({}, {"text": 1})

df = pd.DataFrame(collection.find({}, {"text": 1}))

sample = df["text"].sample(n=10, random_state=1)

paragraph = ""
for review in sample:
    paragraph += review

# print(paragraph)

# Tokenize sentences
sentences = nltk.sent_tokenize(paragraph)
# print(sentences)

# Tokenize words
# words = nltk.word_tokenize(paragraph)
# print(words)

stemmer = PorterStemmer()

# Stemming
for i in range(len(sentences)):
    words = nltk.word_tokenize(sentences[i])
    words = [stemmer.stem(word) for word in words]
    sentences[i] = " ".join(words)
    
print(sentences)

lemmatizer = WordNetLemmatizer()

# Lemmatization
for i in range(len(sentences)):
    words = nltk.word_tokenize(sentences[i])
    words = [lemmatizer.lemmatize(word) for word in words]
    sentences[i] = ' '.join(words)

print(sentences)

# Removing stopwords
for i in range(len(sentences)):
    words = nltk.word_tokenize(sentences[i])
    words = [word for word in words if word not in stopwords.words('english')]
    sentences[i] = ' '.join(words)

print(sentences)

# POS Tagging
words = nltk.word_tokenize(paragraph)

tagged_words = nltk.pos_tag(words)

# Tagged word paragraph
word_tags = []
for tw in tagged_words:
    word_tags.append(tw[0]+"_"+tw[1])

tagged_paragraph = ' '.join(word_tags)
print(tagged_paragraph)
