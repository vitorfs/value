from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from value.ratings.models import Rating
from value.ratings.forms import RatingForm

@login_required
def ratings(request):
    ratings = Rating.objects.all()
    return render(request, 'ratings/ratings.html', { 'ratings' : ratings })

@login_required
def add_rating(request):
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.save()
            return redirect(reverse('rating', args=(rating.pk,)))
    else:
        rating = Rating()
        form = RatingForm(instance=rating)
    return render(request, 'ratings/add_rating.html', { 'form' : form })