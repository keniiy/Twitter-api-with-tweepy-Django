from django.db import models


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    tweet = models.TextField()
    user_name = models.CharField(max_length=240)
    user_email = models.CharField(max_length=240)
    tweet_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    favorite_count = models.IntegerField()
    retweet_count = models.IntegerField()

    def __repr__(self):
            return "<Text: {}>".format(self.text)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
