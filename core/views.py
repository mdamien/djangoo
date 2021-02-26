from django.shortcuts import render
from bs4 import BeautifulSoup
from core.models import Webpage, WebpageTokenCount

import tqdm

def index(request):
    return render(request, 'index.html')


def results(request):
    token = request.GET['q'].lower()
    webpages = WebpageTokenCount.objects.filter(token=token).order_by("-count")
    return render(request, 'results.html', {
        'results': webpages[:20],
        'query': request.GET['q'],
    })