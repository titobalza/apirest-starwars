"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Favorites, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200
@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    result = []
    for person in people:
        person_data = {
            'name': person.name,
            'id': person.id,
            'height': person.height,
            'mass': person.mass,
            'hair_color': person.hair_color,
            'skin_color': person.skin_color,
            'eye_color': person.eye_color,
            'birth_year': person.birth_year,
            'gender': person.gender
        }
        result.append(person_data)
    return jsonify(result)

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Character.query.get(people_id)
    if person:
        return jsonify({'id': person.id, 'name': person.name})
    else:
        return jsonify({'error': 'Person not found'}), 404

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    result = []
    for planet in planets:
        planet_data = {
            'name': planet.name,
            'climate': planet.climate,
            'terrain': planet.terrain,
            'population': planet.population
        }
        result.append(planet_data)
    return jsonify(result)

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return jsonify({'id': planet.id, 'name': planet.name})
    else:
        return jsonify({'error': 'Planet not found'}), 404

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({'id': user.id, 'name': user.name})
    return jsonify(result)

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    result = []
    for favorite in favorites:
        planet = Planet.query.get(favorite.planet_id)
        result.append({'id': favorite.id, 'planet_id': planet.id, 'planet_name': planet.name})
    return jsonify(result)

@app.route('/people', methods=['POST'])
def add_character():
    rb = request.get_json()

    character = Character(
        name=rb.get('name'),
        height=rb.get('height'),
        mass=rb.get('mass'),
        hair_color=rb.get('hair_color'),
        skin_color=rb.get('skin_color'),
        eye_color=rb.get('eye_color'),
        birth_year=rb.get('birth_year'),
        gender=rb.get('gender')
    )

    db.session.add(character)
    db.session.commit()

    return f"Character {rb['name']} added successfully"

@app.route('/planets', methods=['POST'])
def add_planet():
    rb = request.get_json()

    planet = Planet(
        name=rb.get('name'),
        climate=rb.get('climate'),
        terrain=rb.get('terrain'),
        population=rb.get('population')
    )

    db.session.add(planet)
    db.session.commit()

    return jsonify({'message': 'Planet added successfully'})

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    favorite = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite planet added successfully'})

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.args.get('user_id')
    favorite = FavoritePeople(user_id=user_id, people_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite people added successfully'})

@app.route('/favorite/planets/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite planet deleted successfully'})
    else:
        return jsonify({'error': 'Favorite planet not found'}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.args.get('user_id')
    favorite = FavoritePeople.query.filter_by(user_id=user_id, people_id=people_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite people deleted successfully'})
    else:
        return jsonify({'error': 'Favorite people not found'}), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
