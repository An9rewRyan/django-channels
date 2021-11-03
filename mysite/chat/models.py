from typing import DefaultDict
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import AutoField, DateField
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
import datetime 
from datetime import timedelta

class Game(models.Model):
    name = models.CharField(max_length=100)

class Comment(models.Model):
    texts = models.TextField()
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE, default=567)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id = models.IntegerField(primary_key=True)
    pub_date = models.DateTimeField(auto_now=False)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    replied_user_name =  models.CharField(max_length=125, default='None')

    def __str__(self):
        return self.texts