from django.db import models
from django.contrib.auth.models import User
from value.ratings.models import Rating

class Factor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)
    rating = models.ForeignKey(Rating)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='factor_creation_user')
    update_date = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, null=True, related_name='factor_update_user')

    def __unicode__(self):
        return self.name
