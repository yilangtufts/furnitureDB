from os import name
import psycopg2

# PostgreSQL connection details
host = 'my_postgres_db'  # Replace with the actual host of your PostgreSQL container
port = 5432  # Replace with the port of your PostgreSQL container
database = 'mydatabase'
user = 'myuser'
password = 'mypassword'


def execute(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password)
        # create a cursor
        cur = conn.cursor()    
	    # execute a statement
        cur.execute(query)
        # fetch the column names
        header = [desc[0] for desc in cur.description]
        # fetch all the records // rows
        table = cur.fetchall()
	    # close the communication with the PostgreSQL
        cur.close()
        return(header, table)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password)
        # create a cursor
        cur = conn.cursor()    
	    # execute a statement
        cur.execute(query)
        conn.commit()
        cur.close()
        return
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update(query):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password)
        # create a cursor
        cur = conn.cursor()    
	    # execute a statement
        cur.execute(query)
        conn.commit()
        cur.close()
        return
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()