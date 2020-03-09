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

        #   class_collection_id = self.collection.insert({
        #         'diagnosticsid' : diagnosticsid,
        #         'jobtype': jobtype,
        #         'intervalSched': intervalSched
        #         })

        #     new_class_collection = self.collection.find_one({'_id' : class_collection_id})

        #     output = {
        #         'diagnosticsid' : new_class_collection['diagnosticsid'],
        #         'jobtype': new_class_collection['jobtype'],
        #         'intervalSched': new_class_collection['intervalSched']
        #     }

        #     return output
        # print(data)
        # return data
        