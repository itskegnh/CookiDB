import flask, os, json, random, string, time
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# data/refer.json
#    stores information about which shard a database is on

# data/auth/shard-0.json
# data/auth/shard-1.json
# ...

# data/db/shard-0.json
# data/db/shard-1.json
# ...

# open ~/.cooki_config
#    read in the data
#    if it doesn't exist, create it
#    if it does exist, check if it's valid

CONFIG_PATH = os.path.expanduser('~/.cooki_config')

if not os.path.exists(CONFIG_PATH):
    config = {
        'shards': 10,
        'data_path': os.path.expanduser('~/cookidat/'),
    }
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)
    
with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)
    SHARDS = config['shards']
    DATA_PATH = config['data_path']

# create DATA_PATH if it doesn't exist
if not os.path.exists(DATA_PATH):
    os.makedirs(DATA_PATH)

# create DATA_PATH/auth if it doesn't exist
if not os.path.exists(os.path.join(DATA_PATH, 'auth')):
    os.makedirs(os.path.join(DATA_PATH, 'auth'))

# create DATA_PATH/db if it doesn't exist
if not os.path.exists(os.path.join(DATA_PATH, 'db')):
    os.makedirs(os.path.join(DATA_PATH, 'db'))

app = flask.Flask(__name__)

limiter = Limiter(app, key_func=get_remote_address)

def read_data(filename):
    if not os.path.exists(os.path.join(DATA_PATH, filename)):
        return {}
    with open(os.path.join(DATA_PATH, filename + '.json'), 'r') as f:
        data = json.load(f)
    return data

def write_data(filename, data):
    with open(os.path.join(DATA_PATH, filename), 'w') as f:
        json.dump(data, f)

def generate_id(length):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route('/')
def index():
    return flask.redirect('https://github.com/itskegnh/CookiDB')

@app.route('/create')
@limiter.limit('1/minute')
def create():
    # Create a new database
    shard_id = random.randint(1, SHARDS)-1
    while True:
        _id = generate_id(32)
        refer = read_data('refer')
        if _id not in refer:
            break
    
    # Update refer file
    refer[_id] = shard_id
    write_data('refer.json', refer)

    # Update AUTH Shard
    token = generate_id(72)
    auth = read_data('auth/shard-%s' % shard_id)
    auth[_id] = {
        'token': token,
        'created': time.time(),
        'last_interaction': time.time(),
        'interactions': 0,
    }
    write_data('auth/shard-%s.json' % shard_id, auth)

    # Update DB Shard
    db = read_data('db/shard-%s' % shard_id)
    db[_id] = {}
    write_data('db/shard-%s.json' % shard_id, db)

    return flask.jsonify({
        'database': _id,
        'token': token,
    })

@app.route('/database', methods=['GET', 'DELETE', 'PATCH', 'PUT'])
@limiter.limit('5/second')
def database():
    if flask.request.method == 'DELETE':
        # Delete an existing database
        _id = flask.request.args.get('id')
        token = flask.request.headers.get('Authorization')
        key = flask.request.args.get('key')
        refer = read_data('refer')
        if _id not in refer:
            return flask.jsonify({
                'error': 'Database does not exist',
            }), 404
        shard_id = refer[_id]

        # Validate Authentication
        auth = read_data('auth/shard-%s' % shard_id)
        if token is None or auth.get(_id, {}).get('token', None) != token:
            return flask.jsonify({
                'error': 'Invalid token',
            }), 401
        
        # Update AUTH Shard
        auth = read_data('auth/shard-%s' % shard_id)
        auth[_id]['last_interaction'] = time.time()
        auth[_id]['interactions'] += 1
        write_data('auth/shard-%s.json' % shard_id, auth)

        # Update DB Shard
        db = read_data('db/shard-%s' % shard_id)
        if key is None:
            db.pop(_id)
        else:
            db[_id].pop(key, None)
        write_data('db/shard-%s.json' % shard_id, db)

        return flask.jsonify({
            'success': True,
        })
    elif flask.request.method == 'GET':
        # View a database
        _id = flask.request.args.get('id')
        token = flask.request.headers.get('Authorization')
        key = flask.request.args.get('key')

        refer = read_data('refer')
        if _id not in refer:
            return flask.jsonify({
                'error': 'Database does not exist',
            }), 404
        shard_id = refer[_id]

        # Validate Authentication
        auth = read_data('auth/shard-%s' % shard_id)
        if token is None or auth.get(_id, {}).get('token', None) != token:
            return flask.jsonify({
                'error': 'Invalid token',
            }), 401
        
        # Update AUTH Shard
        auth = read_data('auth/shard-%s' % shard_id)
        auth[_id]['last_interaction'] = time.time()
        auth[_id]['interactions'] += 1
        write_data('auth/shard-%s.json' % shard_id, auth)

        # Return DB Shard
        db = read_data('db/shard-%s' % shard_id)
        if key is None:
            return flask.jsonify(db[_id])
        return flask.jsonify(db[_id].get(key, None))
    elif flask.request.method == 'PUT':
        # Write to database
        _id = flask.request.args.get('id')
        token = flask.request.headers.get('Authorization')
        data = flask.request.json

        refer = read_data('refer')
        if _id not in refer:
            return flask.jsonify({
                'error': 'Database does not exist',
            }), 404
        shard_id = refer[_id]

        # Validate Authentication
        auth = read_data('auth/shard-%s' % shard_id)
        if token is None or auth.get(_id, {}).get('token', None) != token:
            return flask.jsonify({
                'error': 'Invalid token',
            }), 401
        
        # Update AUTH Shard
        auth = read_data('auth/shard-%s' % shard_id)
        auth[_id]['last_interaction'] = time.time()
        auth[_id]['interactions'] += 1
        write_data('auth/shard-%s.json' % shard_id, auth)

        # Update DB Shard
        db = read_data('db/shard-%s' % shard_id)
        db[_id] = data
        write_data('db/shard-%s.json' % shard_id, db)

        return flask.jsonify({
            'success': True,
        })
    elif flask.request.method == 'PATCH':
        # Update a database
        _id = flask.request.args.get('id')
        token = flask.request.headers.get('Authorization')
        data = flask.request.json
        
        refer = read_data('refer')
        if _id not in refer:
            return flask.jsonify({
                'error': 'Database does not exist',
            }), 404
        shard_id = refer[_id]

        # Validate Authentication
        auth = read_data('auth/shard-%s' % shard_id)
        if token is None or auth.get(_id, {}).get('token', None) != token:
            return flask.jsonify({
                'error': 'Invalid token',
            }), 401
        
        # Update AUTH Shard
        auth = read_data('auth/shard-%s' % shard_id)
        auth[_id]['last_interaction'] = time.time()
        auth[_id]['interactions'] += 1
        write_data('auth/shard-%s.json' % shard_id, auth)

        # Update DB Shard
        db = read_data('db/shard-%s' % shard_id)
        db[_id].update(data)
        write_data('db/shard-%s.json' % shard_id, db)

        return flask.jsonify({
            'success': True,
        })

if __name__ == '__main__':
    app.run(debug=True)