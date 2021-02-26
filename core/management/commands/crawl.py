from urllib.parse import urljoin
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from core.models import Webpage

SEED = "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal"
DOMAIN = "https://fr.wikipedia.org"

class Command(BaseCommand):
    def handle(self, *args, **options):
        urls_crawled = set()
        urls = set()
        for webpage in Webpage.objects.all():
            urls_crawled.add(webpage.url)
            soup = BeautifulSoup(webpage.html, 'lxml')
            for link in soup.select('a'):
                try:
                    url = urljoin(webpage.url, link['href'])
                    url = url.split('#')[0]
                    urls.add(url)
                except KeyError:
                    pass
        print(len(urls), 'found')
        print(len(urls_crawled), 'already crawled')
        urls = urls - urls_crawled
        print(len(urls), 'to crawl')

        urls = [url for url in urls if url.startswith(DOMAIN)]
        print(len(urls), 'to crawl on this domain')
        if not urls:
            urls = {SEED}
        for url in urls:
            print('GET', url)
            resp = requests.get(url)
            Webpage(url=url, html=resp.text).save()