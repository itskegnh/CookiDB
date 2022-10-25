import requests

class Database:
    ENDPOINT = 'http://db.cooki.lol/'
    def __init__(self, params):
        self.id = params['database']
        self.token = params['token']
        self.session = requests.Session(
            headers={
                'Authorization': self.token,
            },
        )
    
    def read(self, key=None):
        if key is None:
            response = self.session.get(
                self.ENDPOINT + 'database',
                params={
                    'id': self.id,
                },
            )
        else:
            response = self.session.get(
                self.ENDPOINT + 'database',
                params={
                    'id': self.id,
                    'key': key,
                },
            )
        response.raise_for_status()
        return response.json()

    def write(self, data):
        response = self.session.put(
            self.ENDPOINT + 'database',
            params={
                'id': self.id,
            },
            json=data,
        )
        response.raise_for_status()
        return response.json()
    
    def clear(self, key=None):
        if key is None:
            response = self.session.delete(
                self.ENDPOINT + 'database',
                params={
                    'id': self.id,
                },
            )
        else:
            response = self.session.delete(
                self.ENDPOINT + 'database',
                params={
                    'id': self.id,
                    'key': key,
                },
            )
        response.raise_for_status()
        return response.json()
    
    def delete(self, key=None):
        return self.clear(key)
    
    def update(self, data):
        response = self.session.patch(
            self.ENDPOINT + 'database',
            params={
                'id': self.id,
            },
            json=data,
        )
        response.raise_for_status()
        return response.json()