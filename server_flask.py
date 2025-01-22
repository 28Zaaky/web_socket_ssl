from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import ssl
import eventlet
from eventlet import wsgi
from datetime import datetime

app = Flask(__name__)
app.secret_key = ''  # Clé secrète pour la session, à preserver !

# Générez la dans un autre fichier avec :
# import os
# app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Initialisation de Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Liste des utilisateurs connectés
users = {}

# Fonction pour gérer les connexions des utilisateurs
@socketio.on('connect')
def handle_connect():
    print(f"Un utilisateur est connecté : {request.sid}")
    username = session.get('username')  # Récupérer le nom d'utilisateur depuis la session HTTP
    
    if username:
        users[request.sid] = username  # Associer le sid à l'utilisateur
        print(f"{username} a rejoint la conversation")
        emit('connection_ack', {'message': f'Bienvenue, {username}! Vous pouvez commencer à chatter!'})
        emit('set_username', username, room=request.sid)  # Émettre l'événement pour annoncer l'utilisateur
        update_user_list()
    else:
        emit('connection_ack', {'message': 'Bienvenue! Entrez votre nom d\'utilisateur'})

# Fonction pour gérer la déconnexion
@socketio.on('disconnect')
def handle_disconnect():
    print(f"Un utilisateur s'est déconnecté : {request.sid}")
    username = users.pop(request.sid, None)
    if username:
        print(f"{username} a quitté la conversation")
        update_user_list()

from datetime import datetime

# Fonction pour gérer l'envoi de message
@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Inconnu")
    if username == "Inconnu":
        username = "moi"

    timestamp = datetime.now().isoformat()

    print(f"Message reçu de {username}: {msg} à {timestamp}")
    
    # Récupérer le partenaire de chat pour cet utilisateur
    chat_partner = user_chat_partners.get(request.sid)

    # Formater le message
    formatted_msg = {"username": username, "message": msg, "timestamp": timestamp}

    if chat_partner:
        # Envoyer le message au partenaire de chat spécifique
        partner_sid = [sid for sid, user in users.items() if user == chat_partner]
        if partner_sid:
            emit('message', formatted_msg, room=partner_sid[0])

    # Toujours envoyer à l'expéditeur aussi
    emit('message', {"username": "moi", "message": msg, "timestamp": timestamp}, room=request.sid)


# Fonction pour mettre à jour la liste des utilisateurs
def update_user_list():
    emit('update_user_list', list(users.values()), broadcast=True)

# Route pour afficher la page d'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour gérer la soumission du formulaire et rediriger vers le chat
@app.route('/connect', methods=['POST'])
def connect():
    username = request.form['username']  # Récupérer le nom d'utilisateur du formulaire
    session['username'] = username  # Sauvegarder l'utilisateur dans la session HTTP
    print(f"{username} a rejoint la conversation")

    # Une fois que le formulaire est soumis, on redirige vers la page de chat
    return redirect(url_for('chat'))

# Route pour afficher la page de chat
@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('home'))  # Rediriger si l'utilisateur n'est pas connecté
    
    username = session['username']
    return render_template('chat.html', username=username)

# Variable pour suivre la personne avec qui chaque utilisateur parle
user_chat_partners = {}

@socketio.on('set_chat_partner')
def handle_set_chat_partner(partner):
    user_chat_partners[request.sid] = partner
    print(f"{users.get(request.sid)} a commencé à parler à {partner}")

if __name__ == '__main__':
    try:
        # Lancer le serveur Flask avec Flask-SocketIO et Eventlet
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='server.crt', keyfile='server.key')

        # Utilisation de Eventlet pour le serveur avec SSL
        # Mettez votre adresse de loopback ou votre ip sur le LAN (pour pouvoir tester avec un ami). 
        eventlet.wsgi.server(eventlet.wrap_ssl(eventlet.listen(('192.168.0.193', 5001)), certfile='server.crt', keyfile='server.key'), app)
    except Exception as e:
        print(f"Erreur lors du démarrage du serveur : {e}")
