import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from django_apscheduler.jobstores import  DjangoJobStore,register_events, register_job

from django.conf import settings

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

def shutdown():
    scheduler.shutdown()

def job_exists(job_id):
    job = scheduler.get_job(job_id)
    if job == None:
        return False
    else:
        return True
    
def remove_job(job_id):
    scheduler.remove_job(job_id)