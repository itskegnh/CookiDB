import flask, pymongo, os, random, string, time

mongo_secret = os.getenv('MONGO')
if mongo_secret is None:
    with open('mongo.secret') as f:
        mongo_secret = f.read().strip()

client = pymongo.MongoClient(mongo_secret)
db = client['CookiDB']
collection = db['databases']

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.redirect('https://github.com/itskegnh/CookiDB')

@app.route('/create', methods=['GET'])
def create():
    generate_id = lambda x: ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(x))
    x = 9
    while True:
        database_id = generate_id(x)
        if collection.find_one({'_id': database_id}) is None: break
        x += 1
    token = generate_id(32)
    data = {
        '_id': database_id,
        'token': token,
        'data': {},
        'created': int(time.time()),
    }
    collection.insert_one(data)
    return flask.jsonify(data)

@app.route('/db', methods=['GET', 'POST', 'DELETE'])
def database():
    database_id = flask.request.args.get('id')
    overwrite = flask.request.args.get('overwrite', 'false').lower() == 'true'
    token = flask.request.headers.get('Authorization')
    if database_id is None or token is None: return flask.jsonify({'error': 'Missing id or token'}), 400
    data = collection.find_one({'_id': database_id})
    if data is None: return flask.jsonify({'error': 'Database not found'}), 404
    if data.get('token', None) != token: return flask.jsonify({'error': 'Invalid token'}), 401
    
    if flask.request.method == 'GET':
        return flask.jsonify(data['data'])
    elif flask.request.method == 'POST':
        data['data'] = flask.request.get_json()
        if overwrite:
            collection.update_one({'_id': database_id}, {'$set': {'data': data['data']}})
        else:
            data = collection.find_one({'_id': database_id})
            data['data'].update(flask.request.get_json())
            collection.update_one({'_id': database_id}, {'$set': {'data': data['data']}})
        return flask.jsonify({'success': True})
    elif flask.request.method == 'DELETE':
        collection.delete_one({'_id': database_id})
        return flask.jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)