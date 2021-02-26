from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def results(request):
    results = Webpage.objects.all().order_by('-pagerank').limit(10)
    return render(request, 'results.html', {
        'query': request.GET['q'],
    })