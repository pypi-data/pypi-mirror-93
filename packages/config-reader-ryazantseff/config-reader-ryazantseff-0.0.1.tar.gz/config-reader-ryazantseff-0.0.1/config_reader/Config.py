from pathlib import Path
import json, os, copy, logging

class Config(object):
    def __new__(cls, path='/app/config.json'):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
            cls.instance.cfgFilePath = Path(path)
        return cls.instance

    def __init__(self, path=''):
        if not hasattr(self, 'data'):
            if self.cfgFilePath.exists():
                self.data = self.readCfg()
            else:
                self.data = {}
                self.writeCfg()
        for key, field in self.data.items():
            if 'envName' in field.keys():
                self.setEnv(
                    field['envName'],
                    field['value']
                )

    def readCfg(self):
        data = {}
        with open(str(self.cfgFilePath)) as json_file:
            data = json.load(json_file)
        for key, field in data.items():
            if field.get('value', None) != None:
                if field['value'] == 'false':
                    data[key]['value'] = False
                elif field['value'] == 'true':
                    data[key]['value'] = True
            else:
                data[key]['value'] = os.environ[data[key]['envName']]
        return data
    
    def writeCfg(self):
        data = copy.deepcopy(self.data)
        for key, field in data.items():
            if field['value'] == False:
                data[key]['value'] = 'false'
            elif field['value'] == True:
                data[key]['value'] = 'true'
        self.cfgFilePath.parent.mkdir(parents=True, exist_ok=True)
        with open(str(self.cfgFilePath), 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)

    def get(self, name, field='value'):
        if name in self.data.keys():
            return self.data[name][field]
        else:
            return None

    def put(self, name, value, field='value'):
        if name not in self.data.keys():
            self.data[name] = {f'{field}': f'{value}'}
        else:
            self.data[name][field] = value

    def delete(self, name): 
        if name in self.data.keys():
            del self.data[name]

    def setEnv(self, name, val):
        if val == True:
            val = 'true'
        elif val == False:
            val = 'false'
        os.environ[name] = val

    @classmethod
    def drop(cls):
        "Drop the instance (for testing purposes)."
        if hasattr(cls, 'instance'):
            del cls.instance