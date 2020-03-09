from skeduler.settings import client
#db, name
class getSchedulePack():
    def __init__(self):
        self.db = client['scheduler_packs']
        self.collection = self.db['schedPacks']
    
    def read(self,diagnosticsid):
        data = self.collection.find_one({'diagnosticsid': diagnosticsid})
        print(data)
        #if data:
        return data

    def list_all(self):
        data = self.collection.find()
        print(data)
        return data
        