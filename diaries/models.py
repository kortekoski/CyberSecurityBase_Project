from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    admin = models.BooleanField(default=False)

class Entry(models.Model):
    content = models.CharField(max_length=140)
    pub_date = models.DateTimeField("date published")
    user = models.ForeignKey(User, on_delete=models.CASCADE)