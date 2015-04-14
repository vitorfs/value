from django.db import models
from django.contrib.auth.models import User

class Instance(models.Model):
    """FINISHED = u'F'
    STATUS = (
        (NEW, u'New'),
        (READY, u'Ready'),
        (RUNNING, u'Running'),
        (FINISHED, u'Finished'),
        )"""

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)
    stakeholders = models.ManyToManyField(User)
    status = models.CharField(max_length=1)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='valuemodel_creation_user')
    update_date = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, null=True, related_name='valuemodel_update_user')

    def __unicode__(self):
        return self.name
