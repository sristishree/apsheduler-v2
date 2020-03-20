from pymongo import MongoClient
from skeduler.settings import client


class schedPack():

    def __init__(self):
        self.db = client['scheduler_packs']
        self.collection = self.db['schedPacks']

    def create_schedPack(self,
                    jobtype=None,
                    diagID=None,
                    starttime=None,
                    endtime=None,
                    intv_time=None,
                    hours=None,
                    minutes=None,
                    seconds=None,
                    weeks=None,
                    year=None,
                    month=None,
                    day=None,
                    day_of_week=None,
                    week=None,
                    request=None,
                    schedID=None,
                    schedName=None):

        if jobtype == 'date':
            r_data = {
                'schedulerID': schedID,
                'schedulerName': schedName,
                'diagnosticsid' : diagID,
                'jobtype': jobtype,
                'schedData': [{
                    'starttime':starttime
                }],
                'uiData': [
                    request
                ] 
            }
            # schedObj = schedulerCollection(r_data)
            # resp = schedObj.create()
        
            class_collection_id = self.collection.insert(r_data)

            new_class_collection = self.collection.find_one({'_id' : class_collection_id})

            output = {
                    'schedulerID' : new_class_collection['schedulerID'],
                    'schedulerName' : new_class_collection['schedulerName'],
                    'diagnosticsid' : new_class_collection['diagnosticsid'],
                    'jobtype': new_class_collection['jobtype'],
                    'schedData': new_class_collection['schedData'],
                    'uiData': new_class_collection['uiData']
                }

            return output
            print("Scheduler Pack created")

        elif jobtype == 'interval':
            r_data = {
                'schedulerID': schedID,
                'schedulerName': schedName,
                'diagnosticsid' : diagID,
                'jobtype': jobtype,
                'schedData': [{
                    'intv_sec':seconds,
                    'intv_min':minutes,
                    'intv_hrs':hours,
                    'intv_weeks':weeks,
                    'intv_days':day
                }],
                'uiData': [
                    request
                ] 
            }
            # schedObj = schedulerCollection(r_data)
            # resp = schedObj.create()

            class_collection_id = self.collection.insert(r_data)

            new_class_collection = self.collection.find_one({'_id' : class_collection_id})

            output = {
                    'schedulerID' : new_class_collection['schedulerID'],
                    'schedulerName' : new_class_collection['schedulerName'],
                    'diagnosticsid' : new_class_collection['diagnosticsid'],
                    'jobtype': new_class_collection['jobtype'],
                    'schedData': new_class_collection['schedData'],
                    'uiData': new_class_collection['uiData']

                }

            return output
            # return ("Scheduler Pack created")


        elif jobtype == 'cron':
            r_data = {
                'schedulerID': schedID,
                'schedulerName': schedName,
                'diagnosticsid' : diagID,
                'jobtype': jobtype,
                'schedData': [{
                    'starttime':starttime,
                    'job_year':year,
                    'job_month':month,
                    'job_day':day, 
                    'job_dow':day_of_week,
                    'job_hrs':hours,
                    'job_min':minutes,
                    'job_sec':seconds
                }],
                'uiData': [
                    request
                ]  
            }
            
            class_collection_id = self.collection.insert(r_data)

            new_class_collection = self.collection.find_one({'_id' : class_collection_id})

            output = {
                    'schedulerID' : new_class_collection['schedulerID'],
                    'schedulerName' : new_class_collection['schedulerName'],
                    'diagnosticsid' : new_class_collection['diagnosticsid'],
                    'jobtype': new_class_collection['jobtype'],
                    'schedData': new_class_collection['schedData'],
                    'uiData': new_class_collection['uiData']

                }

            return output