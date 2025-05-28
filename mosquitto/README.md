# Recherche sur les HoneyPot

# HoneyPot MQTT:  - Mise en place et documentation

## Objectif

Créer un environnement **honeypot MQTT** destiné à simuler des dispositifs IoT fictifs tout en les surveillant via un tableau de bord remontant les données d'un broker MQTT. L'objectif est de collecter des données de logs enrichies (client ID, IP, topics) de toutes les activités des différents dispositifs.

---

## Principe de fonctionnement

**Mosquitto** est un honeypot a le principe suivant :

- on crée plusieurs dispositifs IoT simulés (capteurs de porte, température, interrupteurs) qui publient périodiquement des messages MQTT sur le broker Mosquitto local,
- un client logger s’abonne à tous les topics (#) pour enregistrer chaque message dans un fichier de logs enrichi, avec timestamp, topic, payload, client ID et adresse IP.,
- une analyse des logs et des logs système de Mosquitto permet d’identifier les clients connectés, leurs IPs, et leurs comportements.
- un dashboard Streamlit visualise en temps réel les logs et met en avant les clients potentiellement malveillants
- l'ensemble tourne sur une VM Debian avec Mosquitto configuré en broker local

---

## Architecture du projet
```bash
mosquitto/
├── devices/                   #Scripts simulant les capteurs 
│   ├── fake_door_sensor.py                
│   ├── fake_temp_device.py  
│   ├── fake_switch.py            
│   └── devices_config.json                    
├── attacker/                  #Scripts simulant les attaques 
│   ├── attacker_flood.py                
│   ├── attacker_spoof.py    
│   └── attacker_spy.py           
├── dashboard/                 #Scripts simulant le dashboard   
│   └── dashboard.py            
├── logs/                      #Scripts simulant les logs                             
│   └── mqtt_logger.py
├── mqtt_log.json              #Logs des messages MQTT
├── orchestral.py              #Script orchestrateur pour lancer les dispositifs 
├── requirements.txt           #Dépendances requises
├── REAMDME.md                 #Documentation du projet
├── venv/                      #Environnement virtuel Python
```
## Prérequis

- Linux ou une VM sous Linux
- Python 3.8+ installé
- Mosquitto MQTT broker installé et fonctionnel
- pip pour installer les dépendances Python
- Il est conseillé de créer un environnement virtuel pour veiller au bon fonctionnement du projet

---

## Installation de Mosquitto

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```
---


## Modification de la configuration de Mosquitto

Pour permettre une meilleure journalisation et autoriser les connexions locales, il est important de:
- Soit modifier le fichier dans ``` /etc/mosquitto/mosquitto.conf ```
- Soit créer un fichier dans ``` /etc/mosquitto/conf.d/```

Peut importe l'option, la configuration utilisée et recommandée ici est la même:
```bash
pid_file /run/mosquitto/mosquitto.pid 

persistence true
persistence_location /var/lib/mosquitto/

allow_anonymous false
password_file /etc/mosquitto/passwd

log_type all
log_type debug
log_dest file /home/user/mosquitto/logs/mosquitto.log

include_dir /etc/mosquitto/conf.d

connection_messages true
log_timestamp true

```

Ensuite, pour appliquer les modifications il est nécessaire de redémarrer Mosquitto avec:

```sudo systemctl restart mosquitto ```

---

## Installation de l'environnement Python

- On va tout d'abord créer et activer l'environnement virtuel Python :
```bash
python3 -m venv venv
source venv/bin/activate
```


- On installe ensuite les dépendances nécessaires :

```bash
pip install paho-mqtt streamlit streamlit-autorefresh
pip install -r requirements.txt
```
---
## Configuration des dispositifs simulés

- Un dossier **devices** contient trois scripts simulant periodiquement des données MQTT: 
    - **fake_door_sensor.py** qui simule un capteur de porte, et envoie toutes les 10 secondes une donnée disant si la porte est ouverte ou fermée.

    - **fake_switch.py** qui simule un interrupteur de lumière, et envoie l'état "ON" ou "OFF" de cet interrupteur toutes les 15 secondes.

    - **fake_temp_device.py** qui simule un capteur de température, et envoie la donnée toutes les 5 secondes pour avoir une température relevée par celui-ci.

- Chacun des dispositifs est ensuite activé ou désactivé dans le fichier **devices_config.json**, par exemple: 
```bash
[
  {
    "script": "devices/fake_door_sensor.py",  #Ici, on active le dispositif de la porte
    "enabled": true
  }
]
```
---
## Lancement du HoneyPot MQTT

- Lancement des dispositifs simulés: Il faut tout d'abord utiliser le script orchestral.py pour lancer les différents dispositifs activés:
```bash
python3 orchestral.py
```

- Collecte des logs MQTT: On lance ensuite le client logger MQTT pour capturer et enregistrer la totalité des messages sur le broker (les logs seront stockéss dans **mqtt_log.json**):
```bash
python3 logs/mqtt_logger.py
```

- Afficher en temps réel les données à travers un dashboard: On finit par lancer le dashboard via Streamlit pour visualiser le fonctionnement du broker MQTT en affichant les derniers messages sous la forme **{timestamp - topic - payload - clientID - IP}**:
```bash
streamlit run dashboard/dashboard.py
```
---

## Simuler des attaques sur le broker

Un dossier nommé **attacker** a été ajouté pour permettre de simuler trois attaques différentes sur le broker MQTT:

- **attacker_flood.py**, qui va permettre d'envoyer un grand nombre de messages MQTT avec des données faussées en peu de temps sur le broker.

- **attacker_spoof.py**, qui va permettre d'envoyer des données erronées sur le broker, ici des températures fausses.

- **attacker_spy.py**, qui va permettre d'écouter les différentes données que reçoit le broker et les reçoit lui aussi.

Les deux premières attaques peuvent être visualisées sur le dashboard directement.

---

