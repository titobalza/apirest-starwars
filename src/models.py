from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    favorites = db.relationship('Favorites', backref='user', cascade='all, delete-orphan')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }


class Favorites(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, user_id, planet_id=None, character_id=None):
        self.user_id = user_id
        self.planet_id = planet_id
        self.character_id = character_id

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'planet_id': self.planet_id,
            'character_id': self.character_id,
            'created_at': self.created_at
        }


class Planet(db.Model):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    population = db.Column(db.String(50))

    def __init__(self, name, climate, terrain, population):
        self.name = name
        self.climate = climate
        self.terrain = terrain
        self.population = population

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'climate': self.climate,
            'terrain': self.terrain,
            'population': self.population
        }


class Character(db.Model):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    height = db.Column(db.String(10))
    mass = db.Column(db.String(10))
    hair_color = db.Column(db.String(20))
    skin_color = db.Column(db.String(20))
    eye_color = db.Column(db.String(20))
    birth_year = db.Column(db.String(10))
    gender = db.Column(db.String(10))

    def __init__(self, name, height, mass, hair_color, skin_color, eye_color, birth_year, gender):
        self.name = name
        self.height = height
        self.mass = mass
        self.hair_color = hair_color
        self.skin_color = skin_color
        self.eye_color = eye_color
        self.birth_year = birth_year
        self.gender = gender

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'mass': self.mass,
            'hair_color': self.hair_color,
            'skin_color': self.skin_color,
            'eye_color': self.eye_color,
            'birth_year': self.birth_year,
            'gender': self.gender
        }