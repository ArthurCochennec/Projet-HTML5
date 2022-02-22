# Script pour créer les différentes tables SQLite

import sqlite3
from function_commun import db_connection

conn = sqlite3.connect("Base.sqlite")
cursor = conn.cursor()

# Table regroupant tous les utilisateurs
sql_query = """ CREATE TABLE User (
    id integer PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    sexe text NOT NULL,
    date_birth text NOT NULL,
    email text NOT NULL UNIQUE,
    pseudo text NOT NULL UNIQUE,
    password text NOT NULL
)"""
cursor.execute(sql_query)

# Table regroupant les messages de la conversation
sql_query = """ CREATE TABLE History (
    pseudo text NOT NULL,
    message text NOT NULL
)"""
cursor.execute(sql_query)

# Table regroupant les records de tous les utilisateurs
sql_query = """ CREATE TABLE Data (
    record_dodge integer NOT NULL,
    trackuser integer NOT NULL UNIQUE,
    FOREIGN KEY (trackuser) REFERENCES User (id) ON DELETE CASCADE
)"""
cursor.execute(sql_query)

# Table regroupant les records du jeu "Dodge"
sql_query = """ CREATE TABLE Record_Dodge (
    record_dodge integer NOT NULL,
    user_pseudo text NOT NULL,
    position integer NOT NULL
)"""
cursor.execute(sql_query)

# On injecte 5 entrées lambdas dans la table Record_Dodge
with db_connection() as conn:
    cursor = conn.cursor()
    sql = """INSERT INTO Record_Dodge (record_dodge, user_pseudo, position)
        VALUES (?, ?, ?)"""
    cursor.execute(sql, (10, "Bot1", 1,))
    cursor.execute(sql, (9, "Bot2", 2,))
    cursor.execute(sql, (8, "Bot3", 3,))
    cursor.execute(sql, (7, "Bot4", 4,))
    cursor.execute(sql, (6, "Bot5", 5,))
    cursor.close()
    conn.commit()
