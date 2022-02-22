# Script regroupant les fonctions / classes utilisées dans plusieurs scripts

import sqlite3
from flask_login import UserMixin
from werkzeug.security import check_password_hash


# Classe pour savoir quel utilisateur est actuellement connecté
class User(UserMixin):
    """
    def set_password(self):
        self.password_hash = generate_password_hash(self.password_hash) """

    # Pour vérifier le mot de passe
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, id, email, password, first_name, pseudo):
         self.id = id
         self.email = email
         self.password_hash = password
         self.first_name = first_name

         self.pseudo = pseudo


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("Base.sqlite", timeout=20)
        conn.execute("PRAGMA foreign_keys = ON")  # Car à "OFF" de base
    except ValueError:
        print("Erreur connexion")

    return conn


def db_disconnect(conn):
    if conn:
        conn.close()


# Fonction pour vérifier si la date de naissance est cohérente
def correct_birth(day_birth, month_birth, year_birth):
    day_birth = int(day_birth)
    month_birth = int(month_birth)
    year_birth = int(year_birth)

    bissextile = False
    if year_birth % 4 == 0:
        if year_birth % 100 == 0:
            if year_birth % 400 == 0:
                bissextile = True
        else:
            bissextile = True

    if (day_birth > 30 and (month_birth == 4 or month_birth == 6 or month_birth == 9 or month_birth == 11))\
            or (day_birth > 29 and month_birth == 2) or (day_birth == 29 and month_birth == 2 and not bissextile):
        return False
    return True


# Fonction pour pouvoir afficher la date de naissance correctement
def adapt_int(number):
    number = int(number)
    if -10 < number < 10:
        number = "0" + str(number)
    else:
        number = str(number)
    return number
