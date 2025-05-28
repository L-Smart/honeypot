# 🐝 Projet Honeypots IoT & Réseaux

Ce projet vise à déployer plusieurs honeypots simulant des services typiques dans les environnements IoT et réseau.  
L’objectif est de piéger, enregistrer et analyser des comportements suspects ou malveillants dans un environnement contrôlé et sans risque pour le système hôte.

---

## 📁 Structure du projet


├── mosquitto/ # Honeypot MQTT basé sur Mosquitto
├── SSH # Honeypot SSH interactif basé sur Cowrie
├── HTTP/ # Honeypot HTTP (documentation à compléter)
└── README.md # Ce fichier

## 🔐 Honeypot SSH – Cowrie

**Fonctionnalités principales :**

- Simulation d’un faux système Linux accessible via SSH
- Journalisation des connexions, commandes exécutées et fichiers téléchargés
- Aucun accès réel au système (tout est simulé)
- Configuration fine (hostname, utilisateurs, port, système de fichiers factice, etc.)

📂 Documentation complète dans : `./SSH/`

---

## 📡 Honeypot MQTT – Mosquitto

**Fonctionnalités principales :**

- Simule des capteurs IoT (porte, température, interrupteur)
- Logger MQTT abonné à tous les topics pour une journalisation enrichie
- Attaques simulées :
  - flood (déni de service)
  - spoofing (falsification de données)
  - espionnage (écoute des topics)
- Dashboard en temps réel avec Streamlit pour visualiser les événements

📂 Documentation complète dans : `./mosquitto/`

---

## 🌐 Honeypot HTTP – (À compléter)


📂 Documentation prévue dans : `./HTTP/`

---

## ⚙️ Prérequis généraux

- VM ou machine Linux
- Python **≥ 3.8**
- Git, pip et virtualenv installés
- Ports à vérifier selon les services :
  - SSH : `2222` ou autre
  - MQTT : `1883`
  - HTTP : `à compléter` 

---

## 🚀 Lancement rapide

Cloner le dépôt :
   ```bash
   git clone https://github.com/ethjoe-lsmart/honeypot.git
   cd honeypot
   ```
