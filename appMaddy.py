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


@app.route("/rack/ouvrir", methods=["GET"])
def ouvert():
    return app.send_static_file('rackouvert.html')


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
    
    # Vérifier si un nom a été fourni
    if name:
        # Créer un nouvel objet User et l'ajouter à la base de données
        conn = get_db_connection()
        users = conn.execute(f"""
            INSERT INTO User (nom, prenom, classe, date)
            VALUES
                ('{name}', 'Gilles', 'Grande', '2024-12-17 09:45:16');
            """)  # Ajouter l'objet User à la session
        conn.commit()  # Sauvegarder les changements dans la base de données
        
        message = f"Utilisateur '{name}' ajouté avec succès!"
    else:
        message = "Nom non fourni."
    
    # Rendre la page avec un message
    return render_template('formulaire.html', message=message)



# ---------------------------------------------------- Formulaire ----------------------------------------------------




# Lancement du serveur Flask
if __name__ == "__main__":
    app.run(debug=True)
