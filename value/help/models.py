from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    ADMIN = u'A'
    GENERAL = u'G'
    CATEGORIES = (
        (ADMIN, u'Administrator Functions'),
        (GENERAL, u'General Usage'),
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=2, choices=CATEGORIES)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='article_creation_user')
    update_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='article_update_user')

    def __unicode__(self):
        return self.name
