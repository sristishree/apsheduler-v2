from django.db import models
import uuid
from mongoengine import Document, EmbeddedDocument, fields



# Create your models here.
class tasks(models.Model):
    diagnosticsid = models.CharField(max_length=100,primary_key=True)
    correlationID = models.CharField(max_length=100,blank=True)
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



class intervalFields(EmbeddedDocument):
    intv_hrs = fields.StringField()
    intv_min = fields.StringField()
    intv_sec = fields.StringField()
    
    # value = fields.DynamicField(required=True)

class cronFields(EmbeddedDocument):
    job_year = fields.StringField()
    job_month = fields.StringField()
    job_day = fields.StringField()
    job_week = fields.StringField()
    job_dow = fields.StringField()
    job_hrs = fields.StringField()
    job_min = fields.StringField()
    job_sec = fields.StringField()
    

class dateFields(EmbeddedDocument):
    starttime = fields.StringField()


class schedPack(Document):
    diagnosticsid = fields.StringField(required=True)
    schedPack_id = fields.UUIDField(default=uuid.uuid4, editbale=False)
    jobtype = fields.StringField()
    dateSched = fields.ListField(fields.EmbeddedDocumentField(dateFields),null=True)
    intvSched = fields.ListField(fields.EmbeddedDocumentField(intervalFields),null=True)
    cronSched = fields.ListField(fields.EmbeddedDocumentField(cronFields),null=True)


class MongoConnectionWorkbook(object):

    def __init__(self):
        #client = MongoClient(mongo_host, mongo_port)
        self.db = client['schedulerPacks']

    def get_collection(self, name):
        self.collection = self.db[name]

class schedulerCollection(MongoConnectionWorkbook):

    def __init__(self, args):
       super(schedulerCollection, self).__init__()
       self.get_collection('schedPacks')
       self.args = args

    def create(self):
        '''
        Add a scheduler pack to the schedulerpack library.
        '''
        if(self.args['jobtype'] == 'date'):
            diagnosticsid = self.args['diagnosticsid']
            jobtype = self.args['jobtype']
            dateSched = self.args['dateSched']

            class_collection_id = self.collection.insert({
                'diagnosticsid' : diagnosticsid,
                'jobtype': jobtype,
                'dateSched': dateSched
                })

            new_class_collection = self.collection.find_one({'_id' : class_collection_id})

            output = {
                'diagnosticsid' : new_class_collection['diagnosticsid'],
                'jobtype': new_class_collection['jobtype'],
                'dateSched': new_class_collection['dateSched']
            }

            return output
            
        elif(self.args['jobtype'] == 'interval'):
            diagnosticsid = self.args['diagnosticsid']
            jobtype = self.args['jobtype']
            intervalSched = self.args['intervalSched']

            class_collection_id = self.collection.insert({
                'diagnosticsid' : diagnosticsid,
                'jobtype': jobtype,
                'intervalSched': intervalSched
                })

            new_class_collection = self.collection.find_one({'_id' : class_collection_id})

            output = {
                'diagnosticsid' : new_class_collection['diagnosticsid'],
                'jobtype': new_class_collection['jobtype'],
                'intervalSched': new_class_collection['intervalSched']
            }

            return output

        elif(self.args['jobtype'] == 'cron'):
            diagnosticsid = self.args['diagnosticsid']
            jobtype = self.args['jobtype']
            cronSched = self.args['cronSched']

            class_collection_id = self.collection.insert({
                'diagnosticsid' : diagnosticsid,
                'jobtype': jobtype,
                'cronSched': cronSched
                })

            new_class_collection = self.collection.find_one({'_id' : class_collection_id})

            output = {
                'diagnosticsid' : new_class_collection['diagnosticsid'],
                'jobtype': new_class_collection['jobtype'],
                'cronSched': new_class_collection['cronSched']
            }

            return output



        # class_collection_id = self.collection.insert(self.args)

        
        
