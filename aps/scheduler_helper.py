import logging
import random
import requests
import pytz
import json
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import  DjangoJobStore,register_events, register_job
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from .models import tasks
from django.db.models import F
from django.conf import settings
from .diagnosticPack import diagnosticPack
from .schedulerPack import schedPack
from skeduler.settings import client as schedClient


# jobstores = {
#     'mongo': MongoDBJobStore(),
#     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
# }
# Create scheduler to run in a thread inside the application process settings.SCHEDULER_CONFIG {'apscheduler.timezone': 'Asia/Kolkata'}
scheduler = BackgroundScheduler(timezone = pytz.timezone('Asia/Calcutta'))
# scheduler.add_jobstore(DjangoJobStore(), "default")
scheduler.add_jobstore(MongoDBJobStore(client=schedClient),"default")


def start_sched():
    # Uncomment if statement to enable Debugging
    # if settings.DEBUG:
    #   	# Hook into the apscheduler logger
    #     logging.basicConfig()
    #     logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # Adding this job here instead of to crons.
    # This will do the following:
    # - Add a scheduled job to the job store on application initialization
    # - The job will execute a model class method at midnight each day
    # - replace_existing in combination with the unique ID prevents duplicate copies of the job

    # scheduler.add_job("core.models.MyModel.my_class_method", "cron", id="my_class_method", hour=0, replace_existing=True)
    # Add the scheduled jobs to the Django admin interface
    # register_events(scheduler)
    print("yyyyyyyyyy")
    scheduler.start()

def listjobs(job_id=None):
    if job_id == None:
        scl = scheduler.get_jobs()
        return (scl)
    else: 
        scl = scheduler.get_job(job_id)
        return (scl)

def state():
    return scheduler.state

def shutdown_sched():
    scheduler.shutdown()

def job_exists(job_id):
    job = scheduler.get_job(job_id)
    if job == None:
        return False
    else:
        return True
    
def get_job(job_id):
    job = scheduler.get_job(job_id)
    if job == None:
        return None
    else:
        return False

def printjobs():
    print(scheduler.print_jobs())
    return scheduler.print_jobs()

def remove_job(job_id):
    scheduler.remove_job(job_id)

def remove_all_jobs():
    jobs = scheduler.get_jobs()
    for job in jobs:
        try:
            a = tasks.objects.get(schedulerName=str(job.id))
            a.delete()
        except:
            return 400
    scheduler.remove_all_jobs()
    return 200
    

def convertYaml(command,ip,target):
    data = {
        "yaml_object": command,
        "host": ip,
        "os": target,
        "execute": "no"
    }
    data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    url = 'http://20.44.41.89/'
    res = requests.post(url, headers=headers,data=data)
    res = res.json()
    return res

def sendRequest(diagID, correlationID, schedName, schedulerID, target, ip, endtime, command, name):
    headers = {'Content-Type': 'application/json'}

    format = "%Y-%m-%d %H:%M:%S %Z%z"
    now_utc = datetime.now(pytz.timezone('UTC'))
    print(now_utc.strftime(format))
    now_asia = now_utc.astimezone(pytz.timezone('Asia/Kolkata'))
    timestamp = now_asia.strftime(format)

    data_compiler = {
        "command": command,
        "tabName": name,
        "schedulerName": schedName,
        "schedulerID": schedulerID,
        "correlationID": correlationID,
        "diagnosticsid": diagID,
        "diagnostics_flag": True,
        "stateid": random.randint(1,10000000),
        "target_env": target,
        "host": ip,
        "end_time": endtime,
        "timestamp": timestamp
    }

    data = json.dumps(data_compiler)
    
    url = 'http://mlapi2-svc/compiler?caller=scheduler'
    res = requests.post(url, headers=headers, data=data)
    #scheduler_event(callback, arguments=[], MASK= EVENTS_ALL)
    print("Event fired", data)


def add_DateJob(starttime,diagID,correlationid, schedName, schedulerID,target,ip,endtime=None):
    fetchRequest = diagnosticPack()
    command,name = fetchRequest.read(diagID)
    command = json.dumps(command)
    if target in {'windows','linux','windowshost','linuxhost'}:
        res = convertYaml(command,ip,target)
        command = res
    scheduler.add_job(sendRequest, trigger='date', run_date=starttime,args=[diagID,correlationid,schedName,schedulerID,target,ip,command,name], id=str(schedName), replace_existing=True)

def add_IntervalJob(intv_sec, intv_min, intv_hrs, intv_weeks, intv_days, starttime, endtime, diagID, correlationid,schedName, schedulerID, target,ip):
    fetchRequest = diagnosticPack()
    command,name = fetchRequest.read(diagID)
    command = json.dumps(command)
    if target in {'windows','linux','windowshost','linuxhost'}:
        print(target,"TTTTTTT")
        res = convertYaml(command,ip,target)
        command = res
    scheduler.add_job(sendRequest,  trigger='interval',
                                    seconds=int(intv_sec),
                                    minutes=int(intv_min),
                                    hours = int(intv_hrs),
                                    weeks = intv_weeks,
                                    days = intv_days,
                                    start_date=starttime,
                                    end_date = endtime,
                                    id=str(schedName), 

                                    args=[diagID,correlationid,schedName,schedulerID,target,ip,endtime,command,name],
                                    jitter=10,
                                    replace_existing=True)

def add_CronJob( job_year,job_month,job_day,job_week,job_dow,job_hrs,job_min,job_sec,starttime,endtime,diagID,correlationid,schedName,schedulerID,target,ip):
    fetchRequest = diagnosticPack()
    command,name = fetchRequest.read(diagID)
    command = json.dumps(command)
    if target in {'windows','linux','windowshost','linuxhost'}:
        res = convertYaml(command,ip,target)
        command = res
    scheduler.add_job(sendRequest, trigger='cron',
                                        year=job_year,
                                        month=job_month, 
                                        day=job_day, 
                                        week=job_week,
                                        day_of_week=job_dow,
                                        hour=job_hrs,
                                        minute=job_min,
                                        second=job_sec,
                                        start_date=starttime,
                                        end_date=endtime,
                                        id=str(schedName), args=[diagID,correlationid,schedName,schedulerID,target,ip,endtime,command,name],jitter=10,
                                        replace_existing=True)


def schedule_listener(event):
    
    try:
        a = tasks.objects.get(pk=int(event.job_id))
        
        a.job_runs = F('job_runs')+ 1

        if event.exception:
            print('Job crashed')
        else: 
            a.job_success = F('job_success')+1
            # job = scheduler.get_job(event.job_id)
            print('Job ran', event.job_id)

        a.save()
    except:
        pass

    print("EVENT=====>",event)

scheduler.add_listener(schedule_listener,EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
