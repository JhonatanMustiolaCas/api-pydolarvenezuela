from flask import Flask
from flask import jsonify
from flask_cors import CORS
from src.obtaining import Api

api = Api()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "<p>Welcome to the Dolar Venezuela API. Go to documentation: https://github.com/fcoagz/api-pydolarvenezuela</p>"

@app.route('/api/v1/dollar/', methods=["GET"])
def get_monitors():
    return jsonify(api.get_all_monitors())

@app.route('/api/v1/dollar/unit/<string:key_monitor>', methods=["GET"])
def get_by_monitor(key_monitor: str):
    return jsonify(api.get_monitor(key_monitor))

@app.route('/api/v1/dollar/<string:section_dollar>', methods=["GET"])
def get_monitor_by_section(section_dollar: str):
    return jsonify(api.categorize_monitors(section_dollar))

@app.route('/api/v1/dollar/<string:section_dollar>/<string:key_monitor>', methods=["GET"])
def get_monitor_by_section_and_key(section_dollar: str, key_monitor: str):
    return jsonify(Api().categorize_monitors(section_dollar, key_monitor))

@app.route('/api/v1/dollar/tb/<string:value>/<string:key_monitor>', methods=["GET"])
def convertion_to_dollar(value: str, key_monitor: str):
    try:
        float(value)

        price = api.get_dollar(key_monitor)
        result = float(value) * float(price) if not type(price) == dict else price
        return jsonify({'value_to_bs': result, "information": api.get_monitor(key_monitor)})
    except ValueError:
        return jsonify({'message': f'Cannot GET information the value: {value}'})
    
@app.route('/api/v1/dollar/td/<string:value>/<string:key_monitor>', methods=["GET"])
def convertion_to_bs(value: str, key_monitor: str):
    try:
        float(value)

        price = api.get_dollar(key_monitor)
        result = float(value) / float(price) if not type(price) == dict else price
        return jsonify({'value_to_dollar': result, "information": api.get_monitor(key_monitor)})
    except ValueError:
        return jsonify({'message': f'Cannot GET information the value: {value}'})
    
app.run()