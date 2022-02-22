# Projet-HTML5

TITRE DU PROJET: Farandole de jeux

DESCRIPTION DU PROJET:site web permettant de s’enregistrer et de se connecter (les mots de passes sont hachés),
de jouer à des jeux (avec musique, bruitage, et avec un tableau des scores pour les 5 meilleurs joueurs)
et d’accéder à un chat. Le high score personnel de chaque utilisateur est enregistré dans une base de donnée.

MEMBRES DE L'ÉQUIPE ET RÔLES:
- Arthur Cochennec (CSS + tout le back-end de l’application web)
- Corentin Dumortier-Piraud (CSS + développement des jeux)

TECHNOLOGIES UTILISÉES:
-  Environnement de développement intégré: Pycharm (Python).
-  Framework: Flask.
-  Base de données: SQLite.
-  Hachage des mots de passe: Bibliothèque « werkzeug. security » (notamment les fonctions « generate_password_hash »
   et « check_password_hash ».
-  Chat en temps réel: Bibliothèque «Socket.IO»
-  Pour gérer les sessions, les formulaires d’enregistrement/connexion: Bibliothèque «  Flask-Login».

DÉMONSTRATION DE L'APPLICATION: le powerpoint "Présentation.pptx" situé dans le dossier "Présentation"
fournit des explicatitions, des images et des vidéos (contenues dans le dossier "Vidéos") qui présentent cette application.


BUGS CONNUS (Les bugs et problèmes spécifiques à certaines pages seront décrits dans le powerpoint):

- Le CSS n’est pas optimisé. Beaucoup de pages nécessiteraient d’être retravaillées à ce niveau-là.
- Si un utilisateur supprime son compte, un nouvel utilisateur pour réutiliser son pseudo.
  Ce qui peut provoquer des problèmes vis-à-vis du chat ou du tableau des scores.
- Ce site est optimisé pour un écran de taille 1920 * 1080. L’utiliser sur un autre type de résolution
  pourrait perturber la mise en page.
- Des noms de variables ou autres sont francisés, ce qui est assez moche.


POUR LANCER LE PROJET:
Executer le fichier "app.py" présent dans le dossier "Farandole_de_jeux" (projet Web) et aller sur cette adresse: http://127.0.0.1:5000/


POUR VIDER LA BASE DE DONNÉES
Supprimer "Base.sqlite" puis lancer "db.py".


La base contient actuellement 3 personnes (pseudos: 'Arthur', 'Jules' et 'Marion') avec pour mot de passe: 'aaaaaa'


