# Chat en temps réel avec Flask et SocketIO

## Description

Ce projet implémente une application de messagerie en temps réel à l'aide de Flask et Flask-SocketIO. Il utilise SSL/TLS pour sécuriser les communications entre le serveur et les clients. Les utilisateurs peuvent se connecter via un navigateur, s'authentifier avec un nom d'utilisateur, et échanger des messages de manière sécurisée.

## Fonctionnalités

- **Authentification** : L'utilisateur entre un nom d'utilisateur via un formulaire. Le nom est enregistré dans la session HTTP.
- **Messagerie en temps réel** : Grâce à Flask-SocketIO, les messages sont envoyés et reçus instantanément.
- **Connexion sécurisée** : Le serveur utilise SSL pour garantir la sécurité des communications.
- **Chat en privé** : Les utilisateurs peuvent discuter en tête-à-tête avec d'autres utilisateurs.
- **Liste d'utilisateurs en ligne** : La liste des utilisateurs connectés est mise à jour en temps réel.

## Fonctionnement

### Serveur

Le serveur utilise Flask pour gérer les requêtes HTTP, avec Flask-SocketIO pour la gestion de la messagerie en temps réel via des websockets. Lorsqu'un utilisateur se connecte, il choisit un nom d'utilisateur, qui est stocké dans une session HTTP. Une fois connecté, l'utilisateur peut envoyer des messages qui seront transmis aux autres utilisateurs en temps réel.

### Client

Le client se connecte au serveur via SocketIO en utilisant le protocole SSL pour sécuriser les échanges. Après s'être authentifié en envoyant un nom d'utilisateur, il peut envoyer des messages à un ou plusieurs utilisateurs. Les messages sont reçus et envoyés en temps réel, et l'interface est mise à jour instantanément avec les nouveaux messages.

### Architecture réseau

Le serveur utilise des sockets sécurisés pour établir des connexions avec les clients. L'authentification de chaque utilisateur est réalisée par session HTTP. Les messages sont ensuite envoyés via des websockets, garantissant une communication en temps réel et sécurisée.

## Prérequis

Avant d'exécuter ce projet, assurez-vous d'avoir installé les dépendances suivantes :

- Python 3
- Flask
- Flask-SocketIO
- Eventlet
- OpenSSL (pour la gestion des certificats SSL)
