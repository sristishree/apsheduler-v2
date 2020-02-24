from .scheduler import scheduler
from datetime import  datetime

# curl -d '{
#     "coid":"320",
#     "startime":"09-02-2019 19:40:11",
#     "command":"get-ip",
#     "jobtype":"interval",
#     "intv_seconds":"20"
# }' -H "Content-Type: application/json" -X POST http://localhost:8000/schedule
# '{
#     "coid":"320",
#     "startime":"09-02-2019 19:40:11",
#     "command":"get-ip",
#     "jobtype":"interval",
#     "interval": "{
#                 "seconds":"10",
#                 "hours":"22"
#                 }"
# }'




def resultfxn(coid):
    print(coid)


def dateformatter(cur_date):
    date_time = {
    "day": "",
    "date": "",
    "month": "",
    "year": "",
    "hour": "",
    "minutes": "",
    "seconds": ""
    }
    dt_obj = datetime.strptime(cur_date, "%Y-%m-%d %H:%M:%S")
    date_time["date"] = dt_obj.strftime('%d')
    date_time["month"] = dt_obj.strftime('%m')
    date_time["year"] = dt_obj.strftime('%Y')
    date_time["hour"] = dt_obj.strftime('%H')
    date_time["minutes"] = dt_obj.strftime('%M')
    date_time["seconds"] = dt_obj.strftime('%S')


def scheduleJob(data):
    print("=========",data.data)
    r_data = data.data
    coid = r_data['coid']
    intv = r_data['starttime']
    cmd = r_data['command']
    jobtype = r_data['jobtype']

    # start date
    if jobtype == 'date':
        return ("hi")
    elif jobtype == 'interval':
        # date when it starts, interval - secs, hours,minutes,date,day,weeks,startdate,enddate
        intv_sec = int(r_data['intv_seconds']) if "intv_seconds" in r_data else 0
        intv_min = int(r_data['intv_minutes']) if "intv_minutes" in r_data else 0
        intv_hrs = int(r_data['intv_hours'])if "intv_hours" in r_data else 0
        intv_weeks = int(r_data['intv_weeks']) if "intv_weeks" in r_data else 0
        print(intv_hrs,"oooooooooo", intv_sec)
        job = scheduler.add_job(resultfxn, trigger='interval',
                            seconds=intv_sec,
                            minutes=intv_min,
                            hours = intv_hrs,
                            weeks = intv_weeks,
                            id=coid, args=[coid],
                            replace_existing=True)
    
        return "job details: %s" % job
    if(cmd == 'shutdown'):
        scheduler.shutdown()
    elif(cmd == 'start'):
        scheduler.start()
    # else:
        # job = scheduler.add_job(resultfxn, trigger='interval', seconds=intv, id=coid,args=[coid],
        #     replace_existing=True)
    
        # return "job details: %s" % job