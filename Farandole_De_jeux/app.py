# Script pour lancer le site en local

from importlib import reload
import forms
from flask import Flask, request, render_template, jsonify, url_for, redirect, flash
from flask_socketio import SocketIO, send
from function_commun import db_connection, db_disconnect, User, correct_birth, adapt_int
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdf4s5df4sdgs84f8zf7892464535130044nv4hb4vdxlo4ldrd5f4eer45cffd4trs4df5ds'
socketio = SocketIO(app, cors_allowed_origins='*')

login_manager = LoginManager(app)
login_manager.login_view = 'preface'  # sert à rediriger les pages
login_manager.login_message = "Erreur, Vous avez beson de vous connecter pour accéder à cette page"


# Pour récuperer les informations de l'utilisateur connecté
@login_manager.user_loader
def load_user(user_id):
    with db_connection() as conn:
        curs = conn.cursor()
        curs.execute("SELECT id, email, password, first_name, pseudo from User where id = (?)", [user_id])
        lu = curs.fetchone()

    if lu is None:
        curs.close()
        db_disconnect(conn)
        return None

    else:
        u = User(int(lu[0]), lu[1], lu[2], lu[3], lu[4])
        curs.close()
        db_disconnect(conn)
        return u


"""@app.after_request
def after_request(response):
    app.template_folder = 'templates'
    return response """


@app.route('/', methods=["GET"])
def index():
    return redirect(url_for('preface'))


@app.route('/preface', methods=["GET"])
def preface():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    return render_template('preface.html')


# Page pour jouer au jeu "Dodge"
@app.route('/Dodge', methods=['GET', 'POST'])
@login_required
def dodge():
    if request.method == "GET":  # Récupère son score et lance le jeu

        with db_connection() as conn:
            cursor = conn.cursor()
            sql = """SELECT record_dodge FROM Data where trackuser = ?"""
            cursor.execute(sql, (current_user.id,))
            cu = cursor.fetchone()

        informations = dict(HighScore=cu[0])
        return render_template('Dodge.html', **informations)

    else:  # Récupère le High-score de la session en cours et actualise (si nécessaire) celui de la base de données

        with db_connection() as conn:  # Récupère le High-score actuel
            cursor = conn.cursor()
            sql = """SELECT record_dodge FROM Data where trackuser = ?"""
            cursor.execute(sql, (current_user.id,))
            cu = cursor.fetchone()
            record_user = cu[0]

        with db_connection() as conn:  # Récupère le pseudo
            cursor = conn.cursor()
            sql = """SELECT pseudo FROM User where id = ?"""
            cursor.execute(sql, (current_user.id,))
            cu = cursor.fetchone()
            pseudo_user = cu[0]

        if int(request.form['record']) > record_user:  # Si le record de la session > record enregistré
            with db_connection() as conn:
                cursor = conn.cursor()
                sql = """UPDATE Data SET record_dodge = ? WHERE trackuser = ?"""
                cursor.execute(sql, (request.form['record'], current_user.id,))

            record_user = int(request.form['record'])
            record_temoin = -1
            new_record = False
            position = 0

            with db_connection() as conn:
                cursor = conn.execute("SELECT * FROM Record_Dodge")
                for row in cursor.fetchall():
                    if record_user > row[0] > record_temoin:  # si le record est dans le top 5
                        new_record = True
                        record_temoin = row[0]
                        position = row[2]

            if new_record:  # Mets à jour le High-score
                with db_connection() as conn:
                    cursor = conn.cursor()
                    sql = """ DELETE FROM Record_Dodge WHERE position = ? """
                    cursor.execute(sql, (5,))

                    sql = """UPDATE Record_Dodge SET position = position + 1  WHERE position >= ?"""
                    cursor.execute(sql, (position,))

                    sql = """INSERT INTO Record_Dodge (record_dodge, user_pseudo, position) VALUES (?, ?, ?)"""
                    cursor.execute(sql, (record_user, pseudo_user, position))

        return redirect(url_for('main_page'))


# Page pour jouer au jeu "Memory"
@app.route('/Memory')
@login_required
def memory():
    return render_template('Memory.html')


"""
@app.route('/score_dodge', methods=['POST'])
@login_required
def score_dodge():
    record = request.form['record']
    return redirect(url_for('main_page'))
"""


# Page pour s'enregistrer
@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    reload(forms)  # Pour actualiser la liste de pseudos et d'adresses mails
    form = forms.RegisterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            new_first_name = request.form["first_name"]
            new_last_name = request.form["last_name"]
            new_day_birth = request.form["day_birth"]
            new_month_birth = request.form["month_birth"]
            new_year_birth = request.form["year_birth"]
            new_date_birth = adapt_int(new_day_birth) + '/' + adapt_int(new_month_birth) + '/' + str(new_year_birth)

            if not correct_birth(new_day_birth, new_month_birth, new_year_birth):
                flash("Date de naissance incorrecte", category='wrong_date')
                return render_template('register.html', form=form)

            new_sexe = request.form["sexe"]
            new_email = request.form["email"]
            new_pseudo = request.form["pseudo"]
            new_password = generate_password_hash(request.form["password"])

            with db_connection() as conn:  # Enregistre le nouvel utilisateur
                cursor = conn.cursor()
                sql = """INSERT INTO User (first_name, last_name, sexe, date_birth, email, pseudo, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?)"""
                cursor.execute(sql, (new_first_name, new_last_name, new_sexe,
                                     new_date_birth, new_email, new_pseudo, new_password))
                cursor.close()
                conn.commit()

            with db_connection() as conn:
                cursor = conn.execute("SELECT id, email, password,"
                                      "first_name FROM User where pseudo = ?", (form.pseudo.data,))
                cu = cursor.fetchone()
            if type(cu) == tuple:
                us = load_user(list(cu)[0])
                cursor.close()
                if us.check_password(form.password.data):  # Enregistre cet utilsateur comme l'utilisateur actuel
                    login_user(us)

            with db_connection() as conn:
                cursor = conn.cursor()
                sql = """INSERT INTO Data (record_dodge, trackuser)
                    VALUES (?, ?)"""
                cursor.execute(sql, (0, current_user.id))
                cursor.close()
                conn.commit()

            flash("Inscription réussie")
            return redirect(url_for('main_page'))

    return render_template('register.html', form=form)


# Page pour se connecter
@app.route('/login/', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))

    reload(forms)
    form = forms.LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            with db_connection() as conn:
                cursor = conn.execute("SELECT id, email, password, first_name,"
                                      "pseudo FROM User where pseudo = ?", (form.pseudo.data,))
                cu = cursor.fetchone()

            if type(cu) == tuple:
                us = load_user(list(cu)[0])
                cursor.close()

                if us.check_password(form.password.data):
                    login_user(us)
                    flash("Connexion réussie")
                    return redirect(url_for('main_page'))

                flash("Mot de passe incorrect", category='wrong_password')
                return render_template('login.html', form=form)

            return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.route('/main_page', methods=["GET", "POST"])
@login_required
def main_page():

    with db_connection() as conn:  # Affiche les 5 meilleurs records du jeu "Dodge"
        cursor = conn.execute("SELECT * FROM Record_Dodge")

        infor = cursor.fetchall()
        records_dodge = []
        records_dodge_list = []

        for row in infor:
            records_dodge.append(row[2])
            records_dodge_list.append(str(row[1]) + ": " + str(row[0]))

        informations = dict(r1=records_dodge_list[records_dodge.index(1)],
                            r2=records_dodge_list[records_dodge.index(2)],
                            r3=records_dodge_list[records_dodge.index(3)],
                            r4=records_dodge_list[records_dodge.index(4)],
                            r5=records_dodge_list[records_dodge.index(5)])

    return render_template('main_page.html', **informations)


# Page pour afficher les utilisateurs (n'est pas censé être accessible par les utilisateurs)
@app.route("/users", methods=["GET", "POST", "DELETE"])
def users():
    if request.method == "GET":
        with db_connection() as conn:
            cursor = conn.execute("SELECT * FROM User")
            users = [dict(id=row[0], first_name=row[1], last_name=row[2], sexe=row[3],
                          date_birth=row[4], email=row[5], pseudo=row[6], password=row[7]) for row in cursor.fetchall()]
        cursor.close()
        if users is not None:
            return jsonify(users)
        else:
            return "Aucun utilisateur!"

    if request.method == "DELETE":
        id = request.form["id"]
        sql = """ DELETE FROM User WHERE id = ? """
        with db_connection() as conn:
            conn.execute(sql, (id,))
            conn.commit()

        return f"The User with id:{id} has been deleted.", 200


# Page pour afficher les records des utilisateurs (n'est pas censé être accessible par les utilisateurs)
@app.route("/datas", methods=["GET", "POST"])
def datas():
    if request.method == "GET":
        with db_connection() as conn:
            cursor = conn.execute("SELECT * FROM Data")
            datas = [
                dict(record=row[0], id=row[1])
                for row in cursor.fetchall()
            ]
        cursor.close()
        if datas is not None:
            return jsonify(datas)
        else:
            return "Aucune donnée!"


@app.route("/record_dodge", methods=["GET", "POST"])
def records():
    if request.method == "GET":
        with db_connection() as conn:
            cursor = conn.execute("SELECT * FROM Record_Dodge")
            datas = [
                dict(record=row[0], pseudo=row[1], pos=row[2])
                for row in cursor.fetchall()
            ]
        cursor.close()
        if datas is not None:
            return jsonify(datas)
        else:
            return "Aucune donnée!"


@app.route('/addata', methods=["GET", "POST"])
def addata():
    if request.method == "POST":
        with db_connection() as conn:
            cursor = conn.cursor()
            new_record = request.form["record"]
            new_trackuser = request.form["trackuser"]

            sql = """INSERT INTO Data (record, trackuser)
                    VALUES (?, ?)"""
            cursor.execute(sql, (new_record, new_trackuser))
            conn.commit()
            cursor.close()

        return "Bien joué"

    else:
        return "Bonjour"


# Page pour se déconnecter
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté")
    return redirect(url_for('preface'))


@app.route('/myaccount')
@login_required
def myaccount():
    with db_connection() as conn:
        cursor = conn.cursor()
        sql = """SELECT * FROM User where id = ?"""
        cursor.execute(sql, (current_user.id,))

        for row in cursor.fetchall():
            id, first_name, last_name, sexe, date_birth, email, pseudo\
                = row[0], row[1], row[2], row[3], row[4], row[5], row[6]

        sql = """SELECT * FROM Data where trackuser = ?"""
        cursor.execute(sql, (current_user.id,))
        for row in cursor.fetchall():
            record = row[0]
        cursor.close()

    informations = dict(Prénom=first_name, Nom=last_name, Date_de_naissance=date_birth,
                        Sexe=sexe, Email=email, Pseudo=pseudo, Record=record)
    return render_template('myaccount.html', **informations)


@app.route('/modify_password', methods=["GET", "POST"])
@login_required
def modify_password():
    reload(forms)
    form = forms.ModifyPasswordForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if check_password_hash(current_user.password_hash, form.old_password.data):
                new_password = generate_password_hash(form.new_password.data)
                with db_connection() as conn:
                    cursor = conn.cursor()
                    sql = """UPDATE User SET password = ? WHERE password = ?"""
                    cursor.execute(sql, (new_password, current_user.password_hash))
                    flash("Mot de passe modifié avec succès")
                return redirect(url_for('main_page'))

            flash("Mot de passe incorrect", category='wrong_password')
            return render_template('modify_password.html', form=form)
        return render_template('modify_password.html', form=form)
    return render_template('modify_password.html', form=form)


@app.route('/modify_informations', methods=["GET", "POST"])
@login_required
def modify_informations():
    reload(forms)
    form = forms.ModifyInformationsForm()

    if request.method == "POST":

        if form.validate_on_submit():
            new_first_name = request.form["first_name"]
            if new_first_name != '':
                with db_connection() as conn:
                    sql = """UPDATE User SET first_name = ? WHERE id = ? """
                    conn.cursor().execute(sql, (new_first_name, current_user.id))

            new_last_name = request.form["last_name"]
            if new_last_name != '':
                with db_connection() as conn:
                    sql = """UPDATE User SET last_name = ? WHERE id = ? """
                    conn.cursor().execute(sql, (new_last_name, current_user.id))

            new_sexe = request.form["sexe"]
            if new_sexe != ' ':
                with db_connection() as conn:
                    sql = """UPDATE User SET sexe = ? WHERE id = ? """
                    conn.cursor().execute(sql, (new_sexe, current_user.id))

            flash("Informations modifiées avec succès")
            return redirect(url_for('myaccount'))
        return render_template('modify_informations.html', form=form)
        # return render_template('modify_informations.html', form=form)

    elif request.method == "GET":
        with db_connection() as conn:
            cursor = conn.cursor()
            sql = """SELECT first_name, last_name, sexe from User WHERE id = ?"""
            cursor.execute(sql, (current_user.id,))
            for row in cursor.fetchall():
                first_name, last_name, sexe = row[0], row[1], row[2]

        informations = dict(Prénom=first_name, Nom=last_name, Sexe=sexe)
        return render_template('modify_informations.html', **informations, form=form)


@app.route('/delete_account', methods=["GET", "POST"])
@login_required
def delete_account():
    reload(forms)
    form = forms.DeleteAccountForm()
    if request.method == "POST":
        if form.validate_on_submit():
            with db_connection() as conn:
                cursor = conn.cursor()
                sql = """DELETE FROM User where id = ?"""
                cursor.execute(sql, (current_user.id,))

            flash("Compte supprimé avec succès")
            return render_template('preface.html')

    return render_template('delete_account.html', form=form)


@app.route('/chat', methods=["GET", "POST"])
@login_required
def chat():
    with db_connection() as conn:
        cursor = conn.cursor()
        sql = """Select * FROM History"""
        cursor.execute(sql)
        informations = dict(messages=cursor.fetchall()[-200:], pseudo=current_user.pseudo + ":")

    return render_template('chat.html', **informations)


@socketio.on('message')
def handlemessage(msg):

    new_msg = [current_user.pseudo + ":", " " + msg]
    send(new_msg, broadcast=True)

    with db_connection() as conn:
        cursor = conn.cursor()

        # sql = """Delete from History"""
        # cursor.execute(sql)

        sql = """INSERT INTO History (pseudo, message) VALUES (?, ?)"""
        cursor.execute(sql, (new_msg[0], new_msg[1]))


if __name__ == "__main__":
    socketio.run(app, debug=True, use_reloader=False)
