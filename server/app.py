#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    result = Animal.query.filter(Animal.id == id).first()
    
    if not result:
        return '<h1> There were no results </h1>'
    
    output = f'<ul>ID: {result.id}</ul><ul>Name: {result.name}</ul><ul>Species: {result.species}</ul><ul>Zookeeper: {result.zookeeper.name}</ul><ul>Enclosure: {result.enclosure.environment}</ul>'
    
    response = make_response(output, 200)
    return response



@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    keeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    body = f'<ul>ID: {keeper.id}</ul><ul>Name: {keeper.name}</ul><ul>Birthday: {keeper.birthday}</ul>'
    animals = [animal for animal in keeper.animals]

    if not animals:
        body += f'<ul>Has no animals</ul>'
    else:
        for animal in animals:
            body += f'<ul>Animal: {animal.name}</ul>'

    response = make_response(body, 200)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):

    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    response_body = f'<ul>ID: {enclosure.id}</ul><ul>Environment: {enclosure.environment}</ul><ul>Open to Visitors: {enclosure.open_to_visitors}</ul>'

    animals = [animal for animal in enclosure.animals]

    if not animals:
        response_body += f'<ul>sorry no animals</ul>'
    else:
        for animal in animals:
            response_body += f'<ul>Animals: {animal.name}</ul>'

    response = make_response(response_body, 200)

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
