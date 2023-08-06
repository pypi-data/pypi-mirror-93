

class Worker():

    def __init__(self, pool: int = 0, stage: int = 0, method: str = 'thread', daemon: bool = False):
        self.pool = pool
        self.stage = stage
        self.method = method
        self.daemon = daemon
        
    def apply(self):
        print('run')


class Plugin():

    def __init__(self, plugin_id):
        self.plugin_id = plugin_id
        self.services = {}
        self.workers = {}

        self.iterate_workers()
        
    def add_service(self, service):
        uuid = service.get('__uuid__')
        self.services[uuid] = service

    def iterate_workers(self):
        pass
        
    def apply(self):
        print(self.plugin_id)
