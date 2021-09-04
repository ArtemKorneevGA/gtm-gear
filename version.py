import logging
from datetime import datetime

logger = logging.getLogger(__name__)



class Version():
    def __init__(self, container, path):
        self.container = container
        self.path = path
        self.data = {}
    
    def init(self):
        self.data = self.container.service.execute(getattr(self.container.gtmservice.accounts().containers(), 'versions')()
                .get(path=self.path)
        )
        logger.info(f"Version {self.get_id()} inited")

    def get_id(self):
        if 'containerVersionId' in self.data:
            return self.data['containerVersionId']

    def compare(self, version):
        change_keys = ['tag', 'trigger', 'variable', 'folder', 'builtInVariable','customTemplate']

        logger.info(f"Start to compare {self.get_id()} and {version.get_id()}")

        version_old = dict(version.data)
        version_new =  self.data

 
        self.changes={}
        for key in ['deleted','added','changed']:
            self.changes[key]={}
            for change_key in change_keys:
                self.changes[key][change_key]=0
                self.changes[key]['total']=0
        self.changes['total']=0


        for entity_type in change_keys:
            # TO-DO: case if customTemplate exists only in one version
            if entity_type in version_new.keys():
                if entity_type == 'builtInVariable':
                    entity_id_name = 'name'
                elif entity_type == 'customTemplate':
                    entity_id_name = 'templateId'
                else:
                    entity_id_name =  f"{entity_type}Id"
                
                entity_len = len(version_new[entity_type])

                for i in range(0,entity_len):
                    entity = version_new[entity_type][i]

                    entity_id = entity[entity_id_name] 

                    if entity_type in version_old.keys():
                        old_entities = [en for en in version_old[entity_type] if en[entity_id_name] == entity_id]
                    else:
                        old_entities = []

                    if len(old_entities)==0:
                        self.changes['added'][entity_type]+=1
                        self.changes['added']['total']+=1
                        self.changes['total']+=1

                        entity["change_type"] = "added"

                    else:
                        if 'change_type' in old_entities[0].keys():
                            del old_entities[0]['change_type']
                        if entity != old_entities[0]:
                            self.changes['changed'][entity_type]+=1
                            self.changes['changed']['total']+=1

                            self.changes['total']+=1
                            entity["change_type"] = "changed"
                if entity_type in version_old.keys():
                    deleted = len(version_old[entity_type])  - len(version_new[entity_type]) + self.changes['added'][entity_type]
                else:
                    deleted = 0

                self.changes['deleted']['total'] += deleted
                self.changes['deleted'][entity_type]+= deleted
                self.changes['total']+= deleted

        return {
                "last_change_date" : datetime.fromtimestamp(int(self.data['fingerprint'])/1000),
                "changes_amount": self.changes['total'],
                "version_id": self.data['containerVersionId']
            }



