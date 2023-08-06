from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CalEvents(models.Model):
    title = models.CharField(max_length=20)
    content = models.CharField(max_length=100)
    date = models.DateField()
    users = models.ManyToManyField(User)

class Info(models.Model):
    salary = models.IntegerField()
    userID = models.ForeignKey(User, on_delete=models.CASCADE)