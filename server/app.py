# server/app.py
#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def home():
    return "Earthquake API"

@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    
    if earthquake:
        return jsonify(earthquake.to_dict())
    else:
        response = make_response(
            jsonify({"message": f"Earthquake {id} not found."}),
            404
        )
        return response

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    return jsonify({
        "count": len(earthquakes),
        "quakes": [earthquake.to_dict() for earthquake in earthquakes]
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)