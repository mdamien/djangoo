from django.db import models

class Webpage(models.Model):
    url = models.URLField(unique=True)
    html = models.TextField()
    pagerank = models.FloatField()