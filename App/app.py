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
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')
  email = data.get('email')
  new_user = User(username, email, password)
  # new_user = User(data['username'], data['email'], data['password'])

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
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')
  token = login(username, password)
  # token = login(data['username'], data['password'])
  if not token:
      return jsonify(error='bad username/password given'), 401
  return jsonify(access_token=token), 200

@app.route('/mypokemon', methods=['POST'])
@jwt_required(fresh=True)
def saveMyPokemon():
  data = request.get_json()
  user = User.query.filter_by(username=get_jwt_identity()).first()
  
  if user and pokemon:
    new_userPokemon = UserPokemon(user.user_id, data.get('pokemon_id'), data['name'])
    return jsonify(message=f'{new_userPokemon.name} captured with id: {new_userPokemon.pokemon_id}'), 201
  else:
    return jsonify(error=f'{new_userPokemon.pokemon_id} is not a valid pokemon id'), 400

@app.route('/mypokemon', methods=['GET'])
@jwt_required()
def listMyPokemons():
  # get the user object of the authenticated user
  user = User.query.filter_by(username=get_jwt_identity()).first()
  # pokemons = UserPokemon.query.filter_by(user_id=user.user_id).all()
  pokemons = UserPokemon.query.filter_by(user_id=get_jwt_identity()).all()
  p_json = []
  if pokemons:
    for p in pokemons:
      p_json.append(p.get_json())
    # p_json = [ UserPokemon.get_json() for p in pokemons ]
    return jsonify(p_json), 200
  else:
    return jsonify(error=f'User has not captured any pokemons'), 401

@app.route('/mypokemon/<int:id>', methods=['GET'])
@jwt_required()
def getMyPokemon():
  user_pokemon = UserPokemon.query.filter_by(username=get_jwt_identity(), pokemon_id=id).first()
  if user_pokemon:
    return jsonify(user_pokemon.get_json()), 200
  return jsonify(error=f"id {id} invalid or does not belong to {get_jwt_identity()}"), 401
  # must check if todo belongs to the authenticated user
  # if not todo or todo.user.username != get_jwt_identity():
  # return jsonify(todo.get_json()), 200

@app.route('/mypokemon/<int:id>', methods=['PUT'])
@jwt_required()
def updateMyPokemon():
  data = request.get_json()
  user = User.query.filter_by(username=get_jwt_identity()).first()
  user_pokemon = UserPokemon.query.filter_by(pokemon_id=pokemon_id, user_id=user.user_id).first()
  if user and user_pokemon:
    if user_pokemon.user_id == user.user_id:
      user_pokemon.name = data.get('name')
      db.session.add(user_pokemon)
      db.session.commit()
    return jsonify(message=f'{user_pokemon.name}'), 200
  else:
    return jsonify(error=f'id {id} invalid or does not belong to {user.username}'), 401
  # must check if todo belongs to the authenticated user
  # if not todo or todo.user.username != get_jwt_identity():
  #   return jsonify(error="Bad ID or unauthorized"), 401

  # user.update_todo(id, data['text'])
  # return jsonify(message=f"todo updated to '{data['text']}'!"), 200

@app.route('/mypokemon/<int:id>', methods=['DELETE'])
@jwt_required()
def deleteMyPokemon():
  data = request.get_json()
  name = data['name']
  user = User.query.filter_by(username=get_jwt_identity()).first()
  user_pokemon = UserPokemon.query.filter_by(pokemon_id=pokemon_id, user_id=user.user_id).first()
  if user and user_pokemon:
    if user_pokemon.user_id == user.user_id:
      user_pokemon.name = name
      db.session.delete(user_pokemon)
      db.session.commit()
    return jsonify(message=f'{name} released'), 200
  else:
    return jsonify(error=f'id {id} invalid or does not belong to {user.username}'), 401
  # if user_pokemon:
  #   # must check if todo belongs to the authenticated user
  # if not todo or todo.user.username != get_jwt_identity():
  #   return jsonify(error="Bad ID or unauthorized"), 401

  # user.delete_todo(id)
  # return jsonify(message="todo deleted!"), 200

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)