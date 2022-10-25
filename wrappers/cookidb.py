import requests, json

class Database:
    ENDPOINT = 'http://db.cooki.lol/'
    def __init__(self, database_id, token):
        self.id = database_id
        self.token = token
        self.headers = {'Authorization': token}
    
    @classmethod
    def create(cls):
        r = requests.get(cls.ENDPOINT + 'create')
        data = r.json()
        return cls(data['_id'], data['token'])

    @classmethod
    def connect(cls, database_id, token):
        return cls(database_id, token)
    
    def read(self):
        url = self.ENDPOINT + 'db'
        r = requests.get(url, params={'id': self.id}, headers=self.headers)
        return r.json()
    
    def write(self, data, overwrite=True):
        url = self.ENDPOINT + 'db'
        r = requests.post(url, params={'id': self.id, 'overwrite': overwrite}, headers=self.headers, json=data)
        return r.json()
    
    def delete(self):
        url = self.ENDPOINT + 'db'
        r = requests.delete(url, params={'id': self.id}, headers=self.headers)
        return r.json()
    
    def __repr__(self):
        return f'<Database id={self.id}>'
    
    def __str__(self):
        return self.__repr__()
    
    def __getitem__(self, key):
        return self.read()[key]
    
    def __setitem__(self, key, value):
        data = {key: value}
        self.write(data, overwrite=False)
    
    def __delitem__(self, key):
        data = self.read()
        del data[key]
        self.write(data, overwrite=True)
    
    def __contains__(self, key):
        return key in self.read()
    
    def __iter__(self):
        return iter(self.read())
    
    def __len__(self):
        return len(self.read())