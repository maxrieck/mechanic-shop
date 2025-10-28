from app.extensions import ma
from app.models import ServiceTicket
from marshmallow import fields
from app.blueprints.mechanics.schemas import MechanicSchema

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    mechanics = fields.Nested(MechanicSchema, many=True)
    class Meta: 
        model = ServiceTicket
        include_fk = True

class EditTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_ticket_schema = ServiceTicketSchema()
edit_ticket_schema = EditTicketSchema()