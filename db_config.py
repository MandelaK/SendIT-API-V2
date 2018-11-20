import os

import psycopg2

from instance.config import app_config

env = os.getenv('FLASK_ENV')
db_url = app_config[env].DATABASE_URL


def connection(db_url):
    conn = psycopg2.connect(db_url)
    return conn


def init_db():
    conn = connection(db_url)
    return conn


def tables():
    users_table = """CREATE TABLE IF NOT EXISTS users(
        user_id serial PRIMARY KEY,
        first_name varchar (25) NOT NULL,
        last_name varchar (25) NOT NULL,
        email varchar(50) NOT NULL unique,
        password varchar (64) NOT NULL,
        phone bigint unique,
        is_admin boolean DEFAULT 'f'
        )"""

    parcels_table = """
        CREATE TABLE IF NOT EXISTS parcels(
        parcel_id serial PRIMARY KEY,
        parcel_name varchar (25) NOT NULL,
        sender_email varchar (50) REFERENCES users (email),
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
    conn = init_db()
    cursor = conn.cursor()
    queries = tables()
    for query in queries:
        cursor.execute(query)
        print("Creating tables")
    conn.commit()


def destroy_tables():
    conn = init_db()
    cursor = conn.cursor()
    drop_users = """DROP TABLE IF EXISTS users CASCADE"""
    drop_parcels = """DROP TABLE IF EXISTS parcels CASCADE"""

    queries = [drop_users, drop_parcels]
    for query in queries:
        cursor.execute(query)
    conn.commit()
