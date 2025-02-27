from flask import Flask, render_template, jsonify, request, redirect, make_response
import sqlite3
import os

app = Flask(__name__)




def get_db_connection():
    # Specify the file path
    file_path = "trottiracks.db"

    # Check if the file exists
    if os.path.exists(file_path):
        print("The file exists.")
        con = sqlite3.connect("trottiracks.db")
        con.row_factory = sqlite3.Row
        return con
    else:
        print("The file does not exist.")   
        con = sqlite3.connect("trottiracks.db")
        con.row_factory = sqlite3.Row
        # Créer les tables
        con.execute("""CREATE TABLE "User" (
            "id_user"	INTEGER,
            "nom"	TEXT NOT NULL,
            "prenom"	TEXT NOT NULL,
            "username"	TEXT NOT NULL UNIQUE,
            "classe"	TEXT NOT NULL,
            "date"	INTEGER DEFAULT current_timestamp,
            "motdepasse"	TEXT NOT NULL,
            PRIMARY KEY("id_user" AUTOINCREMENT)
        );""")

        return con 


@app.route("/", methods=["GET"])
def home():
    nom = None
    if 'username' in request.cookies:
        nom = request.cookies['username']
    return render_template('accueil.html', nom=nom)
    # return app.send_static_file('index.html')  # Simplement afficher le fichier index.html



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html', message=None)  # Aucun message d'erreur par défaut
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        
        # Requête sécurisée pour éviter les injections SQL
        user = conn.execute("SELECT * FROM User WHERE username = ?", (username,)).fetchone()

        if user:
            # Vérifie si le mot de passe correspond
            if user["motdepasse"] == password:
                # Crée une réponse pour rediriger vers la page d'accueil
                response = make_response(redirect('/'))
                # Ajoute un cookie (par exemple, stocker le nom d'utilisateur)
                response.set_cookie('username', username, max_age=3600)  # Expire après 1 heure
                return response
            else:
                # Mauvais mot de passe
                return render_template('login.html', message="Mot de passe ou nom d'utilisateur incorrect.")
        else:
            # Utilisateur non trouvé
            return render_template('login.html', message="Mot de passe ou nom d'utilisateur incorrect.")

@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(render_template('login.html', message="Déconnecté avec succès."))
    response.set_cookie('username', '', max_age=0)  # Supprime le cookie
    return response

# Route pour afficher les utilisateurs dans une page HTML
@app.route("/utilisateurs", methods=["GET"])
def get_users():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM User;').fetchall()  # Récupère tous les utilisateurs de la table 'users'
    conn.close()

    # Convertit les résultats en une liste de dictionnaires
    users_list = [dict(user) for user in users]

    # Passe les utilisateurs au template HTML
    return render_template('utilisateurs.html', users=users_list)

# Route API pour renvoyer les utilisateurs en JSON
@app.route("/utilisateurs/api", methods=["GET"])
def get_users_api():
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM User;').fetchall()  # Récupère tous les utilisateurs de la table 'users'
    conn.close()

    # Convertit les résultats en une liste de dictionnaires
    users_list = [dict(user) for user in users]
    return jsonify(users_list)  # Retourne les utilisateurs en JSON

# Route pour supprimer un utilisateur
@app.route('/utilisateurs/supprimer/<int:id_user>', methods=['POST'])
def supprimer_utilisateur(id_user):
    conn = get_db_connection()
    conn.execute('DELETE FROM User WHERE id_user = ?', (id_user,))
    conn.commit()
    conn.close()
    return jsonify({'message': f"Utilisateur avec l'ID {id_user} supprimé avec succès."}), 200

# Route pour supprimer un utilisateur par son ID
@app.route('/utilisateurs/supprimer/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Supprimer l'utilisateur de la base de données
    cursor.execute("DELETE FROM User WHERE id_user = ?", (id,))
    conn.commit()
    conn.close()

    # Retourner une réponse JSON indiquant le succès
    return jsonify({"message": "Utilisateur supprimé avec succès."}), 200

@app.route("/rack/ouvrir", methods=["GET"])
def ouvert():
    return app.send_static_file('rackouvert.html')
#--------------------------------------------------------SLOT---------------------------------------------------------
# Route pour afficher les slots dans une page HTML
@app.route("/slots", methods=["GET"])
def get_slots():
    conn = get_db_connection()
    slots = conn.execute("SELECT * FROM slots;").fetchall()  # Récupère tous les slots
    conn.close()

    # Convertit les résultats en une liste de dictionnaires
    slots_list = [dict(slot) for slot in slots]

    # Passe les slots au template HTML
    return render_template("slots.html", slots=slots_list)

# Route API pour renvoyer les slots en JSON
@app.route("/slots/api", methods=["GET"])
def get_slots_api():
    conn = get_db_connection()
    slots = conn.execute("SELECT * FROM Slots;").fetchall()
    conn.close()

    # Convertit les résultats en une liste de dictionnaires
    slots_list = [dict(slot) for slot in slots]
    return jsonify(slots_list)  # Retourne les slots en JSON

# Route pour mettre à jour l'état d'un slot (libre ou non)
@app.route("/slots/update/<int:id>", methods=["POST"])
def update_slot(id):
    # Récupère la nouvelle valeur pour "libre" depuis la requête POST
    libre = request.form.get("libre")

    conn = get_db_connection()
    conn.execute("UPDATE Slots SET libre = ? WHERE id_slot = ?", (libre, id))
    conn.commit()
    conn.close()

    return jsonify({"message": "État du slot mis à jour avec succès."}), 200

# ---------------------------------------------------- Formulaire ----------------------------------------------------

# Route pour afficher le formulaire HTML
@app.route('/formulaire')
def form():
    return render_template('formulaire.html')

# Route pour traiter le formulaire en POST
@app.route('/submit', methods=['POST'])
def submit():
    # Récupérer les données envoyées par le formulaire
    name = request.form.get('name')
    surname = request.form.get('surname')
    username = request.form.get('username')
    classe = request.form.get('classe')
    motdepasse = request.form.get('motdepasse')
    confirmationmotdepasse = request.form.get('cmotdepasse')
    # Vérifier si un nom a été fourni
    if not name:
        message = "Nom non fourni."
    elif not surname:
        message = "Prénom non fourni."
    elif not username:
        message = "Nom d'utilisateur non fourni."
    elif not classe:
        message = "Classe non fourni."
    elif not motdepasse:
        message = "Mot de passe non fourni."
    elif not confirmationmotdepasse:
        message = "Mot de passe non fourni."
    # Vérifie si le mot de passe correspond
    elif motdepasse != confirmationmotdepasse:
        message = "Les mots de passe ne correspondent pas."
    else:
        # Créer un nouvel objet User et l'ajouter à la base de données
        try:            
            conn = get_db_connection()
            users = conn.execute(f"""
                INSERT INTO User (nom, prenom, username, classe, motdepasse)
                VALUES
                    ('{name}', '{surname}','{username}', '{classe}', '{motdepasse}');
                """)  # Ajouter l'objet User à la session
            conn.commit()  # Sauvegarder les changements dans la base de données
        except sqlite3.IntegrityError:
            print("couldn't add twice")    
            return render_template('formulaire.html', message="Le nom d'utilisateur existe déjà")
            
        message = f"Bonjour {surname} votre compte à été ajouté avec succès !"  
    
    # Rendre la page avec un message
    return render_template('formulaire.html', message=message)

# ---------------------------------------------------- Formulaire ----------------------------------------------------


# Lancement du serveur Flask
if __name__ == "__main__":
    app.run(debug=True)






