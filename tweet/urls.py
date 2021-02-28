from django.urls import path

from . import views

from .views import TweetListView, FilteredTweetListView


urlpatterns = [
    path('', TweetListView.as_view(), name='index'),
    path('tweets', TweetListView.as_view(), name='index'),
    path('tweets/<str:hashtag>', FilteredTweetListView.as_view(), name='tweets-filtered'),
]