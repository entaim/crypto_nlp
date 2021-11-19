
import string

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import spacy
import praw


%matplotlib inline

reddit = praw.Reddit(client_id='qQBQxY9R1zGrYJH9pACBOw', client_secret='MjrjCout_Omkh_3feZFq3UrzyLBicw', user_agent='Crypto')

crypto = []
ml_subreddit = reddit.subreddit('Cryptocurrency')
for post in ml_subreddit.hot(limit=30000):
    crypto.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
crypto = pd.DataFrame(crypto,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])
# print(posts)
crypto

crypto.dropna(subset=['body'], inplace=True)
crypto['original_body'] = crypto['body']
crypto

import spacy
nlp = spacy.blank('en')


import re

def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))

def remove_stop_words(text):
    doc = nlp(text)
    nlp.Defaults.stop_words -= {"nt","crypto", "cryptocurrency"}
    return " ".join([token.text for token in doc if not token.is_stop])

def lemmatize_words(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])

remove_spaces = lambda x : re.sub('\\s+', ' ', x)

# Reference : https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

remove_double_quotes = lambda x : x.replace('"', '')
remove_single_quotes = lambda x : x.replace('\'', '')
trim = lambda x : x.strip()

other_chars = ['*', '#', '&x200B', '[', ']', '; ',' ;' "&nbsp", "“","“","”", "x200b"]


def remove_other_chars(x: str):
    for char in other_chars:
        x = x.replace(char, '')
    
    return x


def lower_case_text(text):
    return text.lower()

funcs = [
    remove_urls, 
    remove_punctuation,
    remove_stop_words, 
    remove_emoji, 
    remove_double_quotes, 
    remove_single_quotes,
    lower_case_text,
    remove_other_chars,
    lemmatize_words,
    remove_spaces,
    trim]


for fun in funcs:
    crypto['body'] = crypto['body'].apply(fun)

# # reset indexes (again)
crypto.reset_index(inplace=True)
crypto.drop(['index'], axis=1, inplace=True)


