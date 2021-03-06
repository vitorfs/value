# coding: utf-8

from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils.translation import ugettext as _

from value.deliverables.models import Deliverable


def permission_denied(request):
    if request.is_ajax():
        return HttpResponseForbidden()
    else:
        messages.error(request, _('Permission denied.'))
        return redirect('signin')


def user_is_manager(function):
    def wrap(request, *args, **kwargs):
        try:
            deliverable = Deliverable.objects.get(pk=kwargs['deliverable_id'])
            if deliverable.manager == request.user or deliverable.admins.filter(pk=request.user.pk).exists():
                return function(request, *args, **kwargs)
            else:
                return permission_denied(request)
        except Deliverable.DoesNotExist:
            return permission_denied(request)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_stakeholder(function):
    def wrap(request, *args, **kwargs):
        try:
            deliverable = Deliverable.objects.get(pk=kwargs['deliverable_id'])
            if request.user == deliverable.manager or request.user in deliverable.stakeholders.all():
                return function(request, *args, **kwargs)
            else:
                return permission_denied(request)
        except Deliverable.DoesNotExist:
            return permission_denied(request)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
