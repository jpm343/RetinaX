from flask import Flask
from flask import request, jsonify
from flask_cors import CORS

import SACnetwork
#special import
ArraySACnetwork = __import__("array-SACnetwork") 

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return "Hello world"

@app.route('/api/v1/resources/setparams', methods=['POST'])
def set_params():
    params = request.get_json()
    _g = SACnetwork.getGlobals()
    for category in params:
        try:
            for element in params[category]:
                _g[element] = params[category][element]    
        except TypeError:
            pass

    return ArraySACnetwork.scoped(7)

    #return jsonify(results)

@app.route('/api/v1/runsimulation', methods=['GET'])
def run_simulation():

    #results = []
    #results format: numpy hstack. parse to list
    results = ArraySACnetwork.scoped(7)
    #print(results)


    return jsonify(results) 

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', threaded=True)