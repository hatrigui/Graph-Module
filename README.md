# Graph-Module
Ce projet est une API FastAPI avec MongoDB pour la gestion des noeuds.

### Description des Fichiers

- **`app/__init__.py`** : Fichier d'initialisation pour le module `app`.
- **`app/main.py`** : Point d'entrée de l'application FastAPI, où l'application est définie et les routeurs sont inclus.
- **`app/db.py`** : Fichier de configuration pour la connexion à MongoDB, gestion du cycle de vie de la base de données, et création des index nécessaires.
- **`app/routers/node_router.py`** : Fichier contenant les endpoints de l'API pour la gestion des noeuds.
- **`tests/test_main.py`** : Fichier de tests pour vérifier le bon fonctionnement de l'application.
- **`.env`** : Fichier optionnel pour définir les variables d'environnement.
- **`.dockerignore`** : Fichier pour ignorer certains fichiers et répertoires lors de la construction de l'image Docker.
- **`.gitignore`** : Fichier pour ignorer certains fichiers et répertoires dans le contrôle de version Git.
- **`Dockerfile`** : Fichier de configuration pour construire l'image Docker de l'application.
- **`docker-compose.yml`** : Fichier de configuration pour orchestrer les conteneurs Docker nécessaires pour l'application.
- **`requirements.txt`** : Fichier listant toutes les dépendances Python nécessaires pour le projet.
- **`README.md`** : Fichier d'instructions pour l'installation, la configuration et l'utilisation du projet.

## Prérequis

- Python 3.11
- MongoDB installé localement ou accessible via une URL de connexion
- Docker 

## Installation

1. Clonez le dépôt :
```bash
   git clone https://github.com/hatrigui/Graph-Module.git
   cd Graph-Module
```
   
2. Créez et activez un environnement virtuel :
```bash
    python -m venv venv
    venv\Scripts\activate  # Sous Windows
    source venv/bin/activate  # Sous macOS/Linux
```

3. Installez les dépendances :
```bash
    pip install -r requirements.txt
```

## Configuration

1. Assurez-vous que MongoDB est installé et en cours d'exécution.
2. Si vous n'utilisez pas localhost:27017, mettez à jour MONGODB_URL dans db.py :
```python
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://votre_url_de_mongodb:27017/graphdb")
```
3. Mettez à jour l'URL de connexion MongoDB dans le fichier .env si nécessaire.

- **Remarque : Si vous utilisez déjà MongoDB sur localhost:27017, vous n'avez pas besoin de changer l'URL.

## Lancer l'Application
Utilisez uvicorn pour lancer l'application FastAPI :
```bash
uvicorn app.main:app --reload
```
## Utilisation de l'API
Pour utiliser l'API, accédez à la documentation interactive de Swagger à l'adresse suivante :

```bash
http://127.0.0.1:8000/docs
```

## Exécution des Tests
1. Définissez le chemin du projet :

```bash
set PYTHONPATH=%CD%  # Sous Windows
export PYTHONPATH=$(pwd)  # Sous macOS/Linux
```
2. Lancez pytest :
```bash
pytest
```
## Docker
Vous pouvez également utiliser Docker pour exécuter l'application :

Construisez et lancez les conteneurs :

```bash
docker-compose up --build
```

Pour accéder à l'API

```arduino
http://127.0.0.1:8000/docs
```


## Documentation
Une documentation détaillée du projet est également disponible dans le fichier documentation.pdf inclus dans le projet.




