# coding: utf-8

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse as r


def home(request):
    if request.user.is_authenticated():
        return render(request, 'core/home.html')
    else:
        return redirect(r('signin'))
