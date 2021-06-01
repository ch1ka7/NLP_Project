# import the MongoClient class from the library
from pymongo import MongoClient

# import nltk stopwords list
from nltk.corpus import stopwords

# import Natural Language Toolkit library
import nltk

# import pandas library
import pandas as pd

# import heap queue algorithm library
import heapq

# import regular expression library
import re

# !!! We used MongoDB Atlas cloud database
# create an client instance of the MongoDB cloud database class
client = MongoClient("mongodb+srv://admin:admin@cluster0.zljbf.mongodb.net/test?retryWrites=true&w=majority")

# create an instance of "nlp_project_db'
db = client["nlp_project_db"]

# access a MongoDB collection "movie_reviews"
collection = db["movie_reviews"]

# create a dataframe with only reviews text
reviews_df = pd.DataFrame(collection.find({}, {"text": 1}))

# take a random sample from reviews dataframe, n is the sample size
sample = reviews_df["text"].sample(n=10000, random_state=1)

# make a single paragraph with review sentences from sample
paragraph = ""
for review in sample:
    paragraph += review + "\n"
# print(paragraph)

# Tokenize sentences
# break the sentences in the paragraph to a list of sentences.
dataset = nltk.sent_tokenize(paragraph)
for i in range(len(dataset)):  # remove
    dataset[i] = dataset[i].lower()
    dataset[i] = re.sub(r'\W', ' ', dataset[i])
    dataset[i] = re.sub(r'\s+', ' ', dataset[i])
# print(dataset)

# Removing stopwords and numbers
for i in range(len(dataset)):
    words = nltk.word_tokenize(dataset[i])
    words = [word for word in words if word not in stopwords.words('english') and not word.isdigit()]
    dataset[i] = ' '.join(words)
# print(dataset)

# Creating word histogram
word2count = {}
for data in dataset:
    words = nltk.word_tokenize(data)
    for word in words:
        if word not in word2count.keys():
            word2count[word] = 1
        else:
            word2count[word] += 1

# Selecting best 100 features
freq_words = heapq.nlargest(100, word2count, key=word2count.get)

# create a term frequency table; the table contains the most used words in reviews
term_frequency_table = pd.DataFrame(word2count.items(), columns=["Term", "Frequency"])

# sort the table by frequency and show top n=50 terms
sorted_table = term_frequency_table.sort_values(by="Frequency", ascending=False).head(n=50).to_string(index=False)
print(sorted_table)
