from django.contrib.auth.models import User
from django.db import models


# from ckeditor_uploader.fields import RichTextUploadingField



class MyTestimony(models.Model):
    testimony = models.TextField(unique=True)

    def __unicode__(self):
        return '%s' % self.testimony

    def __str__(self):
        return self.testimony


class Testimonies(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    testimonies = models.ForeignKey(MyTestimony)

    def __str__(self):
        return '%s, %s' % (self.user.username, self.testimonies.testimony)

    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.testimonies.testimony)


class UserFollowers(models.Model):
    user = models.ForeignKey(User, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=1)
    followers = models.ManyToManyField(User, related_name='followers')

    def __str__(self):
        return '%s, %s' % (self.user, self.count)

    def __unicode__(self):
        return '%s, %s' % (self.user, self.count)


class SharedTestimonies(models.Model):
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
