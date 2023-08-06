

class Plugin():

    def __init__(self, plugin_id):
        self.plugin_id = plugin_id

    def add_log(self, log):
        pass
        
    def add_variables(self, variables):
        pass

    def add_eventhandler(self, event_handler):
        pass

    def add_auxiliary(self, auxiliary):
        pass
        
    def apply(self):
        print(self.plugin_id)
