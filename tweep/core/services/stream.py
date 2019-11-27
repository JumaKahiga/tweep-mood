import json
import tweepy

from dateutil.parser import parse
from django.conf import settings
from django.db import connection

from .kafka_producer import (
    publish_message, connect_kafka_producer)


# Twitter Keys
API_KEY = settings.API_KEY
API_SECRET_KEY = settings.API_SECRET_KEY
ACCESS_TOKEN = settings.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = settings.ACCESS_TOKEN_SECRET


class TweetObject:
    def __init__(self, username, tweet, created_at, retweet_count, location):
        self.username = username
        self.tweet = tweet
        self.created_at = created_at
        self.retweet_count = retweet_count
        self.location = location

    def toDict(self):
        tweet_dict = dict(
            username=self.username,
            tweet=self.tweet,
            created_at=self.created_at,
            retweet_count=self.retweet_count,
            location=self.location)

        return tweet_dict

    @staticmethod
    def append_tweets(tweets, tweet_dict):
        tweets.append(tweet_dict)
        return tweets


class TweetListener(tweepy.StreamListener):
    def on_connect(self):
        pass

    def on_error(self):
        pass

    def on_data(self, data):
        try:
            raw_data = json.loads(data)

            if 'text' in raw_data:
                username = raw_data['user']['screen_name']
                tweet = raw_data['text']
                created_at = parse(raw_data['created_at'])
                retweet_count = raw_data['retweet_count']
                location = raw_data['user']['location']

                # tweet_dict = TweetObject(
                #     username, tweet, created_at, retweet_count, location).toDict()

                with connection.cursor() as cursor:
                    cursor.execute(""" INSERT INTO
                        core_tweet (
                        username, created_at, tweet, retweet_count, location)
                        VALUES(%s, %s, %s, %s, %s)""", [username, created_at, tweet, retweet_count, location]) # noqa

        except Exception as e:
            return e


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    listener = TweetListener(api=api)
    stream = tweepy.Stream(auth, listener=listener)
    print('starting............')

    kafka_producer_ = connect_kafka_producer()
    man = [{'a': 1}, {'b': 2}]

    for i in man:
        print(i.values())
        publish_message(kafka_producer_, 'raw_tweets', 'raw', 'a sample')

    if kafka_producer_ is not None:
        kafka_producer_.close()

    filter_words = ['kenya', 'nairobi']

    stream.filter(track=filter_words, languages = ['en'])


