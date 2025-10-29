from .schemas import inventories_schema, inventory_schema
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import Inventory, db 
from . import inventory_bp
from app.extensions import limiter, cache


@inventory_bp.route("/", methods=['POST'])
@limiter.limit("10 per hour")
def create_item():
    try:
        item_data = inventory_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400
    query = select(Inventory).where(Inventory.name == item_data['name'])
    existing_inventory = db.session.execute(query). scalars().all()
    if existing_inventory:
        return jsonify({"error": "Item already exists"}), 400 
    new_item = Inventory(**item_data)
    db.session.add(new_item)
    db.session.commit()
    return inventory_schema.jsonify(new_item), 201


@inventory_bp.route("/", methods=['GET'])
@cache.cached(timeout=60)
def get_inventory():
    query = select(Inventory)
    items = db.session.execute(query).scalars().all()

    return inventories_schema.jsonify(items)


@inventory_bp.route("/<int:inventory_id>", methods=['GET'])
def get_item(inventory_id):
    item = db.session.get(Inventory, inventory_id)

    if item:
        return inventory_schema.jsonify(item), 200
    return jsonify({"error": "Item not found."}), 404


@inventory_bp.route("/<int:inventory_id>", methods=['PUT'])
def edit_item(inventory_id):
    item = db.session.get(Inventory, inventory_id)

    if not item:
        return jsonify({"error": "Item not found."}), 404
    
    try:
        item_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in item_data.items():
        setattr(item, key, value)

    db.session.commit()
    return inventory_schema.jsonify(item), 200


@inventory_bp.route("/<int:inventory_id>", methods=['DELETE'])
@limiter.limit("10 per day")
def delete_item(inventory_id):
    item = db.session.get(Inventory, inventory_id)

    if not item:
        return jsonify({"error": "Item not found."}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f'Item id: {inventory_id}, successfully deleted.'}), 200
