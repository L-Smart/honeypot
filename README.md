# Projet de recherche sur les honeypot

Ce projet vise à déployer plusieurs honeypots simulant des services typiques dans les environnements IoT et réseau.  
L’objectif est de piéger, enregistrer et analyser des comportements suspects ou malveillants dans un environnement contrôlé et sans risque pour le système hôte.

---

## Structure du projet

```bash
├── mosquitto/ # Honeypot MQTT basé sur Mosquitto
├── SSH # Honeypot SSH interactif basé sur Cowrie
└── README.md # Ce fichier
```

## Honeypot SSH – Cowrie

**Fonctionnalités principales :**

- Simulation d’un faux système Linux accessible via SSH
- Journalisation des connexions, commandes exécutées et fichiers téléchargés
- Aucun accès réel au système (tout est simulé)
- Configuration fine (hostname, utilisateurs, port, système de fichiers factice, etc.)

 Documentation complète dans : `./SSH/`

---

## Honeypot MQTT – Mosquitto

**Fonctionnalités principales :**

- Simule des capteurs IoT (porte, température, interrupteur)
- Logger MQTT abonné à tous les topics pour une journalisation enrichie
- Attaques simulées :
  - flood (déni de service)
  - spoofing (falsification de données)
  - espionnage (écoute des topics)
- Dashboard en temps réel avec Streamlit pour visualiser les événements

 Documentation complète dans : `./mosquitto/`

---


##  Prérequis généraux

- VM ou machine Linux
- Python **≥ 3.8**
- Git, pip et virtualenv installés
- Ports à vérifier selon les services :
  - SSH : `2222` ou autre
  - MQTT : `1883`

---

## Lancement rapide

Cloner le dépôt :
   ```bash
   git clone https://github.com/ethjoe-lsmart/honeypot.git
   cd honeypot
   ```

 Objectifs pédagogiques
- Comprendre le rôle et l’intérêt des honeypots dans une stratégie de cybersécurité

- Expérimenter la détection d’intrusions dans un environnement contrôlé

- Visualiser le comportement d’attaquants automatisés ou humains

- Renforcer ses connaissances sur les protocoles réseau : SSH, MQTT
