from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
import tweepy
from collections import defaultdict
import threading
import os
from .config import *
from .tweet import TweetService
from django.conf import settings
from .models import Tweet


tweet_service = TweetService(consumerKey, consumerSecret, accessToken, accessTokenSecret)

alltweets = tweets = tweet_service.get_tweets_from_api() 



class TweetListView(ListView):
    # model = Tweet
    template_name = 'pages/index.html' 
    context_object_name = 'tweets'
    ordering = ['-date_posted', '-retweet_count', '-favorite_count']
    paginate_by = 9

    def get_context_data(self, **kwargs):
        hashtag_freqs = tweet_service.get_hashtag_freqs(tweets)
        context = super(TweetListView, self).get_context_data(**kwargs)
        # context['tweets'] = tweets,
        context['hashtag_freqs'] = hashtag_freqs,
        context['hashtag_freq_keys'] = tuple(hashtag_freqs.keys()),
        context['hashtag_freq_values'] = tuple(hashtag_freqs.values()),
        return context

    def get_queryset(self):
        query = self.request.GET.get('q', '').lstrip().rstrip().lower()
        res = list(filter( lambda x: query in list(map(lambda y: y['text'].lower(), x.entities['hashtags'])) or query in x.text.lower(), tweets))
        res = sorted(res, key=lambda x: x.retweet_count , reverse=True)
        res = sorted(res, key=lambda x: x.favorite_count , reverse=True)
        # pdb.set_trace()
        return res #{'tweets' :res, 'hashtag_freqs': hashtag_freqs}

class FilteredTweetListView(ListView):
    # model = Tweet
    template_name = 'pages/index.html'  
    context_object_name = 'tweets'
    ordering = ['-date_posted']
    paginate_by = 9


    def get_context_data(self, **kwargs):
        hashtag_freqs = tweet_service.get_hashtag_freqs(tweets)
        context = super(FilteredTweetListView, self).get_context_data(**kwargs)
        context['hashtag_freqs'] = hashtag_freqs,
        context['hashtag_freq_keys'] = tuple(hashtag_freqs.keys()),
        context['hashtag_freq_values'] = tuple(hashtag_freqs.values()),
        return context

    def get_queryset(self):
        hashtag = self.kwargs.get('hashtag').lstrip().rstrip().lower()
        query = self.request.GET.get('q', '').lstrip().rstrip().lower()
        filtered_tweets_by_hashtag = list(filter( lambda x: hashtag in list(map(lambda y: y['text'].lower(), x.entities['hashtags'])) or hashtag in x.text.lower() ,tweets))
        filtered_tweets_by_query = list(filter( lambda x: query in list(map(lambda y: y['text'].lower(), x.entities['hashtags'])) or query in x.text.lower() , filtered_tweets_by_hashtag))
        tweets_sorted_by_retweet_count = sorted(filtered_tweets_by_query, key=lambda x: x.retweet_count , reverse=True)
        res = tweets_sorted_by_favorite_count = sorted(tweets_sorted_by_retweet_count, key=lambda x: x.favorite_count , reverse=True)
        return res

