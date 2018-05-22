'Donilla Web server.'
import functools
import logging
import os

import flasgger
import flask
import flask_limiter.util

import api_spec
import db

STATIC_DIRS = ['static']
DEBUG = bool(os.environ.get('DONILLA_DEBUG', True))

LOGGER = logging.getLogger('donilla.web')
APP = flask.Flask('donilla')
APP.config['SECRET_KEY'] = os.environ.get('DONILLA_SESSIONS_KEY', os.urandom(24))
DEFAULT_LIMIT = '100 per minute'
LIMITER = flask_limiter.Limiter(APP, key_func=flask_limiter.util.get_remote_address, default_limits=[DEFAULT_LIMIT])
APP.config['SWAGGER'] = api_spec.CONFIG
BLUEPRINT = flask.Blueprint('api', __name__)
flasgger.Swagger(APP)


class MissingFields(Exception):
    'Request if missing required fields.'


@APP.errorhandler(429)
def ratelimit_handler(error):
    'Custom error for rate limiter.'
    msg = 'Rate limit exceeded for {}. Allowed rate: {}'.format(flask.request.url, error.description)
    LOGGER.info(msg)
    return flask.make_response(flask.jsonify({'code': 429, 'error': msg}), 429)


def check_missing_fields(fields, required_fields):
    """Raise exception if there are missing fields."""
    if required_fields is None:
        required_fields = set()
    missing_fields = set(required_fields) - set(fields)
    if missing_fields:
        raise MissingFields("Request does not contain field(s): {}".format(', '.join(missing_fields)))


def optional_arg_decorator(decorator):
    """A decorator for decorators than can accept optional arguments."""
    @functools.wraps(decorator)
    def wrapped_decorator(*args, **kwargs):
        """A wrapper to return a filled up function in case arguments are given."""
        if len(args) == 1 and not kwargs and callable(args[0]):
            return decorator(args[0])
        return lambda decoratee: decorator(decoratee, *args, **kwargs)
    return wrapped_decorator


# Since this is a decorator the handler argument will never be None, it is
# defined as such only to comply with python's syntactic sugar.
@optional_arg_decorator
def call(handler=None, required_fields=None):
    """
    A decorator to handle all API calls: extracts arguments, validates them,
    fixes them, handles authentication, and then passes them to the handler,
    dealing with exceptions and returning a valid response.
    """
    @functools.wraps(handler)
    def _call(*_, **__):
        # pylint: disable=broad-except
        # If anything fails, we want to catch it here.
        response = {'status': 500, 'error': 'Internal server error'}
        kwargs = dict(flask.request.view_args, **flask.request.values.to_dict())
        try:
            check_missing_fields(kwargs.keys(), required_fields)
            response = handler(**kwargs)
        except MissingFields as exception:
            response = {'status': 400, 'error': str(exception)}
        except db.UnknownUser as exception:
            response = {'status': 403, 'error': str(exception)}
        except Exception as exception:
            LOGGER.exception("Unknown server exception: %s (%s)", flask.request.url, kwargs)
            if DEBUG:
                response['debug'] = str(exception)
        # pylint: enable=broad-except
        if 'error' in response:
            LOGGER.error(response['error'])
        return flask.make_response(flask.jsonify(response), response.get('status', 200))
    return _call


@BLUEPRINT.route("/add_user", methods=['POST'])
@flasgger.swag_from(api_spec.ADD_USER)
@call(['user_id', 'full_name'])
def add_user_handler(user_id, full_name):
    """
    Add a user.
    """
    return {'status': 200, 'user_details': db.add_user(user_id, full_name)}


@BLUEPRINT.route("/get_user/<user_id>", methods=['POST', 'GET'])
@flasgger.swag_from(api_spec.GET_USER)
@call(['user_id'])
def get_user_handler(user_id):
    """
    Get user details.
    """
    return {'status': 200, 'user_details': db.get_user(user_id)}


@APP.route('/')
@APP.route('/<path:path>', methods=['GET', 'POST'])
# pylint: disable=unused-variable
def catch_all_handler(path='index.html'):
    """All undefined endpoints try to serve from the static directories."""
    for directory in STATIC_DIRS:
        if os.path.isfile(os.path.join(directory, path)):
            return flask.send_from_directory(directory, path)
    return flask.jsonify({'status': 403, 'error': "Forbidden path: {}".format(path)}), 403


APP.register_blueprint(BLUEPRINT)
