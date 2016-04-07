# coding: utf-8

from django.shortcuts import redirect
from django.http import HttpResponseForbidden, Http404
from django.contrib import messages
from django.utils.translation import ugettext as _

from value.deliverables.meetings.models import Meeting


def permission_denied(request):
    if request.is_ajax():
        return HttpResponseForbidden()
    else:
        messages.error(request, _('Permission denied.'))
        return redirect('signin')


def user_is_meeting_stakeholder(function):
    def wrap(request, *args, **kwargs):
        try:
            meeting = Meeting.objects.get(pk=kwargs['meeting_id'])
            if request.user in meeting.deliverable.get_all_stakeholders() \
                    and meeting.meetingstakeholder_set.filter(stakeholder=request.user).exists():
                return function(request, *args, **kwargs)
            else:
                return permission_denied(request)
        except Meeting.DoesNotExist:
            raise Http404
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
            raise Http404
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
