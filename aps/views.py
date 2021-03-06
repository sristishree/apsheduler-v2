from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from .serializer import TaskSerializer
from .diagnosticPack import diagnosticPack
from .models import tasks
#from .taskScheduler import *
from . import taskScheduler
from . import scheduler_helper
from django.http import HttpResponse
from threading import Thread
from .createData import createData

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    queryset = tasks.objects.all().order_by('diagnosticsid')
    serializer_class = TaskSerializer

class TaskAPIView(APIView):

    def schedulerPost(self,data,format=None):

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            resp_success,resp_obj, resp_status = taskScheduler.scheduleJob(request)
            print (resp_success,resp_obj)
            if resp_success:
                # a = tasks.objects.get(pk=int(request.data['diagID']))
                # a.job_runs = F('job_runs') + 1
                # print(serializer.data['diagID'])
                # query = tasks.objects.
                serializer.save()
            return HttpResponse({'resp_obj': resp_obj, 'status':resp_status})
            #return HttpResponse(resp_obj, status=resp_status)
        else:
            print(serializer.is_valid())
            return HttpResponse({'error':serializer.errors,'status':status.HTTP_400_BAD_REQUEST})
            #return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        t = Thread(target = self.schedulerPost, args = [request.data])
        t.daemon = True
        t.start()
        t.join()
        return HttpResponse({"success": "Data sent to compiler", "status": status.HTTP_202_ACCEPTED})
    
    '''
    def put(self, request, pk=None, format=None):
        pk = request.data['diagnosticsid']
        pk = str(pk)
        if scheduler_helper.job_exists(pk):
            try:
                user = tasks.objects.get(pk=pk)
            except:
                return HttpResponse({'error':"PK not present"})
                #return HttpResponse("PK not present")
            serializer = TaskSerializer(user, data = request.data)
            if serializer.is_valid():
                resp_success, resp_obj, resp_status = taskScheduler.updateJob(request)
                serializer.save()
                return HttpResponse({'resp_obj': resp_obj, 'status':resp_status})
                #return HttpResponse(resp_obj, status=resp_status)
            else:
                print(serializer.is_valid())
                return HttpResponse({'error':serializer.errors,'status':status.HTTP_400_BAD_REQUEST})
                #return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return HttpResponse({'resp_obj':"Job not found", 'status':status.HTTP_400_BAD_REQUEST})
    '''
    def put(self, request, pk=None, format=None):
        r_jobid = str(request.data['diagnosticsid'])
        if scheduler_helper.job_exists(r_jobid):
            try:
                a = tasks.objects.get(pk=request.data['diagnosticsid'])
                scheduler_helper.remove_job(r_jobid)
                a.delete()
            except:
                print("error:PK not present")
        else:
            print("resp_obj:Job not found", "status:status.HTTP_400_BAD_REQUEST")

        
        t = Thread(target = self.schedulerPost, args = [request.data])
        t.daemon = True
        t.start()
        t.join()

        


@api_view(['GET'])
def sched_list(request):
 schedules = []
 scl = scheduler_helper.listjobs()
#  xt = repr(scl[0].trigger)
#  jt = scl[0].trigger
#  print("XXXXXXXXXXXXXX",jt.start_date)
 for job in scl:
     jobdict = {}
    #  jt = type(job.trigger)

     jobdict['job_name'] = job.name
    #  jobdict['job_trigger'] = jt
     jobdict['next run'] = job.next_run_time    
     jobdict['diagnosticsid'] = job.args
    #  jobdict['job'] = job
    #  for f in job.trigger.fields:
    #      curval = str(f)
    #      jobdict[f.name] = curval

     schedules.append(jobdict)
 return HttpResponse(schedules)

@api_view(['POST'])
def sched_state(request):
        print(request.data,type(request.data))
        r_state = request.data['status']
        print(r_state,"wwwwwwwww")
        scheduler_state = scheduler_helper.state()
        print(scheduler_state)
        if r_state == 'start':
            if scheduler_state != 1:
                scheduler_helper.start_sched()
                print("Scheduler Started")
                return HttpResponse({'resp_obj':"STARTED", 'status': status.HTTP_200_OK})
                #return HttpResponse("STARTED", status=status.HTTP_200_OK)
            else:
                print("Scheduler already running")
                return HttpResponse({'resp_obj':"Scheduler already running"})
        elif r_state == 'stop':
            if scheduler_state != 0:
                sched_resp = scheduler_helper.shutdown_sched()
                print(sched_resp)
                if sched_resp == "STOPPED":
                    return HttpResponse({'resp_obj':"STOPPED", 'status': status.HTTP_200_OK})
                    #return HttpResponse("STOPPED", status=status.HTTP_200_OK)
                else:
                    return HttpResponse({'resp_obj':"Error stopping scheduler", 'status':status.HTTP_400_BAD_REQUEST})
            else:
                print("Scheduler not running")
                return HttpResponse({'resp_obj':"Scheduler not running"})
        elif r_state == 'state':
            if scheduler_state == 1:
                print("Scheduler Running")
                return HttpResponse({'resp_obj':1, 'status':status.HTTP_200_OK})
            else:
                return HttpResponse({'resp_obj':0, 'status':status.HTTP_200_OK})
        

@api_view(['POST'])
def sched_remove(request):
    r_jobid = str(request.data['diagnosticsid'])
    if scheduler_helper.job_exists(r_jobid):
        try:
            a = tasks.objects.get(pk=str(request.data['diagnosticsid']))
            scheduler_helper.remove_job(r_jobid)
            a.delete()
            return HttpResponse({'resp_obj':"Job Deleted", 'status':status.HTTP_200_OK})
        except:
            return HttpResponse({'error':"PK not present"})
    else:
        return HttpResponse({'resp_obj':"Job not found", 'status':status.HTTP_400_BAD_REQUEST})

@api_view(['POST'])
def write_data(request):
    data = createData()
    data.write()
    return HttpResponse('OK')

@api_view(['POST'])
def fetch(request):
    fetchRequest = diagnosticPack()
    diagID = str(request.data['diagnosticsid'])
    command = fetchRequest.read(diagID)
    if command == None:
        return HttpResponse({'resp_obj': 'Diagnostic Pack not found', 'status': status.HTTP_400_BAD_RQUEST})
    else:
        return HttpResponse({'resp_obj': command,'status': status.HTTP_200_OK})
    