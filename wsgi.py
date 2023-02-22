import click
import csv
from tabulate import tabulate
from App import db, User, Pokemon, UserPokemon
from App import app

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  with open('pokemon.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
      new_pokemon = Pokemon()
      new_pokemon.id = int(row['pokedex_number'])
      new_pokemon.name = str(row['name'])
      new_pokemon.attack = int(row['attack'])
      new_pokemon.defense = int(row['defense'])
      new_pokemon.hp = int(row['hp'])
      if not row['height_m'] == "":
        new_pokemon.height = int(float(row['height_m']))
      new_pokemon.sp_attack = int(row['sp_attack'])
      new_pokemon.sp_defense = int(row['sp_defense'])
      new_pokemon.speed = int(row['speed'])
      new_pokemon.type1 = str(row['type1'])
      if not row['type2'] == "":
        new_pokemon.type2 = str(row['type2'])
      if not row['weight_kg'] == "":
        new_pokemon.weight = int(float(row['weight_kg']))
      db.session.add(new_pokemon)
    db.session.commit()
  print('database initialized')

  