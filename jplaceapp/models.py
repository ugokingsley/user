from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import secretballot
from registration.signals import user_registered

# from ckeditor_uploader.fields import RichTextUploadingField
'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

'''


class ExUserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    picture = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
    bio =  models.TextField(unique=True, default=None)

    def __unicode__(self):
        return self.user


def user_registered_callback(sender, user, request, **kwargs):
    profile = ExUserProfile(user=user)
    profile.picture = request.POST["picture"]
    profile.bio = request.POST["bio"]
    profile.save()

user_registered.connect(user_registered_callback)



class MyTestimony(models.Model):
    testimony = models.TextField(unique=True)

    def __unicode__(self):
        return '%s' % self.testimony

    def __str__(self):
        return self.testimony


class Testimonies(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(null=True, blank=True)
    user = models.ForeignKey(User)
    testimonies = models.ForeignKey(MyTestimony)
    likes = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return '%s, %s' % (self.user.username, self.testimonies.testimony)

    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.testimonies.testimony)


secretballot.enable_voting_on(Testimonies)

'''
class UserFollowers(models.Model):
    user = models.ForeignKey(User, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    followers = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return '%s, %s' % (self.user, self.count)

    def __unicode__(self):
        return '%s, %s' % (self.user, self.count)
'''


class VoteTestimonies(models.Model):
    testimony = models.ForeignKey(Testimonies, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=1)
    users_voted = models.ManyToManyField(User)

    def __str__(self):
        return '%s, %s' % (self.testimony, self.votes)

    def __unicode__(self):
        return '%s, %s' % (self.testimony, self.votes)


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    testimony = models.ManyToManyField(Testimonies)

    def __unicode__(self):
        return '%s' % (self.name)

    def __str__(self):
        return self.name
