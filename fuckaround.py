#!/usr/bin/env python

# Cool ass web site made by
# a cool dude for another
# cool dude :D
# I like turtle 🐢🐢🐢

# Ben va etre mad, g pa mi de commentaires x_x

from flask import Flask, jsonify, request, render_template
import json

app = Flask(__name__)

def load_items_from_json():
    with open('items.json', 'r') as file:
        items = json.load(file)
    return items

def save_items_to_json(items):
    with open('items.json', 'w') as file:
        json.dump(items, file, indent=2)
        
def is_item_exist(items, name):
    return any(item['name'] == name for item in items)

@app.route('/')
def index():
    items = load_items_from_json()
    return render_template('index.html', items=items)

@app.route('/items', methods=['GET'])
def get_items():
    items = load_items_from_json()
    return jsonify(items)

@app.route('/items/<string:name>', methods=['GET'])
def get_item_by_name(name: int):
    item = get_item(name)
    if item is None:
        return jsonify({ 'error': 'Item does not exist'}), 404
    return jsonify(item)

def get_item(name):
    items = load_items_from_json()
    return next((e for e in items if e['name'] == name), None)

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()

    new_item = {
        'name': data.get('name'),
        'Quantity': data.get('Quantity')
    }

    items = load_items_from_json()

    if not new_item['name']:
        return jsonify({'error': 'Item name is required'}), 400

    if is_item_exist(items, new_item['name']):
        return jsonify({'error': 'Item already exists'}), 400

    items.append(new_item)
    save_items_to_json(items)

    return jsonify({'message': 'Item added successfully'})

if __name__ == '__main__':
    app.run(debug=True)
