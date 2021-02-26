from django.shortcuts import render
from bs4 import BeautifulSoup
from core.models import Webpage

import tqdm

def index(request):
    return render(request, 'index.html')


def results(request):
    token = request.GET['q'].lower()
    url_count = {}
    webpages = Webpage.objects.all()
    for webpage in tqdm.tqdm(webpages):
        soup = BeautifulSoup(webpage.html, 'lxml')
        text = soup.text
        count = len([1 for token2 in text.split() if token == token2.lower()])
        url_count[webpage.url] = count
    webpages = list(webpages)
    webpages.sort(key=lambda page: -url_count[page.url])
    return render(request, 'results.html', {
        'results': webpages[:20],
        'query': request.GET['q'],
    })