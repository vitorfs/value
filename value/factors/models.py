from django.db import models
from django.contrib.auth.models import User
from value.measures.models import Measure

class Factor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)
    measure = models.ForeignKey(Measure, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='factor_creation_user')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='factor_update_user')

    def __unicode__(self):
        return self.name
