from core import ma

class GetUserSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True)
    
class UserSchema(ma.Schema):
    id = ma.Integer(dump_only=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True)
    
class FileSchema(ma.Schema):
    id = ma.Int(dump_only=True)
    filename = ma.Str(required=True)
    url = ma.Str(required=True)
    uploaded_at = ma.DateTime(dump_only=True)