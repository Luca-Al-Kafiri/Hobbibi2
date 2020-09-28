from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.

class User(AbstractUser):
    pass
    country = models.CharField(max_length=64, default='G')
    city = models.CharField(max_length=64, default='Tbilisi')
    age = models.IntegerField(default=30)

class Hobbi(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Hobbies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobbi = models.ForeignKey(Hobbi, on_delete=models.CASCADE)

    def serialize(self):
        return {
            "user": self.user.username,
            "hobbi": self.hobbi.name,
            "age": self.user.age,
        }

    def __str__(self):
        return f"{self.hobbi}"
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender.username,
            "recipient": self.recipient.username,
            "message": self.message,
            "read": self.read,
            "timestamp": self.timestamp.strftime("%b %d, %Y %-H:%-M"),
        }

