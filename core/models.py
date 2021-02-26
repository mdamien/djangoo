from django.db import models
from bs4 import BeautifulSoup

class Webpage(models.Model):
    url = models.URLField(unique=True)
    html = models.TextField()
    pagerank = models.FloatField(default=0)

    def title(self):
        soup = BeautifulSoup(self.html, 'lxml')
        return soup.title.text


class WebpageTokenCount(models.Model):
    webpage = models.ForeignKey(Webpage, on_delete=models.DO_NOTHING)
    token = models.TextField()
    count = models.IntegerField()
