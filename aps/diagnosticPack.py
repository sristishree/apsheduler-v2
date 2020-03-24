from skeduler.settings import client
import ruamel.yaml
import json
#db, name
class diagnosticPack():
    def __init__(self):
        self.db = client['command_classes']
        self.collection = self.db['diagnostics_collection'] 
    
    def read(self,diagnosticsid):
        data = self.collection.find_one({'id': diagnosticsid})
        yaml = ruamel.yaml.YAML(typ='safe')
        camlData = yaml.load(data['camlCode'])
        tabName = yaml.load(data['tabName'])
        print(camlData[0],"DATA FROM DIAG PACK",data)
        #if data:
        #return (json.dumps(camlData),tabName)
        return(camlData,tabName)