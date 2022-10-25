import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
    # redirect to github https://github.com/itskegnh/CookiDB
    return flask.redirect('https://github.com/itskegnh/CookiDB')

if __name__ == '__main__':
    app.run(debug=True)