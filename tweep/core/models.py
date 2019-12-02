from django.db import models

# Create your models here.


class Tweet(models.Model):
    username = models.CharField(max_length=150)
    created_at = models.DateTimeField()
    tweet = models.TextField()
    retweet_count = models.PositiveIntegerField()
    location = models.CharField(max_length=150, null=True)
    location = models.CharField(max_length=150, null=True)

    class Meta:
        verbose_name = "Tweet"
        verbose_name_plural = "Tweets"

    def __str__(self):
        return f'{self.tweet}'
