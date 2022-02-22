from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, NoneOf, AnyOf
from function_commun import db_connection
import datetime

days = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
        '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

months = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']


# Permet de garder la date à jour
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
last_year = date.strftime("%Y")
last_year = int(last_year) - 5
first_year = last_year - 95
years = [' ']
for i in range(first_year, last_year):
    years.append(str(i))

sexes = [' ', 'Homme', 'Femme', 'Autre']


# Si l'age est inferieur à 4 ans
def int_verification(self, field):  # (form, field)
    message = "Ce n'est pas un âge correct"
    try:
        if int(field.data) < 4:
            raise ValidationError(message)
    except ValueError:
        raise ValidationError(message)


# Détection de chiffres (interdit dans plusieurs cas)
def string_without_numbers_verification(self, field):  # (form, field)
    message = "caractères interdits"
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for s in enumerate(str(field.data)):
        if not s[1].isalnum() or s[1] in numbers:
            raise ValidationError(message)


# Détection de caractères interdits (comme ' ( - :)
def string_verification(self, field):
    message = "caractères interdits"
    for s in enumerate(str(field.data)):
        if not s[1].isalnum():
            raise ValidationError(message)


# Récupere les pseudos (pour éviter les doublons)
def get_list_pseudo():
    list_pseudo = []
    conn = db_connection()
    cursor = conn.execute("SELECT pseudo FROM User")
    for row in cursor.fetchall():
        list_pseudo.append(row[0])
    cursor.close()
    if conn:
        conn.close()
    return list_pseudo


# Récupère les emails (pour éviter les doublons)
def get_list_email():
    list_email = []
    conn = db_connection()
    cursor = conn.execute("SELECT email FROM User")
    for row in cursor.fetchall():
        list_email.append(row[0])
    cursor.close()
    if conn:
        conn.close()
    return list_email


# Form pour s'enregistrer comme nouvel utilisateur
class RegisterForm(FlaskForm):
    first_name = StringField("Prénom: ", validators=[DataRequired(), string_without_numbers_verification])

    last_name = StringField("Nom: ", validators=[DataRequired(), string_without_numbers_verification])

    day_birth = SelectField('Jour', validators=[DataRequired(message="jour incorrect")], choices=days)

    month_birth = SelectField('Mois', validators=[DataRequired(message="mois incorrect")], choices=months)

    year_birth = SelectField('Année', validators=[DataRequired(message="année incorrect")], choices=years)

    sexe = SelectField('Sexe', validators=[DataRequired(message="Veuillez selectionner un sexe")], choices=sexes)

    email = StringField("Email: ", validators=[Email(message="Adresse mail incorrecte"),
                                               DataRequired(), NoneOf(get_list_email(), message="email déjà utilisé")])
    pseudo = StringField("Pseudo: ", validators=[DataRequired(),
                                                 NoneOf(get_list_pseudo(), message="Pseudo déjà utilisé"),
                                                 string_verification])
    password = PasswordField("Mot de passe (plus de 5 caractères): ",
                             validators=[Length(min=6, message="Pas assez de caractères!")])
    confirm = PasswordField("Confirmer mot de passe",
                            validators=[EqualTo('password', message="Mots de passe différents!")])
    submit = SubmitField("Confirmer")


# Form pour se connecter
class LoginForm(FlaskForm):
    pseudo = StringField("Pseudo: ", validators=[DataRequired(),
                                                 AnyOf(get_list_pseudo(),
                                                       message="Pseudo inconnu"), string_verification])
    password = PasswordField("Mot de passe: ", validators=[Length(min=6, message="Pas assez de caractères!")])

    submit = SubmitField("Confirmer")


# Form pour modifier son mot de passe
class ModifyPasswordForm(FlaskForm):
    old_password = PasswordField("Votre mot de passe actuel: ",
                                 validators=[Length(min=6, message="Pas assez de caractères!")])
    new_password = PasswordField("Nouveau mot de passe (plus de 5 caractères): ",
                                 validators=[Length(min=6, message="Pas assez de caractères!")])
    new_password_confirmation = PasswordField("Confirmer nouveau mot de passe: ",
                                              validators=[EqualTo('new_password', message="Mots de passe différents!")])
    submit = SubmitField("Confirmer")


class ModifyInformationsForm(FlaskForm):
    first_name = StringField("Nouveau prénom: ", validators=[string_without_numbers_verification])
    last_name = StringField("Nouveau nom: ", validators=[string_without_numbers_verification])
    sexe = SelectField('Nouveau sexe', choices=sexes)
    submit = SubmitField("Confirmer")


class DeleteAccountForm(FlaskForm):
    submit = SubmitField("Confirmer la suppression du compte")
