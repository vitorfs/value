import urllib, hashlib
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from value.factors.models import Factor

class Profile(models.Model):
    user = models.OneToOneField(User)
    factors = models.ManyToManyField(Factor)

    def get_picture(self):
        default = ''
        size = '128'
        try:
            gravatar_url = u'http://www.gravatar.com/avatar/{0}?{1}'.format(
                hashlib.md5(self.user.email.lower()).hexdigest(),
                urllib.urlencode({ 'd' : default, 's' : size, }))
            return gravatar_url
        except Exception, e:
            return default

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
