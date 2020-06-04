import json

class Ficha:

    def __init__(self, path, filename):

        self.path = path
        self.filename = filename

    def to_json(self):

        dict = {'filename' : self.filename,
                'path' : self.path}

        return json.dumps(dict)