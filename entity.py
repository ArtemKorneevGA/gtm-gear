import logging, time, json, re
logger = logging.getLogger(__name__)

from service import Service

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
        self.path = data.get("path")
        self.parameter = data.get("parameter")

        # Param for buit in variables
        self.path_additional_params = {}

        self.dependency_check_id = data.get("name")
        self.dependent_variables = []
        self.dependent_built_in_variables = []
        dependent_variables = re.findall("{{([A-Za-z0-9-_\s\.]+)}}", json.dumps(self.data))

        if len(dependent_variables) > 0:
            for variable in dependent_variables:
                if variable != "_event":
                    if variable in BUILT_IN_VARIABLES_LIST:
                        self.dependent_built_in_variables.append(variable)
                    else:
                        self.dependent_variables.append(variable)




    def update(self):
        (self.service.execute(self.gtmservice.accounts()
        .containers()
        .workspaces()
        .tags()
        .update(
            path=self.path,
            body=self.data,
        )
        ))
        self.parent.update_cache(self.entity_type)         

    def delete(self):
        depended = self.get_depended()
        if depended['len']>0:
            logger.warning(f"Can't delete {self.entity_type} {self.name}: it used in {depended}")
        else:
            self.service.execute(getattr(self.gtmservice.accounts().containers().workspaces(), self.entity_type)().delete(**{**{'path':self.path},**self.path_additional_params}))
            self.parent.delete(self.entity_type, self.name)
         
    
    def get_depended(self):
        return self.parent.get_depended(self.entity_type, self.dependency_check_id, self.depended_checks)