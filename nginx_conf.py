import crossplane, socket

class NginxConf:

    def __init__(self, filepath):
        #self.result = load(open(filepath))
        self.file = filepath
        self.payload = None

    def fetch_rtmp_conf(self):
        host = socket.gethostname()
        ipaddr = socket.gethostbyname(host)

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

        return {
            "port" : sever_port,
            "chunk" : chunk_size,
            "name" : application_name,
            "status" : live_status,
            "streams" : pushed_streams,
            "ip": ipaddr
        }

    def clear_streams(self, stream_list):
        new_list = []
        key, value = 'directive', 'push'

        for dict_item in stream_list:
            print("Evaluating: ", dict_item)
            if not (key in dict_item and value == dict_item[key]):
                new_list.append(dict_item)
        
        return new_list

    def update_rtmp_conf(self, request_form):
        
        config = crossplane.parse(self.file) 
        configs = config['config']

        request_form = request_form.to_dict(flat=False)
        print("Updating:", request_form)

        # Remove buttons from formd data dict
        if 'update' in request_form:
            del(request_form['update'])
        elif 'restart' in request_form:
            del(request_form['restart'])

        new_name = request_form.pop('name')
        new_port = request_form.pop('port')
        new_chunk = request_form.pop('chunk')

        new_livestatus = None
        try:
            new_livestatus = request_form.pop('livestatus')
        except:
            print("Live Status is set to off")
            new_livestatus = ['off']
        
        new_streams = []
        for item in request_form:
            new_streams.append(item)
        
        print("New streams to be added:", new_streams)

        

        print("===== WRITING TO FILE =====")

        for conf in configs:
            for key, value in conf.items():
                if key == 'parsed':
                    for dict_item in value:
                        if 'directive' in dict_item and 'rtmp' == dict_item['directive']:
                            for block_item in dict_item['block']:
                                for subdic in block_item['block']:
                                    # This is where I can finally extract all the properties I need to edit
                                    for k, v in subdic.items():
                                        if 'directive' == k and v == 'listen':
                                            subdic['args'] = new_port
                                            print("Writing new port: ", new_port)
                                        if 'directive' == k and v == 'chunk_size':
                                            subdic['args'] = new_chunk
                                            print("Writing new chunk size: ", new_chunk)                                      
                                        if 'directive' == k and v == 'application':
                                            subdic['args'] = new_name
                                            print("Writing new name: ", new_name)
                                            if 'block' in subdic:
                                                print("Before deleting dicts: ", subdic['block'])
                                                subdic['block'] = self.clear_streams(subdic['block'])       
                                                for app_item in subdic['block']:
                                                    for j, k in app_item.items():
                                                        if 'live' == k:
                                                            app_item['args'] = new_livestatus
                                                            print("New Live status: ", new_livestatus)                                                       
                                                print("After subdic value:", subdic['block'])


                                                for stream in new_streams:
                                                    stream_entry = {
                                                        'directive':'push',
                                                        'args': [stream]
                                                    }
                                                    print("Adding new dict")
                                                    subdic['block'].append(stream_entry)
                                                new_streams = []
        #config['config'] = configs
        self.payload = crossplane.build(configs[0]['parsed'])

        # Write to file
        conf_file = open("./nginx.conf", 'w')
        n = conf_file.write(self.payload)
        conf_file.close() 

    

