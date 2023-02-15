"""Flask app for Cupcakes"""
from flask import Flask, request, redirect, render_template, jsonify, remove
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

def serialize_cupcakes(cupcakes):
    return {
        "id": cupcakes.id,
        "flavor": cupcakes.flavor,
        "size": cupcakes.size,
        "rating": cupcakes.rating,
        "image": cupcakes.image
    }

app.route("/api/cupcakes")
def cupcake_list():
    """Returns a list of all cupcakes in database"""
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcakes(c) for c in cupcakes]

    return jsonify(cupcakes=serialized)

app.route('/api/cupcakes/<cupcake_id>')
def single_cupcake(cupcake_id):
    """Reurns a single cupcake in JSON"""
    cupcakes = Cupcake.query.get(cupcake_id)
    serialized = serialize_cupcakes(cupcakes)

    return jsonify(cupcakes=serialized)

app.route('/api/cupcakes', methods=["POST"])
def add_new_cupcake():
    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcakes(new_cupcake)

    return (jsonify(cupcakes=serialized), 201)

app.route('/api/cupcakes/<cupcake_id>', methods=["PATCH"])
def update_cucake(cupcake_id):
    cupcakes = Cupcake.query.get(cupcake_id)
    serialized = serialize_cupcakes(cupcakes)

    if serialized == None:
        return (404)
    else:
        return (jsonify(cupcakes=serialized))

app.routs('/api/cupcakes/<cupcake_id>', methods=["DELETE"])
def remove_cupcake(cupcake_id):
    cupcakes = Cupcake.query.get(cupcake_id)
    if cupcakes == None:
        return (404)
    else:
      return  remove(cupcakes)