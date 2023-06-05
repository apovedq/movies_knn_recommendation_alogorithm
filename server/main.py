from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.setUpUser import selected_user
import json

# obtenemos la clase del backend de recomendacion
from recomendacion import Rec

rec = Rec()

rec.exec()

# recomendacion sin ningun cambio de front
print(rec.get_final_dataframe())


# Declare the APP server instance
app = Flask(__name__)
# Enable CORS policies
CORS(app)

# GET Current user: string =============================================================================
@app.route("/getCurrentUser", methods=["GET"])
def setUser():
    return jsonify({"Access-Control-Allow-Origin": "*", "msg": rec.get_user_select()})

# GET recomended users: list =============================================================================
@app.route("/get_recommended_user", methods=["GET"])
def setUserList():
  rec.exec()
  print("VECINOS: \n", rec.get_vecinos());
  return jsonify({"msg": list(rec.get_vecinos().keys())})


# GET recomended users: list =============================================================================
@app.route("/get_recommended_movie", methods=["GET"])
def setMovie():
  print("RECOMENDACIONES: \n", rec.get_final_dataframe())
  return jsonify({"msg": rec.get_final_dataframe()["Name"].to_list()[0]})

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
        resp = (jsonify({'error': 'No data provided'}), 400)
        return resp
    print("USUARIO ACTUAL \n", myUser['answer'])
    resp = (jsonify({"Access-Control-Allow-Origin": "*",'response': data}), 201, {'Access-Control-Allow-Origin': '*'})
    print(resp)

    rec.set_user_select(myUser['answer'])

    return resp

# POST setMethod: number =============================================================================
@app.route('/post_method', methods=['POST'])
def define_method():
    # Get the data from the POST endpoint
    data = request.get_json()
    global myMethod
    myMethod = data
    if not data:
        return (jsonify({'error': 'No data provided'}), 400)
    print("METODO ACTUAL \n",myMethod['answer'])

    rec.set_agr_met(myMethod['answer'])

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
    print("PESOS ACTUALES \n",currenSliderValues['answer'])

    nuevosPesos = []
    for i in currenSliderValues['answer']:
        nuevosPesos.append(float(i)/10)

    print("PESOS NORMALIZADOS \n", nuevosPesos)

    rec.set_pesos(nuevosPesos)

    #print(rec.get_pesos())

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
    print("KNN ACTUAL \n", currentKnnValue['answer'])

    rec.set_num_vec(int(currentKnnValue['answer']))

    return (jsonify({'response': data}), 201)

# Execute the app instance
# The app will run locally in: http://localhost:5001/ after execution
if __name__ == "__main__":
  app.run(debug=True, port=5001)
