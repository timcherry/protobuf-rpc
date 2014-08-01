from flask import Flask
import logging

app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/ping')
def ping():
    return 'pong'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
