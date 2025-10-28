from .schemas import service_ticket_schema, service_tickets_schema, edit_ticket_schema, return_ticket_schema
from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from app.models import ServiceTicket, db, Mechanic
from . import service_tickets_bp
from app.extensions import limiter, cache


@service_tickets_bp.route("/", methods=["POST"])
@limiter.limit("5 per hour")
@cache.cached(timeout=60)
def add_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # Check if a ticket with same VIN and date already exists
    existing_ticket = db.session.execute(
        select(ServiceTicket).filter_by(
            VIN=ticket_data["VIN"],
            service_date=ticket_data["service_date"]
        )
    ).scalar_one_or_none()

    if existing_ticket:
        return jsonify({"message": "Service ticket already exists"}), 400

    new_ticket = ServiceTicket(
        VIN=ticket_data["VIN"],
        service_date=ticket_data["service_date"],
        service_desc=ticket_data["service_desc"],
        customer_id=ticket_data["customer_id"]
    )

    db.session.add(new_ticket)
    db.session.commit()

    return (
        jsonify(
            {"Message": "New ticket placed!", "ticket": service_ticket_schema.dump(new_ticket)}
        ),
        201,
    )



@service_tickets_bp.route("/<int:ticket_id>/assign_mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if ticket and mechanic:
        if mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
            db.session.commit()
            return jsonify({"Message": "Successfully assigned mechanic to ticket."}), 200
        else:
            return jsonify({"Message": "Mechanic is already assigned in this ticket."}), 400
    else:
        return jsonify({"Message": "Invalid ticket id or mechanic id."}), 400


# removes specific Mechanic from Service Ticket
@service_tickets_bp.route("/<int:ticket_id>/remove_mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if ticket and mechanic:
        if mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
            db.session.commit()
            return jsonify({"Message": "Successfully removed mechanic from ticket."}), 200
        else:
            return jsonify({"Message": "Mechanic isn't assigned to this ticket."}), 400
    else:
        return jsonify({"Message": "Invalid ticket id or mechanic id."}), 400

# view All Service Tickets
@service_tickets_bp.route("/", methods=["GET"])
def get_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(tickets), 200

# view Specific Service Ticket
@service_tickets_bp.route("/<int:id>", methods=["GET"])
def get_ticket(id):
    ticket = db.session.get(ServiceTicket, id)

    if ticket is None:
        return jsonify({"Error": "Ticket not found"}), 404

    return service_ticket_schema.jsonify(ticket), 200

# add or remove multiple mechanics for ticket
@service_tickets_bp.route("/<int:ticket_id>", methods=['PUT'])
def edit_service_ticket(ticket_id):
    try:
        ticket_edits = edit_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(ServiceTicket).where(ServiceTicket.id == ticket_id)
    ticket = db.session.execute(query).scalars().first()

    for mechanic_id in ticket_edits['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in ticket.mechanics:
                ticket.mechanics.append(mechanic)
    
    for mechanic_id in ticket_edits['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in ticket.mechanics:
                ticket.mechanics.remove(mechanic)
    
    db.session.commit()
    return return_ticket_schema.jsonify(ticket)

