from urllib.parse import urljoin
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import collections
import tqdm
from core.models import Webpage, WebpageTokenCount

class Command(BaseCommand):
    def handle(self, *args, **options):
        webpages = Webpage.objects.all()
        WebpageTokenCount.objects.all().delete()
        tokens = []
        for webpage in tqdm.tqdm(webpages):
            soup = BeautifulSoup(webpage.html, 'lxml')
            for token, count in collections.Counter(soup.text.lower().split()).items():
                tokens.append(WebpageTokenCount(
                    webpage=webpage,
                    token=token,
                    count=count
                ))
        WebpageTokenCount.objects.bulk_create(tokens)