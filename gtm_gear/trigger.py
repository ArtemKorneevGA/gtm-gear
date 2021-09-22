import logging
logger = logging.getLogger(__name__)

from .entity import Entity

class Trigger(Entity):
    def __init__(self, data, parent):
        Entity.__init__(self, data, parent)
        self.entity_type ='triggers'
        self.dependency_check_id = str(data.get("triggerId"))
        self.triggers_references = []
        self.depended_checks = {
            'tags':['firing_triggers','blocking_triggers'],
            'triggers':['triggers_references']

        }
        self.get_dependencies()


    def get_dependencies(self):
        if self.type == 'triggerGroup':
            for parameter in self.parameter:
                if parameter['key'] == 'triggerIds':
                    for trigger in parameter['list']:
                        self.triggers_references.append(trigger['value'])

    def get_custom_event_template_param(self, param_name):
        if 'customEventFilter' in self.data:
            for param in self.data['customEventFilter'][0]['parameter']:
                if param["type"] == "template" and param["key"] == param_name:
                    return param["value"]