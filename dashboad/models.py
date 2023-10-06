from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=200)
    descriptions = models.TextField()

    class Meta:
        verbose_name = "notes" # for new name
        verbose_name_plural = "notes" # show name like notess
        
    def __str__(self):
        return self.title

class Homework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField('Title', max_length=100)
    description = models.TextField(default="")
    due = models.DateTimeField()
    is_finished = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=100)
    is_finished = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    

    