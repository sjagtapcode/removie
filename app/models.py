from django.db import models
from django.contrib.postgres.fields import ArrayField


class Movies(models.Model):
    mid = models.IntegerField(primary_key=True)
    vote_count = models.IntegerField(default=0)
    vote_average = models.FloatField(default=0)
    release_date = models.DateField(null=True)
    language = models.CharField(max_length=10,null=True)
    title = models.CharField(max_length=100)
    adult = models.BooleanField(default=False)
    popularity = models.FloatField(null=True)
    poster_path = models.CharField(max_length=100,null=True)
    genre_ids = ArrayField(models.IntegerField(null=True,blank=True),null=True,blank=True)
    overview = models.CharField(max_length=10000,null=True)

    def __str__(self):
        return self.title


class Lists(models.Model):
    lid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,null=True)
    mylist = ArrayField(
        models.IntegerField(null=True,blank=True),
        default=[0],
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.lid)
