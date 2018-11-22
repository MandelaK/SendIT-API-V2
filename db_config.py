import os

import psycopg2
from werkzeug.security import generate_password_hash

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
        password varchar (254) NOT NULL,
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
    drop_users = """DROP TABLE IF EXISTS users CASCADE;"""
    drop_parcels = """DROP TABLE IF EXISTS parcels CASCADE;"""

    queries = [drop_users, drop_parcels]
    for query in queries:
        cursor.execute(query)
    conn.commit()


def create_admin():
    """We will import this method and initialize it after we create our
    tables so that we always have admin in the database."""

    conn = init_db()
    cursor = conn.cursor()

    admin_pass = {"password": generate_password_hash("adminpassword")}
    create_admin = """
    INSERT INTO users (first_name, last_name, email, password, phone, is_admin)
    VALUES ('Admin', 'Major', 'admin@admin.admin', %(password)s, 1111111111, 't')
    """
    cursor.execute(create_admin, admin_pass)
    print("Creating admin")
    conn.commit()


def delete_admin():
    """We delete admin before creating our app so that there can only always be only
    one admin"""

    conn = init_db()
    cursor = conn.cursor()
    delete_ad = """DELETE FROM users WHERE email = 'admin@admin.admin'
    """
    cursor.execute(delete_ad)
    conn.commit()
