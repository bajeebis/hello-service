from flask import Flask, request, jsonify
import logging as log
import os, subprocess, json, yaml, logging as log
from threading import Thread
from kubernetes import client, config

# Set ENV vars
DEBUG_LEVEL = os.getenv('DEBUG_LEVEL')
if DEBUG_LEVEL == 'DEBUG':
    DEBUG_BOOL = True
    LOG_LEVEL = log.DEBUG
if DEBUG_LEVEL == 'INFO':
    DEBUG_BOOL = False
    LOG_LEVEL = log.INFO
# def debug_level(level):
#     info_dict

log.basicConfig(
    # filename=time.strftime('%I%p')+'-flask_app.log',
    level=LOG_LEVEL,
    format='%(asctime)s %(levelname)-8s %(message)s',
    handlers=[log.StreamHandler()]
)


class NoHealth(log.Filter):
    def filter(self, record):
        return 'GET /health' not in record.getMessage()
    
no_health = NoHealth()

app = Flask(__name__)
log.getLogger("werkzeug").addFilter(NoHealth())

@app.route('/health')
def health_check():
    return 'OK', 200 # Default during testing, will reconfigure

@app.route('/')
def catch_all():
    # content = request.get_json()
    UUID = request.headers.get('request-reference-no')
    log.info('Error received')
    return "Invalid or missing request", 200

@app.route('/api/hello', methods=['GET'])
def hello():
    # content = request.get_json()
    # UUID = request.headers.get('request-reference-no')
    log.info('Hit received')
    return "hello", 200

@app.route('/api/get_my_ip', methods=['GET'])
def get_my_ip():
    return jsonify({'client-ip': request.environ['REMOTE_ADDR'], 
                    'behind-proxy': request.environ['HTTP_X_FORWARDED_FOR']}), 200

@app.route('/api/all_headers', methods=['GET'])
def get_headers():
    return jsonify({'headers': str(dict(request.headers))}), 200

def run_flask():
    app.run(debug=DEBUG_BOOL, host='0.0.0.0', port=8080)

if __name__ == '__main__':
    log.info("Starting Application")

    flask_thread = Thread(target=run_flask())
    flask_thread.start()
