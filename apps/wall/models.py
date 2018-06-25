from __future__ import unicode_literals
from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100,default='some@gmail.com')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.first_name+' '+self.last_name

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="messages")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.message

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    message = models.ForeignKey(Message,on_delete=models.CASCADE,related_name='messages')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.comment

