from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

def index(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect(reverse('search:index'))
    return render(request, 'search/index.html')