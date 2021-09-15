from flask import Flask, jsonify, request, json, abort, make_response
from sqlalchemy.ext.declarative import DeclarativeMeta
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
import cloudinary
from cloudinary import uploader


app = Flask(__name__)

# make all APIs allow cross-origin access.
CORS(app)

app.secret_key = b'\r6\xafd\xc29\x0b\x86=\xcb\x8d\x0f\xd8\x9c\x10}r\x89@\x17\x820\x8e?'

# Local DB URL
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Masterdare@12@localhost/radio_statio" 

# Heroku DB URL
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://hsqbyhkrzskgzx:36f94ba4b49d4ad4b005e8dce3e57c27af48b2af545398788e1835d7df20acf8@ec2-34-254-69-72.eu-west-1.compute.amazonaws.com:5432/deolstqq6kogp" 

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from model import RadioStation


"""
GET api that fetches all created radio stations
"""
@app.route('/api/v1/radiostations/all', methods=['GET'])
def get_radio_stations_all():
    stations = db.session.query(RadioStation).all()  

    return make_response(jsonify(stations), 200)


"""
POST api that creates s radio station
"""
@app.route('/api/v1/radiostation', methods=['POST'])
# @cross_origin #Make this api accepts cross-origin access
def add_station():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        logo = request.files.get('logo')
        category = request.form.get('category')
        streamUrl = request.form.get('streamUrl')

        if logo:
            print(logo)
            cloudinary.config(cloud_name='oluwadare', folder='fm_logos', api_key='435671638148369', api_secret='Vfyxt0dsIo9wJhYOsUy0wXvj6eU')
            try:
                upload_result = uploader.upload(logo)
                station_obj = RadioStation(name=name,description=description,logo=upload_result['url'],category=category,streamUrl=streamUrl)
                db.session.add(station_obj)
                db.session.commit()
                return make_response(jsonify({"message": 'Request successful'}), 201)
            except Exception as e:
                print(upload_result)
                return make_response(jsonify({"message": 'Something bad happened'}), 400)
        
    return make_response(jsonify({"message": 'Bad request'}), 400)


"""
GET api that fetches one radio station based on given parameter
"""
@app.route('/api/v1/radiostations/<int:station_id>', methods=['GET'])
def get_radio_station(station_id):
    station = db.session.query(RadioStation).filter_by(id=station_id).all()  

    return make_response(jsonify(station), 200)


"""
Delete api that deletes one radio station based on given parameter
"""
@app.route('/api/v1/radiostations/<int:station_id>', methods=['DELETE'])
def delete_radio_station(station_id):
    station = db.session.query(RadioStation).filter_by(id=station_id).first()  
    if station:
        try:
            db.session.delete(station)
            db.session.commit()
            return make_response(jsonify({"status": "Deleted"}), 200)
        except Exception as e:
            return make_response(jsonify({"status": e}), 400)
    return abort(404)


"""
Update api that updates radio station data based on given parameters
"""
@app.route('/api/v1/radiostations/<int:station_id>', methods=['PUT'])
def update_radio_station(station_id):
    data = request.get_json()
    # print("testing", data)
    station = db.session.query(RadioStation).filter_by(id=station_id).first()  
    if station:
        try:            
            station.name = data['name']
            station.category = data['category']
            station.description = data['description']
            station.streamUrl = data['streamUrl']
            db.session.commit()
            return make_response(jsonify({"status": "Updated"}), 200)
        except Exception as e:
            # print(e)
            return make_response(jsonify({"status": "Error occured. Ask Admin."}), 400)
    return abort(404)


if __name__ == "__main__":
    app.run()