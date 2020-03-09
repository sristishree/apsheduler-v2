from skeduler.settings import client
#db, name
class diagnosticPack():
    def __init__(self):
        self.db = client['scheduler']
        self.collection = self.db['diagPack']
    
    def read(self,diagnosticsid):
        data = self.collection.find_one({'diagnosticsid': diagnosticsid})
        print(data)
        #if data:
        return data
        