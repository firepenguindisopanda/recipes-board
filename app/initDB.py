from models import db, Recipe, Ingredient
from flask import Flask
import json
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///.Database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    return app

app = create_app()
app.app_context().push()
db.create_all(app=app)

f = open('raw_data.json')

data = json.load(f)

for x in data.values():
    ingreList = ""
    for y in x['ingredients']:
        ingreList += (y + ",")
    newRecipe = Recipe(name=x['title'], ingredients_list=ingreList, instructions=x['instructions'])
    db.session.add(newRecipe)
db.session.commit()
    