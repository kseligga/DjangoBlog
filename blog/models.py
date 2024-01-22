from django.contrib.auth.models import User

# Create your models here.
from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=126)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=31)
    pub_date = models.DateTimeField()


class Thread(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')
    author = models.CharField(max_length=31)

    def __str__(self):
        return self.title


class Response(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.CharField(max_length=31)
    pub_date = models.DateTimeField()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200, null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.user.username
