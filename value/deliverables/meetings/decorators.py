# coding: utf-8

from functools import wraps

from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib import messages

from value.deliverables.meetings.models import Meeting


def permission_denied(request):
    if request.is_ajax():
        return HttpResponseForbidden()
    else:
        messages.error(request, 'Permission denied.')
        return redirect('signin')

def user_is_meeting_stakeholder(function):
    def wrap(request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(pk=kwargs['meeting_id'])
            if request.user in meeting.deliverable.get_stakeholders() \
                    and meeting.meetingstakeholder_set.filter(stakeholder=request.user).exists():
                return function(request, *args, **kwargs)
            else:
                return permission_denied(request)
        except Meeting.DoesNotExist:
            return permission_denied(request)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def meeting_is_analysing_or_closed(function):
    def wrap(request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(pk=kwargs['meeting_id'])
            if meeting.is_analysing() or meeting.is_closed():
                return function(request, *args, **kwargs)
            else:
                return redirect('deliverables:meetings:dashboard', meeting.deliverable.pk, meeting.pk)
        except Meeting.DoesNotExist:
            return permission_denied(request)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap