from skeduler.settings import client

class getSchedulePack():
    def __init__(self):
        self.db = client['scheduler_packs']
        self.collection = self.db['schedPacks']
    
    def read(self,diagnosticsid):
        pack = self.collection.find_one({'diagnosticsid': diagnosticsid})
        allPacks = []

        if pack != None:
                
            p = {
                    'diagnosticsid' : pack['diagnosticsid'],
                    'jobtype' : pack['jobtype'],
                    'schedData' : pack['schedData']
                }
            
            allPacks.append(p)
            print('allPacks',allPacks)
            return allPacks
        else:
            return None

    def list_all(self):
        packs = self.collection.find()
        allPacks = []
        for pack in packs:
            p = {
                'diagnosticsid' : pack['diagnosticsid'],
                'jobtype' : pack['jobtype'],
                'schedData' : pack['schedData']
            }
            allPacks.append(p)
        print('allPacks',allPacks)
        return allPacks
    
    def delete_pack(self, schedName):
        pack = self.collection.find_one({'schedulerName': schedName})
        
        if pack != None:
            delete_pack = self.collection.remove({'schedulerName': schedName})
            return ("Successfully removed")
        else:
            return None
    
    def delete_all_packs(self):
        packs = self.collection.find()
        for pack in packs:
            delete_pack = self.collection.remove({'schedulerName': pack['schedulerName']})
        return("Successfully removed all packs")

    def checkSchedPackExists(self, uiData):
        in_diagID = uiData['diagnosticsid']
        packs = self.collection.find({'uiData.diagnosticsid': in_diagID}, {'uiData': []})
        for pack in packs:
            s_pack = pack['uiData'][0]
            if s_pack['jobtype'] == uiData['jobtype'] and s_pack['diagnosticsid'] == uiData['diagnosticsid'] and s_pack['target'] == uiData['target']:
                if s_pack['starttime'] == uiData['starttime']:
                    if uiData['jobtype'] == 'date':
                        if s_pack['starttime'] == uiData['starttime'] and s_pack['endtime'] == uiData['endtime']:
                            return True
                    if uiData['jobtype'] == 'interval':
                        if s_pack['intv_weeks'] == uiData['intv_weeks'] and s_pack['intv_days'] == uiData['intv_days'] and s_pack['intv_time'] == uiData['intv_time'] :
                            return True
                    if uiData['jobtype'] == 'cron':
                        if s_pack['date'] == uiData['date'] and s_pack['time'] == uiData['time'] and s_pack['dow'] == uiData['dow']:
                            return True
        return False
