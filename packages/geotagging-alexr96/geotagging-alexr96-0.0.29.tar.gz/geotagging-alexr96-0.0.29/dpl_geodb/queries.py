import psycopg2
import typing
from dpl_geodb.geo_ops import config


def thumb_querie(id:int) -> typing.Union[tuple, str]:
    # TODO operate off of uuids
    connection = None
    db_parameters = config()
    connection = psycopg2.connect(**db_parameters)
    try:
        cursor = connection.cursor()
        select_command = f"SELECT * FROM picturereference WHERE id={int(id)};"
        cursor.execute(select_command)
        pic_ref = cursor.fetchone()
    except Exception as e:
        return e
    finally:
        if connection is not None:
            connection.close()
    return pic_ref
        
    

