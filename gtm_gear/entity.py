import logging, time, json, re
logger = logging.getLogger(__name__)


# https://support.google.com/tagmanager/answer/7182738?hl=en
# Array.from(str).map( s => s.innerText)

BUILT_IN_VARIABLES_LIST = ["Click Element", "Click Classes", "Click ID", "Click Target", "Click URL", "Click Text", "Error Message", "Error URL", "Error Line", "Debug Mode", "Form Classes", "Form Element", "Form ID", "Form Target", "Form Text", "Form URL", "History Source", "New History Fragment", "New History State", "Old History Fragment", "Old History State", "Page Hostname", "Page Path", "Page URL", "Referrer", "Scroll Depth Threshold", "Scroll Depth Units", "Scroll Direction", "Container ID", "Container Version", "Environment Name", "Event", "HTML ID", "Random Number", "Video Current Time", "Video Duration", "Video Percent", "Video Provider", "Video Status", "Video Title", "Video URL", "Video Visible", "Percent Visible", "On-Screen Duration"]

class Entity():
    def __init__(self, data, parent):
        self.service = parent.service
        self.gtmservice = parent.gtmservice
        self.parent = parent
        self.data = data
        self.name = data.get("name")
        self.type = data.get("type")
        self.path = data.get("path")
        self.parameter = data.get("parameter")

        # Param for buit in variables
        self.path_additional_params = {}

        self.dependency_check_id = data.get("name")
        self.dependent_variables = []
        self.dependent_built_in_variables = []
        dependent_variables = re.findall("{{([A-Za-z0-9-_\s\.\/]+)}}", json.dumps(self.data))

        if len(dependent_variables) > 0:
            for variable in dependent_variables:
                if variable != "_event":
                    if variable in BUILT_IN_VARIABLES_LIST:
                        self.dependent_built_in_variables.append(variable)
                    else:
                        self.dependent_variables.append(variable)




    def update(self):
        self.service.execute(getattr(self.gtmservice.accounts().containers().workspaces(), self.entity_type)().update(path=self.path,body=self.data,))
        if self.parent.cache:
            self.parent.update_cache(self.entity_type)         

    def replace_data_fragment(self, old_text, new_text, api_update=True):
        try:
            changed_data = re.sub(old_text, new_text, json.dumps(self.data))
            self.data = json.loads(changed_data)
            if api_update:
                self.update()
            else:
                if self.parent.cache:
                    self.parent.update_cache(self.entity_type)  
        except Exception as e:
            raise ValueError(f"Can't change data for {self.name}: {e}")

    def rename_references(self, new_name, old_name, api_update=True):
        dependencies = self.get_depended()
        if dependencies['len']>0:
            for entity_type in dependencies.keys():
                if entity_type == 'len':
                    continue
                if f"dependent_{self.entity_type}" in dependencies[entity_type].keys():
                    for entity_name in dependencies[entity_type][f"dependent_{self.entity_type}"]:
                        entity = self.parent.get_entity(entity_type, entity_name)
                        entity.replace_data_fragment(f"{{{{{old_name}}}}}", f"{{{{{new_name}}}}}",api_update)
                        logger.info(f"Modifed {entity_type} {entity_name}")


    def delete(self, do_check = True):
        depended = self.get_depended()
        if do_check and depended['len']>0:
            logger.warning(f"Can't delete {self.entity_type} {self.name}: it used in {depended}")
        else:
            self.service.execute(getattr(self.gtmservice.accounts().containers().workspaces(), self.entity_type)().delete(**{**{'path':self.path},**self.path_additional_params}))
            self.parent.delete(self.entity_type, self.name)
         
    
    def get_depended(self):
        return self.parent.get_depended(self.entity_type, self.dependency_check_id, self.depended_checks)

    def get_template_name(self):
        for param in self.parameter:
            if param["type"] == "template" and param["key"] == "name":
                return param["value"]

    def get_param(self, param_key, param_type='template'):
        for param in self.parameter:
            if param["type"] == param_type and param["key"] == param_key:
                return param["list"] if param_type == 'list' else param["value"]
    
    def get_template_param(self, param_name):
        if self.parameter:
            for param in self.parameter:
                if param["type"] == "template" and param["key"] == param_name:
                    return param["value"]
    

    def set_folder_id(self, folder_id):
        self.data['parentFolderId']=folder_id

    def set_type(self, type):
        self.data['type'] = type
        self.type = type   
