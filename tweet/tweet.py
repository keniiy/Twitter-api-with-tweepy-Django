import tweepy
import os
from collections import defaultdict
from .config import *
from .models import Tweet

class TweetService:

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumerKey
        self.consumer_secret = consumerSecret
        self.access_token = accessToken
        self.access_token_secret = accessTokenSecret

    def get_tweets_from_api(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        user = api.get_user("python_tip")
        alltweets = []

        tweets_with_replies = api.user_timeline(screen_name = 'python_tip', count = 3000, include_rts = True)
        tweet_replies = list(filter(lambda x: x.in_reply_to_user_id, tweets_with_replies))
        tweets = list(filter(lambda x: not x.in_reply_to_user_id, tweets_with_replies))
        return tweets


    def get_hashtag_freqs(self, tweets):

        hashtag_freqs = defaultdict(int)

        for tweet in tweets:
            tweet.byUser = tweet.entities['user_mentions'][0]['screen_name'] if tweet.entities['user_mentions'] and tweet.entities['user_mentions'][0]['screen_name'] else ""
    
            for hashtag in tweet.entities['hashtags']:
                hashtag_freqs[hashtag['text'].lower()] += 1
        return hashtag_freqs

def save_to_db():
    original_tweets = get_tweets_from_api()
    for original_tweet in original_tweets:
        if not original_tweet.retweeted:
            if not Tweet.objects.filter(tweet_id=original_tweet.id):
                new_tweet = Tweet(tweet_id = original_tweet.id, tweet_text = original_tweet.text, published_date = original_tweet.created_at, is_active = True)
                Tweet.save()    