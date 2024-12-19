from flask import Flask, render_template, jsonify, request
import sqlite3

app = Flask(__name__)

# Fonction pour obtenir la connexion à la base de données SQLite
def get_db_connection():
    conn = sqlite3.connect('L:/ELEVES-TSTI2D_2/SIN/DOC PROJET/trottiracks.db')  # Chemin vers votre base de données
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux résultats comme des dictionnaires
    return conn

# Route principale pour tester si l'application fonctionne
@app.route("/")
def home():
        return app.send_static_file('index.html')

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
    slots = conn.execute("SELECT * FROM Slots;").fetchall()  # Récupère tous les slots
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
#--------------------------------------------------------SLOT---------------------------------------------------------
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
    classe = request.form.get('classe')
    
    # Vérifier si un nom a été fourni
    if not name:
        message = "Nom non fourni."
    elif not surname:
        message = "Prénom non fourni."
    elif not classe:
        message = "Classe non fournie."
    else:
        # Créer un nouvel objet User et l'ajouter à la base de données
        conn = get_db_connection()
        users = conn.execute(f"""
            INSERT INTO User (nom, prenom, classe, date)
            VALUES
                ('{name}', '{surname}', '{classe}', '2024-12-17 09:45:16');
            """)  # Ajouter l'objet User à la session
        conn.commit()  # Sauvegarder les changements dans la base de données
        
        message = f"Bonjour {name} {surname} votre compte à été ajouté avec succès !"  
    
    # Rendre la page avec un message
    return render_template('formulaire.html', message=message)

# ---------------------------------------------------- Formulaire ----------------------------------------------------

# Lancement du serveur Flask
if __name__ == "__main__":
    app.run(debug=True)
