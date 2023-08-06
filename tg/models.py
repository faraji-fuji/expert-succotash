from django.db import models

# Create your models here.
class Chat(models.Model):
    chat_id = models.IntegerField()
    title = models.CharField(max_length=256)
    username = models.CharField(max_length=256)
    type = models.CharField(max_length=256)

    