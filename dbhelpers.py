import mariadb
import dbcreds

def connect_db():
    try:
        conn=mariadb.connect(
        user=dbcreds.user,
        password=dbcreds.password,
        host=dbcreds.host,
        port=dbcreds.port,
        database=dbcreds.database,
        # there's an option that eliminates the need to do conn.commit()
        autocommit=True
        )
        cursor = conn.cursor()
        return cursor
    except mariadb.OperationalError as e:
        print("OPERATIONAL ERROR:", e)
    except Exception as e:
        print("UNEXPECTED ERROR:", e)
    
def disconnect_db(cursor):
    try:
        conn = cursor.connection
        cursor.close()
        conn.close()
    except mariadb.OperationalError:
        print("OPERATIONAL ERROR: ")
    except mariadb.InternalError as e:
        print("INTERNAL ERROR:", e)
    except Exception:
        print("UNEXPECTED ERROR:", e)

def execute_statement(cursor, statement, args=[]):
    try:
        cursor.execute(statement, args)
        results = cursor.fetchall()
        return results
    except mariadb.ProgrammingError as e:
        if "doesn't have a result set" in str(e):
            return None
        print("Syntax error in your SQL statement:", e)
        return str(e)
    except mariadb.IntegrityError as e:
        print("This statement failed to execute due to integrity error,", e)
        return str(e)
    except mariadb.DataError as e:
        print("DATA ERROR:", e)
        return str(e)
    except Exception as e:
        print("Unexpected error", e)
        return str(e)

def run_statement(statement : str, args=[]):
    """
    This function expects a valid SQL statement and an optional list of arguments. It connect to the DB,
    executes the statement and closes the connection.
    If the connection to the DB fails, it returns None without running the statement.

    Args:
    statement (str): A valid SQL query
    args (list, optional): The list of arguments. Defaults to [].
    """
    cursor = connect_db()
    if (cursor == None):
        print("Failed to connect to the DB, statement will not run")
        return None
    result = execute_statement(cursor, statement, args)
    disconnect_db(cursor)
    return result