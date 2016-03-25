# coding: utf-8

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Article(models.Model):
    ADMIN = 'A'
    GENERAL = 'G'
    CATEGORIES = (
        (ADMIN, _('Administrator Functions')),
        (GENERAL, _('General Usage')),
    )

    name = models.CharField(_('name'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)
    description = models.TextField(_('description'))
    category = models.CharField(_('category'), max_length=2, choices=CATEGORIES)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='article_creation_user')
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='article_update_user')

    class Meta:
        db_table = 'help_articles'
        verbose_name = _('article')
        verbose_name_plural = _('articles')

    def __unicode__(self):
        return self.name
