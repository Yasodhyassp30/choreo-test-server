from cerberus import Validator

def validate_input(data):
    schema = {
        'data': {
            'type': 'dict',
            'required': True,
            'schema': {
                'turbidity': {'type': 'float', 'required': True},
                'ph': {'type': 'float', 'required': True},
                'conductivity': {'type': 'float', 'required': True},
            }
        }
    }

    v = Validator(schema)
    if not v.validate(data):
        raise Exception(v.errors)
    
def validate_sensor(data):
    schema = {
        'data': {
            'type': 'dict',
            'required': True,
            'schema': {
                'sensor_id': {'type': 'string', 'required': True},
                'ph':{'type': 'float', 'required': True},
                'turbidity': {'type': 'float', 'required': True},
                'conductivity': {'type': 'float', 'required': True},
            }
        }
    }

    v = Validator(schema)
    if not v.validate(data):
        raise Exception(v.errors)