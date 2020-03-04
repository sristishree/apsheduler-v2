from django.db import models

# Create your models here.
class tasks(models.Model):
    diagID = models.IntegerField(primary_key=True)
    #command = models.CharField(max_length=100)
    starttime = models.CharField(max_length=100)
    jobtype = models.CharField(max_length=30)
    #interval = models.CharField(max_length=30,blank=True)
    

def __str__(self):
        return self.coid