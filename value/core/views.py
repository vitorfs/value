from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from value.deliverables.meetings.models import Meeting, MeetingStakeholder


@login_required
def home(request):
    meeting_ids = MeetingStakeholder.objects.filter(stakeholder=request.user).values('meeting_id')
    ongoing_meetings = Meeting.objects.filter(id__in=meeting_ids, status=Meeting.ONGOING)
    closed_meetings = Meeting.objects.filter(id__in=meeting_ids, status=Meeting.CLOSED)
    return render(request, 'core/home.html', { 'ongoing_meetings': ongoing_meetings, 'closed_meetings': closed_meetings })
    