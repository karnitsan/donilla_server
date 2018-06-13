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
            'name': 'mail', 'description': 'mail of new user',
            'in': 'formData', 'required': True, 'type': 'string'
        },
        {
            'name': 'password', 'description': 'password of new user',
            'in': 'formData', 'required': True, 'type': 'string'
        },
        {
            'name': 'nick_name', 'description': 'nick of new user',
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
            'name': 'mail', 'description': 'mail of queried user',
            'in': 'formData', 'required': True, 'type': 'string'
        },
        {
            'name': 'password', 'description': 'password of queried user',
            'in': 'formData', 'required': True, 'type': 'string'
        }
    ],
    'responses': {
        '200': {'description': 'user details retrieved'}
    }
}

ADD_CAMPAIGN = {
    'tags': ['campaign'],
    'parameters': [
        {
            'name': 'mail', 'description': 'mail of new user',
            'in': 'formData', 'required': True, 'type': 'string'
        },
        {
            'name': 'password', 'description': 'password of new user',
            'in': 'formData', 'required': True, 'type': 'string'
        },
        {
            'name': 'nick_name', 'description': 'nick of new user',
            'in': 'formData', 'required': True, 'type': 'string'
        }
    ],
    'responses': {
        '201': {'description': 'user added'}
    }
}
