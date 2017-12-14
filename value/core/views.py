# coding: utf-8

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect, render

from value.deliverables.meetings.models import Meeting, MeetingStakeholder
from value.deliverables.meetings.views.evaluate import evaluate
from value.core.forms import SurveyUserForm


@login_required
def home(request):
    return redirect('deliverables:index')


def survey(request, uuid):
    try:
        meeting = Meeting.objects.get(survey_id=uuid, is_survey=True)
    except Meeting.DoesNotExist:
        raise Http404

    if request.user.is_authenticated():
        return evaluate(request, meeting.deliverable_id, meeting.id, 'core/survey.html')
    else:
        form = SurveyUserForm(request.POST or None)
        if request.method == 'POST':
            user = None

            email = request.POST.get('email', '').strip()

            if email:
                try:
                    user = User.objects.get(email__iexact=email)
                except (User.MultipleObjectsReturned, User.DoesNotExist):
                    user = None

            authenticate_external_user = False

            if user is not None:
                if user.profile.is_external:
                    authenticate_external_user = True
                else:
                    signin_url = reverse('signin')
                    next_url = reverse('deliverables:meetings:evaluate', kwargs={
                        'deliverable_id': meeting.deliverable_id,
                        'meeting_id': meeting.id
                    })
                    url = '{}?next={}'.format(signin_url, next_url)
                    messages.info(request, 'The user "%s" already exists in our database. Please enter your username and password to proceed.' % user.email)
                    return redirect(url)
            else:
                if form.is_valid():
                    user = form.save()
                    authenticate_external_user = True

            if authenticate_external_user:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                ms, created = MeetingStakeholder.objects.get_or_create(meeting=meeting, stakeholder=user, defaults={
                    'is_external': True
                })
                if created:
                    meeting.calculate_all_rankings()
                return redirect('survey', uuid=uuid)

        return render(request, 'core/survey_login.html', {'form': form, 'meeting': meeting})


def thanks(request):
    return render(request, 'core/thanks.html')
