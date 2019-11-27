import re

from django.db import connection

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from wordcloud import WordCloud, STOPWORDS


class TweetProcessor:
    def retrieve_tweets(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT username, tweet FROM core_tweet")
            tweets = cursor.fetchall()

            df = pd.DataFrame(
                tweets, columns=['username', 'tweet'])

        return df

    def clean_tweets(self, df):
        stopwords_ = stopwords.words('english')
        wordnet = WordNetLemmatizer()
        df['clean_tweets'], df['len'] = None, None

        for i in range(0, len(df['tweet'])):
            exclude_list = ['[^a-zA-Z]','rt', 'http', 'co', 'RT']
            exclusions = '|'.join(exclude_list)
            text_ = re.sub(exclusions, ' ', df['tweet'][i])
            text_ = text_.lower()
            words = text_.split()
            words = [wordnet.lemmatize(
                word) for word in words if word not in stopwords_]

            df['clean_tweets'][i] = ' '.join(words)

            df['len'][i] = np.array(
                [len(tweet) for tweet in df["clean_tweets"] if tweet])

        return df

    def word_cloud(self, df):
        plt.subplots(figsize=(12, 10))
        wordcloud_ = WordCloud(
            background_color='blue',
            width=1000,
            height=800).generate(' '.join(df['clean_tweets']))

        plt.imshow(wordcloud_)
        plt.axis('off')
        plt.show()

    def save_to_csv(self, df):
        try:
            df.to_csv('clean_tweets.csv')
            print('CSV save successful. \n')
        except Exception as e:
            print(e)

    def sentiment_analyzer(self, tweet):
        analyzer = TextBlob(tweet)

        if analyzer.sentiment.polarity > 0:
            return 1
        elif analyzer.sentiment.polarity == 0:
            return 0
        else:
            return -1


if __name__ == '__main__':
    instance = TweetProcessor()
    df = instance.retrieve_tweets()
    new_df = instance.clean_tweets(df)

    instance.word_cloud(new_df)

    new_df['Sentiment'] = np.array(
        [instance.sentiment(x) for x in new_df['clean_tweets']]

    instance.word_cloud(new_df)
    instance.save_to_csv(new_df)

