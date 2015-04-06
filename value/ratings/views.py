from django.shortcuts import render

def ratings(request):
    return render(request, 'ratings/ratings.html')