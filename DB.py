import sqlite3
import pandas as pd
import joblib
import pickle
from joblib import Parallel, delayed


def create_table():
    conn = sqlite3.connect("test.db")
    print("Opened database successfully")
    conn.execute(
        """CREATE TABLE PATIENTS(
            USERNAME        TEXT      NOT NULL UNIQUE,
            PASSWORD        TEXT      NOT NULL,
            EMAIL           CHAR(50)  NOT NULL PRIMARY KEY,
            CONTRACT ADDRESS TEXT)
            ;"""
    )
    print("Table created successfully")
    conn.close()


def insert_record(username, email, password):
    conn = sqlite3.connect("test.db")
    print("Opened database successfully")
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO PATIENTS (USERNAME , PASSWORD, EMAIL) VALUES ('{0}', '{1}', '{2}');""".format(
            username, password, email
        )
    )
    conn.commit()
    print("Record Inserted Successfully !!!")
    conn.close()


def table_drop():
    conn = sqlite3.connect("test.db")
    print("Opened database successfully")
    conn.execute("DROP TABLE PATIENTS;")
    print("Table Dropped Successfully !!!")
    conn.commit()
    conn.close()


def select():
    conn = sqlite3.connect("test.db")
    print("Opened database successfully")
    cursor = conn.cursor()
    sql = "SELECT * FROM PATIENTS"
    print(sql)
    cursor.execute(sql)
    print(cursor.fetchall())
    conn.commit()
    conn.close()


def predict_anomalies(query, username, password, cursor):
    vectorizer = pickle.load(open("./static/SQLI_Attack/vectorizer.pickle", "rb"))
    naive_bayes = joblib.load("./static/SQLI_Attack/naive_bayes_model.pkl")
    query_df = pd.DataFrame(dict(Sentence=query), index=[0])
    query_arr = vectorizer.transform(query_df.values.ravel()).toarray()
    predict = naive_bayes.predict(query_arr)

    # try:
    #     int(str(username))
    # except ValueError:
    #     return []

    sql = "SELECT * FROM PATIENTS WHERE USERNAME = ?".format(username)
    print(sql)
    cursor.execute(sql, [username])
    data = cursor.fetchall()
    return data


def authenticate_user(username, password):
    print("username = ", username, "password = ", password)
    conn = sqlite3.connect("test.db")
    print("Opened database successfully")
    cursor = conn.cursor()
    sql = "SELECT * FROM PATIENTS WHERE USERNAME = " + str(username) + ";"
    return predict_anomalies(sql, username, password, cursor)
    print(sql)
    data = []
    for query in sql.split(";"):
        if query != " ":
            cursor.execute(query)
            data.append(cursor.fetchall())
    conn.commit()
    conn.close()
    print(data)
    return data[0]


if __name__ == "__main__":
    # create_table()
    # insert_record("Pruthiev", "aspruthiev@gmail.com", "Asp@2001")
    # print("Result", authenticate_user(str("'' OR 1=1--"), "Asp@2001"))
    # table_drop()
    # create_table()
    print(authenticate_user("Pruthiev", "Asp@2001"))
    pass

    # "'' OR 1=1-- ",
    # DROP TABLE
