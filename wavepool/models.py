from django.db import models
import datetime


class NewsPost(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField(max_length=3000)
    source = models.URLField()
    is_cover_story = models.BooleanField(default=False)
    publish_date = models.DateField(default=datetime.date.today())

    @property
    def teaser(self):
        return self.body[:150]


class UserStory(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.title


class AcceptanceCriteria(models.Model):
    UserStory = models.ForeignKey(UserStory, on_delete=models.CASCADE)
    ac = models.TextField(max_length=3000)
