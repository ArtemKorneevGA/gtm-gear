import logging
logger = logging.getLogger(__name__)

from entity import Entity

class Tag(Entity):
    def __init__(self, data, parent):
        Entity.__init__(self, data, parent)
        self.entity_type ='tags'

        self.firing_triggers = []
        self.blocking_triggers = []
        self.setup_tags = []
        self.teardown_tags = []
        self.depended_checks = {
            'tags':['setup_tags','teardown_tags']
        }
        
        self.get_dependencies()

    def get_dependencies(self):


        if self.data.get("teardownTag"):
            for teardown_trigger in self.data['teardownTag']:
                self.teardown_tags.append(
                    teardown_trigger["tagName"]
                )

        if self.data.get("setupTag"):
            for setupTag in self.data['setupTag']:
                self.setup_tags.append(setupTag["tagName"])

        if self.data.get("firingTriggerId"):
            self.firing_triggers = self.data["firingTriggerId"]
 
        if self.data.get("blockingTriggerId"):
            self.blocking_triggers = self.data["blockingTriggerId"]
 
    def get_ua_type(self):
        for param in self.parameter:
            if param["type"] == "template" and param["key"] == "trackType":
                return param["value"]
 
    def is_ua_ecommerce(self):
        for param in self.parameter:
            if param["type"] == "boolean" and param["key"] == "enableEcommerce":
                return True if param["value"] == 'true' else False     
        return False

    def set_html(self, value):
        for param in self.parameter:
            if param["type"] == "template" and param["key"] == "html":
                param["value"] = value

    def isPaused(self):
        if "paused" in self.data.keys() and self.data['paused']:
            return True
        return False