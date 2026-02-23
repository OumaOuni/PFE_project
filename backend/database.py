
import psycopg2

def get_connection():
    return psycopg2.connect(
    host="localhost",
    dbname="luxury_home_decor_bi",
    user="postgres",
    password="Oouunnii123$"
)
    