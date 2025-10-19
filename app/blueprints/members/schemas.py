from app.extensions import ma
from app.models import Member 


class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Member

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
