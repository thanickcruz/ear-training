import psycopg2

# https://www.postgresqltutorial.com/postgresql-python/connect/#:~:text=To%20connect%20to%20the%20suppliers,instance%20of%20the%20connection%20class.&text=The%20following%20is%20the%20list,that%20you%20want%20to%20connect.

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('---- Successfully connected to PostgreSQL Server ----\n')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)