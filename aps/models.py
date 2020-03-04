import uuid
from django.db import models

# Create your models here.
class tasks(models.Model):
    diagnosticsid = models.CharField(max_length=100,primary_key=True)
    correlationID = models.CharField(max_length=100)
    starttime = models.CharField(max_length=100)
    jobtype = models.CharField(max_length=30)
    lookup_id = models.UUIDField(default=uuid.uuid4, editable=False)
    job_runs = models.IntegerField(default=0)
    job_success = models.IntegerField(default=0)
    #interval = models.CharField(max_length=30,blank=True) 
    # luID -> lookup
    #         -> Send req to Compiler wit diagID and ID
    # Incr -> Increments everytime successful & No change on fail    

def __str__(self):
        return self.coid