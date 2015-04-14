from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.forms.models import inlineformset_factory
from value.ratings.models import Rating, RatingValue
from value.ratings.forms import RatingForm
from django.contrib import messages

@login_required
@user_passes_test(lambda user: user.is_superuser)
def ratings(request):
    ratings = Rating.objects.all()
    return render(request, 'ratings/ratings.html', { 'ratings' : ratings })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def add(request):
    RatingValueFormSet = inlineformset_factory(Rating, RatingValue, fields=('description', 'weight',), extra=1)
    if request.method == 'POST':
        form = RatingForm(request.POST)
        formset = RatingValueFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            form.instance.created_by = request.user
            rating = form.save()
            formset = RatingValueFormSet(request.POST, instance=rating)
            if formset.is_valid():
                formset.save()
                messages.success(request, u'The rating {0} was added successfully.'.format(rating.name))
                return redirect(reverse('ratings:ratings'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        rating = Rating()
        form = RatingForm(instance=rating)
        formset = RatingValueFormSet(instance=rating)
    return render(request, 'ratings/rating.html', { 'form' : form, 'formset' : formset })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def rating(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    RatingValueFormSet = inlineformset_factory(Rating, RatingValue, fields=('description', 'weight',), extra=1)
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        formset = RatingValueFormSet(request.POST, instance=rating)
        if form.is_valid() and formset.is_valid():
            form.instance.updated_by = request.user
            form.save()
            formset.save()
            messages.success(request, u'The rating {0} was changed successfully.'.format(rating.name))
            return redirect(reverse('ratings:ratings'))
        else:
            messages.error(request, u'Please correct the error below.')
    else:
        form = RatingForm(instance=rating)
        formset = RatingValueFormSet(instance=rating)
    return render(request, 'ratings/rating.html', { 'form' : form, 'formset' : formset })

@login_required
@user_passes_test(lambda user: user.is_superuser)
def delete(request, rating_id):
    rating = get_object_or_404(Rating, pk=rating_id)
    if request.method == 'POST':
        rating.delete()
        messages.success(request, u'The rating {0} was deleted successfully.'.format(rating.name))
        return redirect(reverse('ratings:ratings'))
    return render(request, 'ratings/delete.html', { 'rating' : rating })
    