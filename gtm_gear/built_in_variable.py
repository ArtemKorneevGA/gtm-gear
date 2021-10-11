from .entity import Entity
from .utils import camel_case
import logging
logger = logging.getLogger(__name__)

class BuiltInVariable(Entity):
    def __init__(self, data, parent):
        Entity.__init__(self, data, parent)
        self.entity_type = 'built_in_variables'

        self.depended_checks = {
            'tags': ['dependent_built_in_variables'],
            'triggers': ['dependent_built_in_variables'],
            'variables': ['dependent_built_in_variables'],
        }
        self.param_names = {
            "Click Element":"clickElement", 
            "Client Name":"clientName", 
            "Click Classes":"clickClasses", 
            "Click ID":"clickId", 
            "Click Target":"clickTarget", 
            "Click URL":"clickUrl", 
            "Click Text":"clickText", 
            "Error Message":"errorMessage", 
            "Error URL":"errorUrl", 
            "Error Line":"errorLine", 
            "Event Name":"eventName", 
            "Event":"event", 
            "Debug Mode":"debugMode", 
            "Form Classes":"formClasses", 
            "Form Element":"formElement", 
            "Form ID":"formId",
            "Form Target":"formTarget", 
            "Form Text":"formText", 
            "Form URL":"formUrl", 
            "History Source":"historySource", 
            "New History Fragment":"newHistoryFragment", 
            "New History State":"newHistoryState", 
            "Old History Fragment":"oldHistoryFragment", 
            "Old History State":"oldHistoryState", 
            "Page Hostname":"pageHostname", 
            "Page Path":"pagePath", 
            "Page URL":"pageUrl", 
            "Referrer":"referrer", 
            "Scroll Depth Threshold":"scrollDepthThreshold", 
            "Scroll Depth Units":"scrollDepthUnits", 
            "Scroll Direction":"scrollDepthDirection", 
            "Container ID":"containerId", 
            "Container Version":"containerVersion", 
            "Environment Name":"environmentName", 
            "Event":"event", 
            "HTML ID":"htmlId", 
            "Random Number":"randomNumber", 
            "Video Current Time":"videoCurrentTime", 
            "Video Duration":"videoDuration", 
            "Video Percent":"videoPercent", 
            "Video Provider":"videoProvider", 
            "Video Status":"videoStatus", 
            "Video Title":"videoTitle", 
            "Video URL":"videoUrl", 
            "Video Visible":"videoVisible", 
            "Percent Visible":"elementVisibilityRatio", 
            "On-Screen Duration":"elementVisibilityTime"}

        if self.name in self.param_names.keys():
            self.path_additional_params = {'type': self.param_names[self.name]}
        else:
            self.path_additional_params = {'type': camel_case(self.name)}
