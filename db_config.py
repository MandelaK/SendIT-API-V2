import psycopg2

db_url = "dbname='sendit_db' user='postgres' password='postgres' host='localhost' port='5432'"


def connection(db_url):
    try:
        conn = psycopg2.connect(db_url)
    except (Exception, psycopg2.Error) as error:
        return "We could not create a connection to the database", error
    else:
        print("Connection established to database")
        return conn


def init_db():
    conn = connection(db_url)
    return conn


def tables():
    users_table = """CREATE TABLE IF NOT EXISTS users(
        user_id serial PRIMARY KEY,
        first_name varchar (25) NOT NULL,
        last_name varchar (25) NOT NULL,
        email varchar(144) NOT NULL unique,
        password varchar (64) NOT NULL,
        username varchar (32) unique,
        phone integer unique
        )"""

    parcels_table = """
        CREATE TABLE IF NOT EXISTS parcels(
        parcel_id serial PRIMARY KEY,
        parcel_name varchar (25) NOT NULL,
        sender_id integer REFERENCES users (user_id),
        recipient_name varchar (40) NOT NULL,
        pickup_location varchar (40) NOT NULL,
        current_location varchar (40),
        destination varchar (40) NOT NULL,
        weight integer NOT NULL,
        price integer NOT NULL,
        status varchar (15) NOT NULL
        )"""

    queries = [users_table, parcels_table]
    return queries


def create_tables():
    conn = connection(db_url)
    cursor = conn.cursor()
    queries = tables()
    for query in queries:
        cursor.execute(query)
    conn.commit()


def destroy_tables():
    pass
