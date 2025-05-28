# Recherche sur les HoneyPot

# HoneyPot SSH: Utilisation de Cowrie - Mise en place et documentation

## Objectif

Créer un environnement **honeypot SSH** simulant un système Linux afin de **piéger, observer et analyser** le comportement d’attaquants dans un environnement contrôlé et sans risque.

---

## Principe de fonctionnement

**Cowrie** est honeypot interactif codé en python qui simule un accès shell (SSH ou Telnet, bien que SSH dans notre cas). Lorsqu’un attaquant s’y connecte :

- Il interagit avec un **faux système de fichiers pouvant cloner le principe du système réel** (`honeyfs/`),
- Ses actions sont **enregistrées et loggées** (commandes, fichiers, comportement),
- **Aucun** accès réel au système n’est accordé à l'attaquant.

---

## Architecture du projet
```bash
cowrie/
├── bin/                    # Scripts de lancement et utilitaires
├── cowrie.cfg              # Configuration principale de cowrie
├── cowrie-env/             # Environnement virtuel en Python
├── honeyfs/                # Faux système de fichiers Linux
│   ├── bin/                # Faux exécutables
│   ├── etc/                # Fichiers système simulés
│   ├── proc/               # Infos système factices
│   └── filesystem.yaml     # Structure de l’arborescence générée
├── var/log/cowrie/         # Logs des sessions et des intrusions

```
---

## Prérequis

- Linux ou une VM sous Linux
- Python 3.10 ou 3.11 dans l'idéal
- git, virtualenv et openssh-client


---

## Installation de Cowrie

```bash
git clone https://github.com/cowrie/cowrie.git
cd cowrie
python3 -m virtualenv --python=python3 cowrie-env
source cowrie-env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp etc/cowrie.cfg.dist cowrie.cfg
```

---

## Modification de la configuration de Cowrie

nano etc/cowrie.cfg

Des paramètres mis par défaut sont **importants** à regarder et à **configurer** pour avoir un honeypot efficace, fonctionnant correctement et comme on le souhaite:

- Nom d'hôte (par défaut svr04, qui n'est pas le plus réaliste):
```bash
hostname = svr04   #à modifier
hostname = lsmart  #exemple de modification
```

- Spécifications d'**authentification**, il s'agit d'une partie essentielle au bon fonctionnement de Cowrie
    - la configuration du fichier texte d'authentication liant des noms d'utilisateurs et les mots de passe, voici le chemin par défaut, modifiable:
    ```bash
    userdb_file = ./etc/userdb.txt
    ```

    - la classe d'authentification a deux possibilités:
        - UserDB qui va donc permettre de chercher et lire les données dans userdb.txt
        - AuthRandom qui ne nécessite pas ce fichier texte, mais a besoin de l'ajout du paramètre suivant:
        ```bash
        auth_any_user = true
        ```
        D'autres paramètres son alors à configurer:

        ```bash
        auth_class_parameters = <min try>, <max try>, <maxcache>
        auth_class_parameters = 2, 5, 10 #exemple concret qui permet de donner un accès après un randint(2,5) tentatives de connexion et avec un cache de 10 combinaisons.
        ```

    - Configuration SSH:
    ```bash
    enabled = true #par défaut
    listen_port = <port souhaité>
    listen_port = 2222 #exemple concret

    listen_endpoints = tcp:<port souhaité>:interface:0.0.0.0
    listen_endpoints = tcp:2223:interface:0.0.0.0
    ```

---

## Création du système de fichiers (honeyfs/)

```bash
mv honeyfs honeyfs_backup
mkdir -p honeyfs/{bin,etc,proc,root,home/user}
```
---

## Ajout possible de contenu

```bash
cat > honeyfs/etc/passwd <<EOF
root:x:0:0:root:/root:/bin/bash
ethan:x:1000:1000:Ethan:/home/ethan:/bin/bash
EOF

cat > honeyfs/etc/shadow <<EOF
root:*:19000:0:99999:7:::
ethan:*:19000:0:99999:7:::
EOF

echo "honeypot" > honeyfs/etc/hostname

echo -e '#!/bin/sh\necho "bin  etc  home  proc  root"' > honeyfs/bin/ls
chmod +x honeyfs/bin/ls

```

---

## Générer un fichier filesystem.yaml

- Cette étape est à réaliser **à chaque fois** que l'on modifie le système de fichiers et son contenu.
- Le fichier est en binaire donc pas modifiable en l'état, le script **createfs** le crée lui-même et est interprêté par Cowrie.

```bash
rm -f honeyfs/filesystem.yaml
bin/createfs -o honeyfs/filesystem.yaml honeyfs/
```

---

## Lancer Cowrie
```bash
source cowrie-env/bin/activate
./bin/cowrie start

tail -f var/log/cowrie/cowrie.log #Vérifier les logs en direct
```

---

## Se connecter à Cowrie

```bash
ssh -p <port> user@ip
```
Exemple concret d'utilisation: 
```bash
ssh -p 2222 ethan@127.0.0.1
```

On peut donc maintenant tester la connexion en entrant un mot de passe:

- si le mot de passe est incorrect, on a "Permission denied, please try again."
- sinon, on accède au bash simulé.

---

## Tester le fonctionnement de Cowrie une fois connecté

On a la possibilité de tester différentes commandes, telles que:

- ls
- cat /etc/passwd
- whoami

---

## Arrêter Cowrie
```bash
./bin/cowrie stop
```