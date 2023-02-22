import os
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from .models import db, User, UserPokemon, Pokemon


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'MySecretKey'
    app.config["JWT_SECRET_KEY"] = "super-secret"
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
    CORS(app)
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
jwt = JWTManager(app)  #setup flask jwt-e to work with app

@app.route('/')
def index():
  return '<h1>Poke API v1.0</h1>'

@app.route('/pokemon', methods=['GET'])
def listPokemon():
  pokemons = Pokemon.query.all()
  if pokemons:
    return [pokemon.get_json() for pokemon in pokemons]
  else:
    return []

@app.route('/signup', methods=['POST'])
def signUpUser():
  data = request.json
  new_user = User(data['username'], data['email'], data['password'])

  user_username = User.query.filter_by(username=data['username']).first()
  user_email = User.query.filter_by(email=data['email']).first()
  
  if user_username or user_email:
    return jsonify(error=f'username or email already exists'), 400
  
  db.session.add(new_user)
  db.session.commit()
  return jsonify(message=f'{new_user.username} created', email=f'{new_user.email}', password=f'{new_user.password}'), 201
  return jsonify(message=f'{new_user.username} created'), 201

def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
      return create_access_token(identity=username)
    return None

@app.route('/login', methods=['POST'])
def loginUser():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
      return jsonify(error='bad username/password given'), 401
  return jsonify(access_token=token)

@app.route('/mypokemon', methods=['POST'])
def saveUserPokemon():
  data = request.json
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)