from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class UserPokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
  pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.pokemon_id'), nullable = False)
  name = db.Column(db.String(50), nullable = False)
  pass

  def __init__(self, user_id, pokemon_id, name):
    self.user_id = user_id
    self.pokemon_id = pokemon_id
    self.name = name

  def get_json(self):
    pokemon = Pokemon.query.filter_by(pokemon_id=self.pokemon_id).first()
    if pokemon:
      return {"id": self.pokemon_id, "name": self.name, "species": pokemon.name}
    else:
      return {"id": self.pokemon_id, "name": self.name, "species": null}

class User(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique = True, nullable = False)
  email = db.Column(db.String(120), unique = True, nullable = False)
  password = db.Column(db.String(120), unique = True, nullable = False)
  pass

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.set_password(password)

  def catch_pokemon(pokemon_id, name):
    user_pokemon = Pokemon.query.filter_by(pokemon_id=pokemon_id).first()
    return

  def release_pokemon(pokemon_id, name):
    user_pokemon = UserPokemon.query.filter_by(pokemon_id=pokemon_id).first()
    return

  def rename_pokemon(pokemon_id, name):
    user_pokemon = UserPokemon.query.filter_by(pokemon_id=pokemon_id).first()
    if user_pokemon:
      user_pokemon.name = name
    return

  def set_password(self, password):
    self.password = generate_password_hash(password, method='sha256')

  def check_password(self, password):
    return check_password_hash(self.password, password)
    
class Pokemon(db.Model):
  pokemon_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(30), nullable = False)
  attack = db.Column(db.Integer, nullable = False)
  defense = db.Column(db.Integer, nullable = False)
  hp = db.Column(db.Integer, nullable = False)
  height = db.Column(db.Integer, nullable = True)
  sp_attack = db.Column(db.Integer, nullable = False)
  sp_defense = db.Column(db.Integer, nullable = False)
  speed = db.Column(db.Integer, nullable = False)
  type1 = db.Column(db.String(50), nullable = False)
  type2 = db.Column(db.String(50), nullable = False, default = "None")
  weight = db.Column(db.Integer, nullable = True)
  pass

  def get_json(self):
    return {"pokemon_id": self.pokemon_id, "name": self.name, "attack": self.attack, "defense": self.defense, "hp": self.hp, 
            "height": self.height, "sp_attack": self.sp_attack, "sp_defense": self.sp_defense,
            "speed": self.speed, "type1": self.type1, "type2": self.type2, "weight": self.weight}