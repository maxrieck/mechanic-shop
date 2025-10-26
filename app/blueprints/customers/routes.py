from . import customers_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import Customer, db 
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required
from app.blueprints.service_tickets.schemas import service_tickets_schema


@customers_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = request.json
        email = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting email and password'}), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and customer.password == password: 
        auth_token = encode_token(customer.id)

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else: 
        return jsonify({'message': "Invalid email or password"}), 401


@customers_bp.route("/", methods=['POST'])
@limiter.limit("3 per hour")  #limits user to creating 3 profiles per hour
@cache.cached(timeout=60)
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400
    query = select(Customer).where(Customer.email == customer_data['email'])
    existing_customer = db.session.execute(query). scalars().all()
    if existing_customer:
        return jsonify({"error": "Email already associated with an account"}), 400 
    new_customer = Customer(**customer_data)
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


@customers_bp.route("/", methods=['GET'])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()

    return customers_schema.jsonify(customers)


@customers_bp.route("/<int:customer_id>", methods=['GET'])
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 404


@customers_bp.route("/", methods=['PUT'])
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


@customers_bp.route("/", methods=['DELETE'])
@limiter.limit("10 per day")
@token_required
def delete_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": f'Customer id: {customer_id}, successfully deleted.'}), 200


@customers_bp.route("/<int:customer_id>/service_tickets", methods=['GET'])
@token_required
def get_customer_service_tickets(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

   
    tickets = customer.service_tickets
    
    return service_tickets_schema.jsonify(tickets), 200