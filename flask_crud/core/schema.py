from core import ma

class GetUserSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True)
    
class UserSchema(ma.Schema):
    id = ma.Integer()
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True)