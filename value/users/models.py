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

    def get_picture_32(self):
        return self.get_picture(32)

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

        return '/static/img/' + initials.upper() + '.png'

        colors = {
          'a' : 'AA3C39',
          'b' : '993350',
          'c' : '8A2E60',
          'd' : '6F256F',
          'e' : '592A71',
          'f' : '4B2D73',
          'g' : '403075',
          'h' : '343477',
          'i' : '2E4372',
          'j' : '29516D',
          'k' : '236467',
          'l' : '277553',
          'm' : '2D882D',
          'n' : '609732',
          'o' : '7B9F35',
          'p' : '91A437',
          'q' : 'AAA839',
          'r' : 'AA9F39',
          's' : 'AA9739',
          't' : 'AA8E39',
          'u' : 'AA8539',
          'v' : 'AA7939',
          'w' : 'AA6D39',
          'x' : 'AA5A39',
          'y' : 'AA5439',
          'z' : '7F2A68'
        }

        default = u'http://www.initials-avatar.com/{0}?{1}'.format(
            initials,
            urllib.urlencode({ 'bg' : colors[initials[:1].lower()], 'fg' : 'FFFFFF', 's' : size }))

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
