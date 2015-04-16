import urllib, hashlib
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from value.factors.models import Factor

class Profile(models.Model):
    user = models.OneToOneField(User)
    factors = models.ManyToManyField(Factor)

    def get_display_name(self):
        if self.user.first_name and self.user.last_name:
            return self.user.get_full_name()
        elif self.user.first_name:
            return self.user.first_name
        elif self.user.last_name:
            return self.user.last_name
        else:
            return self.user.username

    def get_picture_64(self):
        return self.get_picture(64)

    def get_picture(self, size=128):
        
        initials = u''

        if self.user.first_name and self.user.last_name:
            initials = u'{0}{1}'.format(
                self.user.first_name[:1],
                self.user.last_name[:1]
                )
        elif self.user.first_name and len(self.user.first_name) > 1:
            initials = self.user.first_name[:2]
        elif self.user.last_name and len(self.user.last_name) > 1:
            initials = self.user.last_name[:2]
        elif len(self.user.username) > 1:
            initials = self.user.username[:2]
        else:
            initials = self.user.username

        default = u'http://www.initials-avatar.com/{0}?{1}'.format(
            initials,
            urllib.urlencode({ 'bg' : 'Salmon', 'fg' : 'White', 's' : size }))

        try:
            gravatar_url = u'http://www.gravatar.com/avatar/{0}?{1}'.format(
                hashlib.md5(self.user.email.lower()).hexdigest(),
                urllib.urlencode({ 'd' : default, 's' : size }))
            #return gravatar_url
            return default
        except Exception, e:
            return default

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
