import os
import argparse
import sqlite3
import uuid
import datetime
import time
import jaydebeapi
import shutil

from utils.tools import file_not_valid

parser = argparse.ArgumentParser(description='Match counter video features')
parser.add_argument("--database", "-db", type=str, required=True, help="vifeco sqlite database from v2")

args = vars(parser.parse_args())
db_sqlite = args['database']


def connect_sqlite(file):
    return sqlite3.connect(file)


def connect_h2db():
    cur_dir = os.path.dirname(__file__)
    h2_jar_path = os.path.abspath(os.path.join(cur_dir, "db", "h2-1.4.200.jar"))
    db_str = "jdbc:h2:{}".format(os.path.abspath(os.path.join(cur_dir, "target", "vifeco")))

    if file_not_valid(h2_jar_path):
        print("You must provide h2 jar to continue.")
        exit(1)

    return jaydebeapi.connect("org.h2.Driver", db_str, ["", ""], h2_jar_path)


def clear_target(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM POINT")
    cursor.execute("DELETE FROM VIDEO")
    cursor.execute("DELETE FROM COLLECTION_CATEGORY")
    cursor.execute("DELETE FROM COLLECTION")
    cursor.execute("DELETE FROM CATEGORY")
    cursor.execute("DELETE FROM USER")


def create_target_db():
    cur_dir = os.path.dirname(__file__)
    target_dir = os.path.join(cur_dir, "target")
    template_file = os.path.abspath(os.path.join(cur_dir, "db", "vifeco.mv.db"))
    template_copy = os.path.abspath(os.path.join(target_dir, "vifeco.mv.db"))
    shutil.copyfile(template_file, template_copy)


def read_user(cursor):
    query = "SELECT * FROM user"

    result = cursor.execute(query)
    for row in result.fetchall():
        yield row


def insert_user(cursor, data):
    data = (data[0], data[1], data[2], data[4])

    query = "INSERT INTO user (ID, FIRSTNAME, LASTNAME, ISDEFAULT) VALUES (?,?,?,?)"
    cursor.execute(query, data)


def read_category(cursor):
    query = "SELECT * FROM category"

    result = cursor.execute(query)
    for row in result.fetchall():
        yield row


def insert_category(cursor, data):
    query = "INSERT INTO category (ID, NAME, ICON, COLOR, SHORTCUT) VALUES (?,?,?,?,?)"
    cursor.execute(query, data)


def read_collection(cursor):
    query = "SELECT * FROM collection"

    result = cursor.execute(query)
    for row in result.fetchall():
        yield row


def insert_collection(cursor, data):
    query = "INSERT INTO collection (ID, NAME, ISDEFAULT) VALUES (?,?,?)"
    cursor.execute(query, data)


def read_category_collection(cursor):
    query = "SELECT * FROM category_collection"

    result = cursor.execute(query)
    for row in result.fetchall():
        yield row


def insert_category_collection(cursor, data):
    query = "INSERT INTO collection_category (COLLECTION_ID, CATEGORY_ID) VALUES (?,?)"
    cursor.execute(query, data)


def read_video(cursor):
    query = "SELECT * FROM video"

    result = cursor.execute(query)
    for row in result.fetchall():
        yield row


def insert_video(cursor, data):
    result = (data[0], uuid.uuid4().hex)
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    data = (result[1], data[1], data[2], data[3], data[4], timestamp)
    query = "INSERT INTO video (ID, PATH, DURATION, USER_ID, COLLECTION_ID, CREATEDAT) VALUES (?,?,?,?,?,?)"
    cursor.execute(query, data)

    return result


def read_point(cursor):
    query = "SELECT * FROM point"

    result = cursor.execute(query)
    for row in result.fetchall():
        yield row


def insert_point(cursor, data):
    query = "INSERT INTO POINT (ID, X, Y, CATEGORY_ID, VIDEO_ID, START) VALUES (?,?,?,?,?,?)"
    cursor.execute(query, data)


def count_point(cursor, identifier):
    query = "SELECT count(id), category_id from point where " \
            "video_id={} group by category_id".format(identifier)
    return cursor.execute(query).fetchone()


if __name__ == '__main__':
    if file_not_valid(db_sqlite):
        print("One of the files path is not valid")
        exit(1)

    # Create target db file
    create_target_db()

    # Clear tables
    conn_h2db = connect_h2db()
    clear_target(conn_h2db)

    conn_sqlite = connect_sqlite(db_sqlite)
    for row in read_user(conn_sqlite):
        insert_user(conn_h2db.cursor(), row)

    for row in read_category(conn_sqlite):
        insert_category(conn_h2db.cursor(), row)

    for row in read_collection(conn_sqlite):
        insert_collection(conn_h2db.cursor(), row)

    for row in read_category_collection(conn_sqlite):
        insert_category_collection(conn_h2db.cursor(), row)

    video_ids = []

    for row in read_video(conn_sqlite):
        video_ids.append(insert_video(conn_h2db.cursor(), row))

    for row in read_point(conn_sqlite):
        video_id = next(filter(lambda x: x[0] == row[3], video_ids))
        data = (uuid.uuid4().hex, row[1], row[2], row[4], video_id[1], row[5])
        insert_point(conn_h2db.cursor(), data)


    # Validation
    for ids in video_ids:
        print(ids[0])
        original = count_point(conn_sqlite.cursor(), ids[0])
        print(original)
        # migrate = count_point(conn_h2db.cursor(), ids[1])
