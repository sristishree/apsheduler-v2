import logging
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import  DjangoJobStore,register_events, register_job
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED
from .models import tasks
from django.db.models import F
import requests
from django.conf import settings
from .diagnosticPack import diagnosticPack
# Create scheduler to run in a thread inside the application process settings.SCHEDULER_CONFIG {'apscheduler.timezone': 'Asia/Kolkata'}
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")



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
    register_events(scheduler)
    print("yyyyyyyyyy")
    scheduler.start()

def listjobs():
    scl = scheduler.get_jobs()
    return (scl)

def state():
    return scheduler.state

def shutdown_sched():
    scheduler.shutdown()

def job_exists(job_id):
    job = scheduler.get_job(job_id)
    print("**********")
    if job == None:
        return False
    else:
        return True
    
def get_job(job_id):
    job = scheduler.get_job(job_id)
    print("**********")
    if job == None:
        return None
    else:
        return False
    
def remove_job(job_id):
    scheduler.remove_job(job_id)

def sendRequest(diagID, correlationID):
    # fetchRequest = diagnosticPack()
    # command = fetchRequest.read(diagID)
    # command = command['command']
    headers = {'Content-Type': 'application/json'}
    data = {
        # "command": command,
        "correlationID": '',
        "diagnosticsid": diagID
    }
    '''
    data = { 
        "diagnosticsid" : diagID,
        "diagnostic_flag" : "True",
        "state_id": random.randint(1,10000)
        #"counter_": "int" Incremental
    }'''
    # url = 'http://mlapi2-svc/compiler?caller=scheduler'
    # res = requests.post(url, headers=headers, data=data)
    #scheduler_event(callback, arguments=[], MASK= EVENTS_ALL)
    print("Event fired", data)
'''
def sendRequest(diagID):
    
    b = tasks.objects.get(pk=int(diagID))
    lookupId = b.lookup_id
    jobRuns = b.job_runs

    print(diagID, "Reached sendReq()", lookupId, jobRuns)
'''


def add_DateJob(starttime,diagID,correlationid):
    scheduler.add_job(sendRequest, trigger='date', run_date=starttime,args=[diagID,correlationid], id=str(diagID), replace_existing=True)

def add_IntervalJob(intv_sec, intv_min, intv_hrs, intv_weeks, starttime, diagID, correlationid):
    scheduler.add_job(sendRequest,  trigger='interval',
                                    seconds=int(intv_sec),
                                    minutes=int(intv_min),
                                    hours = int(intv_hrs),
                                    weeks = intv_weeks,
                                    start_date=starttime,
                                    id=str(diagID), args=[diagID,correlationid],jitter=30,
                                    replace_existing=True)

def add_CronJob( job_year,job_month,job_day,job_week,job_dow,job_hrs,job_min,job_sec,starttime,enddate,diagID,correlationid):
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
                                        end_date=enddate,
                                        id=str(diagID), args=[diagID,correlationid],jitter=30,
                                        replace_existing=True)


def update_DateJob(starttime, diagID, correlationID):
    scheduler.reschedule_job(trigger='date',job_id=str(diagID),run_date=starttime)

def update_IntervalJob(intv_sec, intv_min, intv_hrs, intv_weeks, starttime, diagID):
    scheduler.reschedule_job(trigger='interval',
                            seconds=int(intv_sec),
                            minutes=int(intv_min),
                            hours = int(intv_hrs),
                            weeks = intv_weeks,
                            start_date=starttime,
                            job_id=str(diagID))

def update_CronJob( job_year,job_month,job_day,job_week,job_dow,job_hrs,job_min,job_sec,starttime,enddate,diagID):
    scheduler.reschedule_job(trigger='cron',
                            year=job_year,
                            month=job_month, 
                            day=job_day, 
                            week=job_week,
                            day_of_week=job_dow,
                            hour=job_hrs,
                            minute=job_min,
                            second=job_sec,
                            start_date=starttime,
                            end_date=enddate,
                            job_id=str(diagID))


def schedule_listener(event):
    
    try:
        a = tasks.objects.get(pk=int(event.job_id))
        
        a.job_runs = F('job_runs')+ 1

        if event.exception:
            print('Job crashed')
        else: 
            a.job_success = F('job_success')+1
            # job = scheduler.get_job(event.job_id)
            print('Job created', event.job_id)

        a.save()
    except:
        pass

    print("EVENT=====>",event)

scheduler.add_listener(schedule_listener,EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
