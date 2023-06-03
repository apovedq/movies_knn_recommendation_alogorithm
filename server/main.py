from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.setUpUser import selected_user

# Declare the APP server instance
app = Flask(__name__)
# Enable CORS policies
CORS(app)


# Variables to store values from front end.
currentUser = ""
currentMethod = ""
currenSliderValues = ""
currentKnnValue = ""

currentUserList = ["Andres Poveda", "Camilo Munera", "Juan Pablo Bueno"]
currentRecommendedMovie =  "Los piratas del caribe"

# GET Current user: string =============================================================================
@app.route("/getCurrentUser", methods=["GET"])
def setUser():
  return jsonify({"msg": currentUser})

# GET recomended users: list =============================================================================
@app.route("/get_recommended_user", methods=["GET"])
def setUserList():
  return jsonify({"msg": currentUserList})


# GET recomended users: list =============================================================================
@app.route("/get_recommended_movie", methods=["GET"])
def setMovie():
  return jsonify({"msg": currentRecommendedMovie})

  # GET Connection status =============================================================================
@app.route("/", methods=["GET"])
def index():
  return jsonify({"msg": "All good"})

# POST Endpoint =============================================================================
@app.route('/post_endpoint', methods=['POST'])
def create_data():
    # Get the data from the POST endpoint
    data = request.get_json()
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    return (jsonify({'response': 'ok all good'}), 201)


# POST changeName: string =============================================================================
@app.route('/post_name', methods=['POST'])
def define_user():
    # Get the data from the POST endpoint
    data = request.get_json()
    global myUser
    myUser = data
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    return (jsonify({'response': data}), 201)


# POST setMethod: number =============================================================================
@app.route('/post_method', methods=['POST'])
def define_method():
    # Get the data from the POST endpoint
    data = request.get_json()
    global myMethod
    myMethod = data
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    return (jsonify({'response': data}), 201)

# POST sliderValues: number =============================================================================
@app.route('/post_slider_values', methods=['POST'])
def define_slider_values():
    # Get the data from the POST endpoint
    data = request.get_json()
    global currenSliderValues
    currenSliderValues = data
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    return (jsonify({'response': data}), 201)

# POST sliderValues: number =============================================================================
@app.route('/post_knn_value', methods=['POST'])
def define_knn_value():
    # Get the data from the POST endpoint
    data = request.get_json()
    global currentKnnValue
    currentKnnValue = data
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    return (jsonify({'response': data}), 201)

# Execute the app instance
# The app will run locally in: http://localhost:5001/ after execution
if __name__ == "__main__":
  app.run(debug=True, port=5001)