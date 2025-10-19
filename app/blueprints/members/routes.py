from .schemas import member_schema, members_schema
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import Member, db 
from . import members_bp


@members_bp.route("/", methods=['POST'])
def create_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400
    query = select(Member).where(Member.email == member_data['email'])
    existing_member = db.session.execute(query). scalars().all()
    if existing_member:
        return jsonify({"error": "Email alrady associated with an account"}), 400 
    new_member = Member(**member_data)
    db.session.add(new_member)
    db.session.commit()
    return member_schema.jsonify(new_member), 201


@members_bp.route("/", methods=['GET'])
def get_members():
    query = select(Member)
    members = db.session.execute(query).scalars().all()

    return members_schema.jsonify(members)


@members_bp.route("/<int:member_id>", methods=['GET'])
def get_member(member_id):
    member = db.session.get(Member, member_id)

    if member:
        return member_schema.jsonify(member), 200
    return jsonify({"error": "Member not found."}), 404


@members_bp.route("/<int:member_id>", methods=['PUT'])
def update_member(member_id):
    member = db.session.get(Member, member_id)

    if not member:
        return jsonify({"error": "Member not found."}), 404
    
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in member_data.items():
        setattr(member, key, value)

    db.session.commit()
    return member_schema.jsonify(member), 200


@members_bp.route("/<int:member_id>", methods=['DELETE'])
def delete_member(member_id):
    member = db.session.get(Member, member_id)

    if not member:
        return jsonify({"error": "Member not found."}), 404
    
    db.session.delete(member)
    db.session.commit()
    return jsonify({"message": f'Member id: {member_id}, successfully deleted.'}), 200