import crossplane

class NginxConf:

    def __init__(self, filepath):
        #self.result = load(open(filepath))
        self.file = filepath
        self.payload = None

    def fetch_rtmp_conf(self):
        sever_port = None
        chunk_size = None
        pushed_streams = []
        live_status = ''  # Either on or off
        application_name = ''

        # TODO: Improve this by making going to the exact spot in the dict I need rather than iterating over it, because I dont care about the other
        # TODO: stuff anyways.
        # Once in connfig->parsed and directive == "rtmp"->server->block-->application-->block ---- keywords = []
        config = crossplane.parse(self.file)
        self.payload = config
        configs = config['config']
        for conf in configs:
            for key, value in conf.items():
                if key == 'parsed':
                    #print(key, value)
                    for dict_item in value:
                        if 'directive' in dict_item and 'rtmp' == dict_item['directive']:
                            for block_item in dict_item['block']:
                                for subdic in block_item['block']:
                                    # This is where I can finally extract all the properties I need to edit
                                    for k, v in subdic.items():
                                        if 'directive' == k and v == 'listen':
                                            sever_port = subdic['args'][0]
                                            print("Server Port found: ", sever_port)                     
                                        if 'directive' == k and v == 'chunk_size':
                                            chunk_size = subdic['args'][0]
                                            print("Chunk Size found: ", chunk_size)                                      
                                        if 'directive' == k and v == 'application':
                                            application_name = subdic['args'][0]
                                            print("Application name found: ", application_name)
                                            if 'block' in subdic:
                                                for app_item in subdic['block']:
                                                    for j, k in app_item.items():
                                                        if 'live' == k:
                                                            live_status = app_item['args'][0]
                                                            print("Live status: ", live_status)                                                       
                                                        if 'push' == k:
                                                            pushed_streams.append(app_item['args'][0])
        print("Pushing to: ", pushed_streams)
        return {
            'port' : sever_port,
            "chunk" : chunk_size,
            "name" : application_name,
            "status" : live_status,
            "streams" : pushed_streams
        }

    def update_rtmp_conf(self, updates):
        
        config = crossplane.parse(self.file) 
        configs = config['config']
        for conf in configs:
            for key, value in conf.items():
                if key == 'parsed':
                    #print(key, value)
                    for dict_item in value:
                        if 'directive' in dict_item and 'rtmp' == dict_item['directive']:
                            for block_item in dict_item['block']:
                                for subdic in block_item['block']:
                                    # This is where I can finally extract all the properties I need to edit
                                    for k, v in subdic.items():
                                        if 'directive' == k and v == 'listen':
                                            subdic['args'][0] = [updates['port']]
                                            print("New Server Port: ", subdic['args'][0])                     
                                        if 'directive' == k and v == 'chunk_size':
                                            subdic['args'][0] = [updates['chunk']]
                                            print("New Chunk Size: ", subdic['args'][0])                                      
                                        if 'directive' == k and v == 'application':
                                            application_name = subdic['args'][0]
                                            print("Application name found: ", application_name)
                                            if 'block' in subdic:
                                                for app_item in subdic['block']:
                                                    for j, k in app_item.items():
                                                        if 'live' == k:
                                                            live_status = app_item['args'][0]
                                                            print("Live status: ", live_status)                                                       
                                                        if 'push' == k:
                                                            pushed_streams.append(app_item['args'][0])

    

conf = NginxConf("./nginx.conf")

