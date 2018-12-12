from .models import MeetingStakeholder


def meeting_stakeholder(request):
    context = {'is_meeting_stakeholder': False}
    if hasattr(request, 'resolver_match'):
        if request.resolver_match is not None:
            meeting_id = request.resolver_match.kwargs.get('meeting_id')
            if MeetingStakeholder.objects.filter(meeting_id=meeting_id, stakeholder_id=request.user.pk).exists():
                context['is_meeting_stakeholder'] = True
    return context
