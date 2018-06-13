'Donilla database handling.'
import contextlib
import logging
import sqlite3

LOGGER = logging.getLogger('donilla.db')
DB_NAME = 'donilla.db'


class UnknownUser(Exception):
    'Unknown user mail.'


class DuplicateUser(Exception):
    'Duplicate user mail.'

class WrongUserPassword(Exception):
    'Wornd user password.'


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
            CREATE TABLE campaigns(
                id VARCHAR(32) UNIQUE,
                name VARCHAR(256),
                amota VARCHAR(256),
                status INTEGER,
                target INTEGER,
                start_date VARCHAR(32),
                end_date VARCHAR(32),
                clearing_info VARCHAR(256),
                link_home_page VARCHAR(256),
                link_logo VARCHAR(256),
                link_text VARCHAR(256),
                link_video VARCHAR(256),
                link_pic1 VARCHAR(256),
                link_pic2 VARCHAR(256)
                )''')
        LOGGER.debug('campign table created')

        sql.execute('''
            CREATE TABLE users(
                mail VARCHAR(256) UNIQUE,
                password VARCHAR(256),
                first_name VARCHAR(32),
                last_name VARCHAR(32),
                nick_name VARCHAR(32),
                gender INTEGER,
                address VARCHAR(256),
                id_number VARCHAR(32),
                age_verifyed BOOLEAN,
                mail_verifyed BOOLEAN,
                status INTEGER
                )''')
        LOGGER.debug('user table created')
        
        sql.execute('''
            CREATE TABLE donations(
                id VARCHAR(32) UNIQUE,
                campaign_id VARCHAR(32),
                mail VARCHAR(256),
                amount INTEGER,
                totel INTEGER,
                date VARCHAR(32),
                time VARCHAR(32),
                voucher_info VARCHAR(256),
                approval_info VARCHAR(256)
                )''')
        LOGGER.debug('donate table created')
          
        sql.execute('''
            CREATE TABLE lottery_game(
                id VARCHAR(32) UNIQUE,
                status INTEGER,                
                cycle INTEGER,
                winner_index INTEGER,
                date VARCHAR(32),
                time VARCHAR(32)
                )''')
        LOGGER.debug('lottery_game table created')
        
        sql.execute('''
            CREATE TABLE lottery_ticket(
                id VARCHAR(32) UNIQUE,
                mail VARCHAR(256),
                lottery_game_id VARCHAR(32),
                price INTEGER,
                luck_number INTEGER,
                ticket_index INTEGER,
                total INTEGER,
                date VARCHAR(32),
                time VARCHAR(32)
                )''')
        LOGGER.debug('lottery_ticket table created')

        sql.execute('''
            CREATE TABLE spinner_game(
                id VARCHAR(32) UNIQUE,
                status INTEGER,
                cycle INTEGER,
                date VARCHAR(32),
                time VARCHAR(32)
                )''')
        LOGGER.debug('spinner_game table created')
                
        sql.execute('''
            CREATE TABLE spinner_ticket(
                id VARCHAR(32) UNIQUE,
                mail VARCHAR(256),
                spinner_game_id VARCHAR(32),
                price INTEGER,
                ticket_index INTEGER,
                spinner_slot INTEGER,
                total INTEGER,
                date VARCHAR(32),
                time VARCHAR(32)
                )''')
        LOGGER.debug('spinner_ticket table created')
         

def get_user(user_mail, user_password):
    'Get details of a user.'
    with sql_connection() as sql:
        sql.execute("SELECT * FROM users WHERE mail = ?", (user_mail,))
        try:
            user_details = sql.fetchall()[0]
        except IndexError:
            raise UnknownUser("user {} does not exist".format(user_mail))
        
        p = user_details["password"]
        if p != user_password:
            raise WrongUserPassword("user {} Wrong user password".format(user_mail))
        return {key: user_details[key] for key in user_details.keys()}


def add_user(user_mail, user_password, user_nick_name):
    'Add a user to the database. '
    with sql_connection() as sql:
        try:
            sql.execute("INSERT INTO users (mail, password, nick_name) VALUES (?, ?, ?)", (user_mail, user_password, user_nick_name))
        except sqlite3.IntegrityError as exception:
            bad_column_name = str(exception).split('.')[-1]
            bad_value = locals().get(bad_column_name)
            raise DuplicateUser("{} {} is non unique".format(bad_column_name, bad_value))
    return get_user(user_mail, user_password)

#init_db()
