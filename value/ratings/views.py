from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from value.ratings.models import Rating, RatingValue
from value.ratings.forms import RatingForm

@login_required
def ratings(request):
    ratings = Rating.objects.all()
    return render(request, 'ratings/ratings.html', { 'ratings' : ratings })

@login_required
def add_rating(request):
    RatingValueFormSet = inlineformset_factory(Rating, RatingValue, fields=('description', 'weight',))
    if request.method == 'POST':
        form = RatingForm(request.POST)
        formset = RatingValueFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            rating = form.save()
            formset = RatingValueFormSet(request.POST, instance=rating)
            if formset.is_valid():
                formset.save()
                return redirect(reverse('ratings'))
    else:
        rating = Rating()
        form = RatingForm(instance=rating)
        formset = RatingValueFormSet(instance=rating)
    return render(request, 'ratings/add_rating.html', { 'form' : form, 'formset' : formset })