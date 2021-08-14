import logging
logger = logging.getLogger(__name__)

from entity import Entity

class Trigger(Entity):
    def __init__(self, data, parent):
        Entity.__init__(self, data, parent)
        self.entity_type ='triggers'
        self.dependency_check_id = str(data.get("triggerId"))

        self.depended_checks = {
            'tags':['firing_triggers','blocking_triggers']
        }
