from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import numpy as np
from scipy import sparse
from fast_pagerank import pagerank
import tqdm
from core.models import Webpage

class Command(BaseCommand):
    def handle(self, *args, **options):
        webpages = Webpage.objects.all()
        nodes = [webpage.url for webpage in webpages]
        links = []
        for webpage in tqdm.tqdm(webpages):
            soup = BeautifulSoup(webpage.html, 'lxml')
            for link in soup.select('a'):
                try:
                    url = urljoin(webpage.url, link['href'])
                    url = url.split('#')[0]
                    if url in nodes:
                        links.append([nodes.index(webpage.url), nodes.index(url)])
                except KeyError:
                    pass
        A = np.array(links)
        weights = [1]*len(links)
        G = sparse.csr_matrix((weights, (A[:,0], A[:,1])), shape=(len(nodes), len(nodes)))
        pr=pagerank(G, p=0.85)
        print('saving')
        for i, webpage in enumerate(webpages):
            webpage.pagerank = pr[i]
        Webpage.objects.bulk_update(webpages, ['pagerank'])

        for webpage in Webpage.objects.all().order_by('-pagerank')[:20]:
            print(webpage.url, webpage.pagerank)