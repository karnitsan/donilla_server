'API definitions for flasgger.'

CONFIG = {
    'title': 'Donilla API',
    'uiversion': 2,
    'specs_route': '/',
    'specs': [{
        'endpoint': '/',
        'route': '/apispec.json',
    }],
    'info': {
        'title': 'The Donilla Web Server API',
        'version': 1,
        'contact': {
            'name': 'Donilla Balagan',
            'email': 'help@donilla.com',
            'url': 'https://api.donilla.com',
        },
        'license': {
            'name': 'GNU GPL 3.0',
            'url': 'http://www.gnu.org/licenses/'
        },
        'description': '''
Shmulik's per project.
        '''
    }
}

ADD_USER = {
    'tags': ['user'],
    'parameters': [
        {
            'name': 'user_id', 'description': 'id of new user',
            'in': 'formData', 'required': True, 'type': 'string'
        },
        {
            'name': 'full_name', 'description': 'full name of new user',
            'in': 'formData', 'required': True, 'type': 'string'
        }
    ],
    'responses': {
        '201': {'description': 'user added'}
    }
}

GET_USER = {
    'tags': ['user'],
    'parameters': [
        {
            'name': 'user_id', 'description': 'id of queried user',
            'in': 'path', 'required': True, 'type': 'string'
        }
    ],
    'responses': {
        '200': {'description': 'user details retrieved'}
    }
}
