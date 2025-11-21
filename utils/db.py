import mysql.connector


def conexion():
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user="root",
            password="",
            port=3306,
            database="db_entrenamiento"
        )
        return conn

    except Exception as e:
        return {"error":str(e)},500
    