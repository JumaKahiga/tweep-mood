import re

from django.db import connection

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
from wordcloud import WordCloud


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
            background_color='white',
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

    new_df['Sentiment'] = np.array(
        [instance.sentiment_analyzer(x) for x in new_df['clean_tweets']])

    instance.save_to_csv(new_df)

    positive = [t for i, t in enumerate(
        new_df['clean_tweets']) if new_df['Sentiment'][i] > 0]

    negative = [t for i, t in enumerate(
        new_df['clean_tweets']) if new_df['Sentiment'][i] < 0]

    neutral = [t for i, t in enumerate(
        new_df['clean_tweets']) if new_df['Sentiment'][i] == 0]

    positive_percent = round(
        100 * (len(positive) / len(new_df['clean_tweets'])))
    negative_percent = round(
        100 * (len(negative) / len(new_df['clean_tweets'])))
    neutral_percent = round(
        100 * (len(neutral) / len(new_df['clean_tweets'])))

    print(f'Positive Tweets: {positive_percent}% \n')
    print(f'Negative Tweets: {negative_percent}% \n')
    print(f'Neutral Tweets: {neutral_percent}% \n')

    sentiment_results = [positive_percent, negative_percent, neutral_percent]
    labels = ['positive', 'negative', 'neutral']

    plt.pie(sentiment_results, labels=labels, startangle=90, autopct='%.1f%%')
    plt.show()

    instance.word_cloud(new_df)
