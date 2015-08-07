# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from cart.models import CartItem
from log.models import *
from datetime import *
from django.utils.translation import ugettext as _
from notification_email import sendEmail

class Rate(models.Model):
    user = models.ForeignKey(User)
    mark = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(User, related_name='who_post')
    text = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0,blank=True,null=True)
    file = models.FileField(upload_to='files/',blank=True,null=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return self.text

class Chat(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user')
    to_user = models.ForeignKey(User, related_name='to_user')
    create_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(Comment)
    is_from_user_read = models.BooleanField(default=True)
    is_to_user_read = models.BooleanField(default=True)


    def add_message(self,from_user,text,file=None):
        comment = Comment.objects.create(user=from_user,text=text,file=file)
        self.comments.add(comment)
        self.save()

