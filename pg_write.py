"""Write to Postgres."""
import time
import string
import random
import sqlalchemy as sqla

con = sqla.create_engine("postgresql://postgres:postgres@0.0.0.0:5432/postgres")

fake_names = [
    "Ben Dover",
    "Sal Monella",
    "Anna Lytics",
    "Tess Tickle",
    "Hugh Jass",
    "Marge Arita",
    "Bobby Pin",
    "Arthur Itis",
    "Faye Daway",
    "Tara Misu",
    "King Kong",
    "Ram Ghosh",
    "Donatella Nobatti"
]

def random_string():
    return random.choice(fake_names)

def random_number():
    return random.randint(1, 100)

create_table = """
CREATE TABLE IF NOT EXISTS
    test (
    user_id serial PRIMARY KEY,
    name VARCHAR(50),
    value integer);
    """
con.execute(create_table)

while True:
    name = random_string()
    number = random_number()
    insert_table = f"""
    INSERT INTO test (name, value)
    VALUES('{name}', {number});"""
    con.execute(insert_table)
    print(insert_table)
    time.sleep(3)
