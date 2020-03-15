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
    
    def delete_pack(self, diagnosticsid):
        pack = self.collection.find_one({'diagnosticsid': diagnosticsid})
        if pack != None:
            delete_pack = self.collection.remove({'diagnosticsid': diagnosticsid})
            return ("Successfully removed")
        else:
            return None

        