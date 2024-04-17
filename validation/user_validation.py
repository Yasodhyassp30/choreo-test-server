from cerberus import Validator

def validate_user(data):
    schema = {
        'password': {
            'type': 'string',
            'required': True,
        },
        'email': {
            'type': 'string',
            'required': True,
        }
    }

    v = Validator(schema)
    if not v.validate(data):
        raise ValueError(v.errors)

def validate_login(data):
    schema = {
        'email': {
            'type': 'string',
            'required': True,
        },
        'password': {
            'type': 'string',
            'required': True,
        }
    }

    v = Validator(schema)

    if not v.validate(data):
        raise ValueError(v.errors)