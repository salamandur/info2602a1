from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class UserPokemon(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), unique = True, nullable = False)
  pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.pokemon_id'), unique = True, nullable = False)
  name = db.Column(db.String(50), nullable = False)
  pass

  def get_json():
    return {"id": self.id, "pokemon_id": self.pokemon_id, "name": self.name}


class User(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique = True, nullable = False)
  email = db.Column(db.String(120), unique = True, nullable = False)
  password = db.Column(db.String(120), unique = True, nullable = False)
  # pokemons = db.relationship('UserPokemon', backref='pokemon', lazy=True, cascade='all, delete-orphan')
  pass

  def __catch_pokemon__(pokemon_id, name):
    return

  def __release_pokemon__(pokemon_id, name):
    return

  def __rename_pokemon__(pokemon_id, name):
    return

  def __set_password__(password):
    self.password = generate_password_hash(password)

  def __check_password__(password):
    if(generate_password_hash(self.password)==generate_password_hash(password)):
      return True
    return False

    
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
  # users = db.relationship('UserPokemon', backref='user', lazy=True, cascade='all, delete-orphan')
  pass

  def get_json(self):
    return {"pokemon_id": self.pokemon_id, "name": self.name, "attack": self.attack, "defense": self.defense, "hp": self.hp, 
            "height": self.height, "sp_attack": self.sp_attack, "sp_defense": self.sp_defense,
            "speed": self.speed, "type1": self.type1, "type2": self.type2}
    # return db.session.execute(db.select(Pokemon))

