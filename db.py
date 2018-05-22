'Donilla database handling.'
import contextlib
import logging
import sqlite3

LOGGER = logging.getLogger('donilla.db')
DB_NAME = 'donilla.db'


class UnknownUser(Exception):
    'Unknown user ID.'


class DuplicateUser(Exception):
    'Duplicate user ID.'


@contextlib.contextmanager
def sql_connection(db_name=None):
    'Context manager for querying the database.'
    try:
        connection = sqlite3.connect(db_name or DB_NAME)
        connection.row_factory = sqlite3.Row
        yield connection.cursor()
        connection.commit()
    except sqlite3.Error as db_exception:
        raise db_exception
    finally:
        if 'connection' in locals():
            connection.close()


def init_db():
    'Initialize the database.'
    with sql_connection() as sql:
        # Not using IF EXISTS here in case we want different handling.
        sql.execute('SELECT name FROM sqlite_master WHERE type = "table" AND name = "users"')
        if len(sql.fetchall()) == 1:
            LOGGER.debug('database already exists')
            return
        sql.execute('''
            CREATE TABLE users(
                user_id VARCHAR(32) UNIQUE,
                full_name VARCHAR(256),
                kwargs VARCHAR(1024))''')
        LOGGER.debug('user table created')


def get_user(user_id):
    'Get details of a user.'
    with sql_connection() as sql:
        sql.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        try:
            user_details = sql.fetchall()[0]
        except IndexError:
            raise UnknownUser("user {} does not exist".format(user_id))
        return {key: user_details[key] for key in user_details.keys()}


def add_user(user_id, full_name):
    'Add a user to the database.'
    with sql_connection() as sql:
        try:
            sql.execute("INSERT INTO users (user_id, full_name) VALUES (?, ?)", (user_id, full_name))
        except sqlite3.IntegrityError as exception:
            bad_column_name = str(exception).split('.')[-1]
            bad_value = locals().get(bad_column_name)
            raise DuplicateUser("{} {} is non unique".format(bad_column_name, bad_value))
    return get_user(user_id)
