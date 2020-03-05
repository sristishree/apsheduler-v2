from pymongo import MongoClient
from skeduler.settings import client

class createData():
    def __init__(self):
        self.db = client['scheduler']
        self.collection = self.db['diagPack']

    def write(self, list_diagnosticsid,list_command):
        '''
        dict1 = {'diagnosticsid':'1',
                'command': 
                    {"Command":{"query":"get-ip","input":"null","host":"52.168.178.43","os":"linux"}
                    }, 'correlationID': ''}
        dict2 = {'diagnosticsid':'2',
                'command':
                    {"Command":{"query":"get-ip","input":"null","host":"52.168.178.43","os":"linux"}
                }, 'correlationID': ''}
        x = self.collection.insert_one(dict1)
        print(x)
        y = self.collection.insert_one(dict2)
        print(y)
        '''
        for i in len(list_diagnosticsid):
            x = self.collection.insert_one({'diagnosticsid':list_diagnosticsid[i],'command':list_command[i],'correlationid':''})
            print(x)