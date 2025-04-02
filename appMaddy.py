from flask import Flask, render_template, jsonify, request, redirect, make_response
import sqlite3
import os
import requests

app = Flask(__name__)

# Database connection function
def get_db_connection():
    file_path = "trottiracks.db"
    if os.path.exists(file_path):
        print("The file exists.")
        con = sqlite3.connect(file_path)
        con.row_factory = sqlite3.Row
        return con
    else:
        print("The file does not exist.")
        con = sqlite3.connect(file_path)
        con.row_factory = sqlite3.Row
        # Create tables
        con.execute("""
            CREATE TABLE "User" (
                "id_user" INTEGER PRIMARY KEY AUTOINCREMENT,
                "nom" TEXT NOT NULL,
                "prenom" TEXT NOT NULL,
                "username" TEXT NOT NULL UNIQUE,
                "classe" TEXT NOT NULL,
                "date" INTEGER DEFAULT current_timestamp,
                "motdepasse" TEXT NOT NULL
            );
        """)
        return con

# Function to create admin account if it doesn't exist
def create_admin_account():
    conn = get_db_connection()
    admin_exists = conn.execute("SELECT * FROM User WHERE username = 'admin'").fetchone()
    if not admin_exists:
        conn.execute("""
            INSERT INTO User (nom, prenom, username, classe, motdepasse)-
            VALUES ('Admin', 'Admin', 'admin', 'Admin', 'admin');
        """)
        conn.commit()
    conn.close()

# Call the function to create admin account
create_admin_account()

# Home route
@app.route("/", methods=["GET"])
def home():
    nom = request.cookies.get('username')
    logged_in = nom is not None
    return render_template('accueil.html', nom=nom, logged_in=logged_in)

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html', message=None)
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM User WHERE username = ?", (username,)).fetchone()
        if user and user["motdepasse"] == password:
            response = make_response(redirect('/'))
            response.set_cookie('username', username, max_age=3600)
            return response
        else:
            return render_template('login.html', message="Mot de passe ou nom d'utilisateur incorrect.")

# Logout route
@app.route("/logout", methods=["GET"])
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie('username', '', max_age=0)
    return response

# Route to display users in HTML
@app.route("/utilisateurs", methods=["GET"])
def get_users():
    username = request.cookies.get('username')
    if username != 'admin':
        return redirect('/login')
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM User;').fetchall()
    conn.close()
    users_list = [dict(user) for user in users]
    return render_template('utilisateurs.html', users=users_list)

# API route to return users in JSON
@app.route("/utilisateurs/api", methods=["GET"])
def get_users_api():
    username = request.cookies.get('username')
    if username != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM User;').fetchall()
    conn.close()
    users_list = [dict(user) for user in users]
    return jsonify(users_list)

# Route to delete a user
@app.route('/utilisateurs/supprimer/<int:id_user>', methods=['POST'])
def supprimer_utilisateur(id_user):
    conn = get_db_connection()
    conn.execute('DELETE FROM User WHERE id_user = ?', (id_user,))
    conn.commit()
    conn.close()
    return jsonify({'message': f"Utilisateur avec l'ID {id_user} supprimé avec succès."}), 200

# Route to delete a user by ID
@app.route('/utilisateurs/supprimer/<int:id>', methods=['DELETE'])
def delete_user(id):
    username = request.cookies.get('username')
    if username != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403
    conn = get_db_connection()
    conn.execute("DELETE FROM User WHERE id_user = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Utilisateur supprimé avec succès."}), 200

# Route to make a user admin
@app.route('/utilisateurs/make_admin', methods=['POST'])
def make_admin():
    username = request.cookies.get('username')
    if username != 'admin':
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    user_to_make_admin = data.get('username')

    if not user_to_make_admin:
        return jsonify({"error": "Nom d'utilisateur non fourni"}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM User WHERE username = ?", (user_to_make_admin,)).fetchone()
    if user:
        conn.execute("UPDATE User SET classe = 'Admin' WHERE username = ?", (user_to_make_admin,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Utilisateur rendu admin avec succès."}), 200
    else:
        conn.close()
        return jsonify({"error": "Utilisateur non trouvé"}), 404


# Route to open rack
@app.route("/rack/ouvrir/1", methods=["GET"])
def ouvert1():
    r = requests.get('http://169.254.231.1:5000/ouvrir1')
    print(r) 
    return "ouvert"


@app.route("/rack/ouvrir/2", methods=["GET"])
def ouvert2():
    r = requests.get('http://169.254.231.1:5000/ouvrir2')
    print(r) 
    return "ouvert"


@app.route("/rack/ouvrir/3", methods=["GET"])
def ouvert3():
    r = requests.get('http://169.254.231.1:5000/ouvrir3')
    print(r) 
    return "ouvert"

# Route to display slots in HTML
@app.route("/slots", methods=["GET"])
def get_slots():
    username = request.cookies.get('username')
    if not username:
        return redirect('/login')  # Redirect to login if not logged in
    conn = get_db_connection()
    slots = conn.execute("SELECT * FROM slots;").fetchall()
    conn.close()
    slots_list = [dict(slot) for slot in slots]
    return render_template("slots.html", slots=slots_list)

# API route to return slots in JSON
@app.route("/slots/api", methods=["GET"])
def get_slots_api():
    conn = get_db_connection()
    slots = conn.execute("SELECT * FROM Slots;").fetchall()
    conn.close()
    slots_list = [dict(slot) for slot in slots]
    return jsonify(slots_list)

# Route to update slot status
@app.route("/slots/update/<int:id>", methods=["POST"])
def update_slot(id):
    libre = request.form.get("libre")
    conn = get_db_connection()
    conn.execute("UPDATE Slots SET libre = ? WHERE id_slot = ?", (libre, id))
    conn.commit()
    conn.close()
    return jsonify({"message": "État du slot mis à jour avec succès."}), 200

# Route to display form
@app.route('/formulaire')
def form():
    return render_template('formulaire.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    surname = request.form.get('surname')
    username = request.form.get('username')
    classe = request.form.get('classe')
    motdepasse = request.form.get('motdepasse')
    confirmationmotdepasse = request.form.get('cmotdepasse')
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
    elif motdepasse != confirmationmotdepasse:
        message = "Les mots de passe ne correspondent pas."
    else:
        try:
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO User (nom, prenom, username, classe, motdepasse)
                VALUES (?, ?, ?, ?, ?);
            """, (name, surname, username, classe, motdepasse))
            conn.commit()
            message = f"Bonjour {surname} votre compte à été ajouté avec succès !"
        except sqlite3.IntegrityError:
            return render_template('formulaire.html', message="Le nom d'utilisateur existe déjà")
    return render_template('formulaire.html', message=message)

# Route to display user information
@app.route("/user_info", methods=["GET"])
def user_info():
    username = request.cookies.get('username')
    if not username:
        return redirect('/login')

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM User WHERE username = ?", (username,)).fetchone()
    conn.close()
    
    if user:
        user_info = dict(user)
        user_info['date_creation'] = user['date']  # Add account creation date
        return render_template('user_info.html', user=user_info, logged_in=True)
    else:
        return redirect('/login')

# Route to display slots reservation page
@app.route("/reserve_slot", methods=["GET"])
def reserve_slot():
    username = request.cookies.get('username')
    if not username:
        return redirect('/login')
    return render_template("slots.html")

# Route to handle slot reservation
@app.route("/reserve_slot", methods=["POST"])
def reserve_slot_post():
    data = request.get_json()
    title = data.get('title')
    start = data.get('start')
    end = data.get('end')
    username = request.cookies.get('username')

    if not username:
        return jsonify({"error": "Unauthorized access"}), 403

    conn = get_db_connection()
    conn.execute("""
        INSERT INTO Reservations (title, start, end, username)
        VALUES (?, ?, ?, ?);
    """, (title, start, end, username))
    conn.commit()
    conn.close()
    return jsonify({"message": "Réservation effectuée avec succès."}), 200

# API route to return reserved slots in JSON
@app.route("/slots/api", methods=["GET"])
def get_reserved_slots_api():
    conn = get_db_connection()
    slots = conn.execute("SELECT * FROM Reservations;").fetchall()
    conn.close()
    slots_list = [dict(slot) for slot in slots]
    return jsonify(slots_list)

# Run Flask server
if __name__ == "__main__":
    app.run(debug=True)

# Function for gunicorn deployment
def create_app(test_config=None):
    return app


