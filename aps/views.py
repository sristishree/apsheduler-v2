from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from .serializer import TaskSerializer
from .models import tasks
#from .taskScheduler import *
from . import taskScheduler
from . import scheduler
# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = tasks.objects.all().order_by('diagID')
    serializer_class = TaskSerializer

class TaskAPIView(APIView):
    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            resp_obj, resp_status = taskScheduler.scheduleJob(request)
            # serializer.save()
            return Response(resp_obj, status=resp_status)
        else:
            print(serializer.is_valid())
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def sched_list(request):
 schedules = []
 scl = scheduler.listjobs()
#  xt = repr(scl[0].trigger)
#  jt = scl[0].trigger
#  print("XXXXXXXXXXXXXX",jt.start_date)
 for job in scl:
     jobdict = {}
    #  jt = type(job.trigger)

     jobdict['job_name'] = job.name
    #  jobdict['job_trigger'] = jt
     jobdict['next run'] = job.next_run_time    
     jobdict['diagID'] = job.args
    #  jobdict['job'] = job
    #  for f in job.trigger.fields:
    #      curval = str(f)
    #      jobdict[f.name] = curval

     schedules.append(jobdict)
 return Response(schedules)

@api_view(['POST'])
def sched_state(request):
    
        r_state = request.data['status']
        print(r_state,"wwwwwwwww")
        scheduler_state = scheduler.state()
        print(scheduler_state)
        if r_state == 'start':
            if scheduler_state != 1:
                scheduler.start_sched()
                print("Scheduler Started")
                return Response("STARTED", status=status.HTTP_200_OK)
            else:
                print("Scheduler already running")
                return Response("Scheduler already running")
        elif r_state == 'stop':
            if scheduler_state != 0:
                sched_resp = scheduler.shutdown_sched()
                print(sched_resp)
                if sched_resp == "STOPPED":
                    return Response("STOPPED", status=status.HTTP_200_OK)
                else:
                    return Response("Error stopping scheduler", status=status.HTTP_400_BAD_REQUEST)
            else:
                print("Scheduler not running")
                return Response("Scheduler not running")
        elif r_state == 'state':
            if scheduler_state == 1:
                print("Scheduler Running")
                return Response(1, status=status.HTTP_200_OK)
            else:
                return Response(0, status=status.HTTP_200_OK)
        

@api_view(['POST'])
def sched_remove(request):
    r_jobid = str(request.data['job_id'])
    if scheduler.job_exists(r_jobid):
        scheduler.remove_job(r_jobid)
        return Response("Job Deleted", status=status.HTTP_200_OK)
    else:
        return Response("Job not found", status=status.HTTP_400_BAD_REQUEST)