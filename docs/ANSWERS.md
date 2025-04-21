# Réponses du test

## Etapes 1 à 3:

### Sommaire:

Cette solution consiste en la conception et l’implémentation d’un pipeline ETL complet, capable de récupérer des données via une API FastAPI, de les transformer, puis de les charger dans une base de données SQLite. L’ensemble du processus est automatisé via GitHub Actions, et accompagné d’un ensemble de tests automatisés.

Le pipeline est structuré en deux étapes CI distinctes :

- Un job de tests (unitaires et dépendants de l’API)
- Un job d’exécution du pipeline ETL, déclenché uniquement si les tests réussissent

Ci-desous vous trouverez les détails de l'implémentation technique:

### Mise en place de l'environnement de développement

Pour garantir un environment reproductible, j'ai utilisé un environment virtuel Python voici les étapes de configurations:

```
 # Création de l’environnement virtuel
python -m venv .venv

# Activation
source .venv/bin/activate

# Installation des dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

Le fichier `requirements.txt` contient les libraries à l'exécution du pipeline.

### Construction du pipeline ETL

Le pipeline est structuré autour de trois modules:

#### Extaction

Le module `src/data_pipeline/extract.py` interogge trois points de terminaison FasAPI:

- `/tracks`
- `/users`
- `/listen_history`

Les données sont extraitent en format `.json`

#### Transformation

Le module `src/data_pipeline/transform.py` nettoie et restructure les données en conformité avec le schéma de la bse de données. Cela inclut:

- La normalisation des types de champs
- Le dépliage des champs imbriqués (ex: `listen_history.items`)

#### Chargement:

Le module `src/data_pipeline/load.py` insère les données transformées dans une base données SQLite (`music_data.db`). Les trois tables crées sont:

- `tracks`
- `users`
- `listen_history`

L'ensemble du processus est orchestré par `run_etl.py`

### Mise en place des tests automatisés

Deux types de tests ont été définis:

#### Tests unitaires (`@pytest.mark.unit`)

Testant la logique et les fonctions de transformaiton et la structure de la base de données.

Exemple:

```
@pytest.mark.unit
def test_transform_tracks(): ...
```

#### Tests dépendents de l'API (`@pytest.mark.api`)

Simulent les réponses des endpoints FastAPI à l'aide de `requests-mock`.

Exemple:

```
@pytest.mark.api
def test_tracks_extract(requests_mock): ..
```

### Intégration continue:

L'exécution des tests et du pipeline est automatisée via GitHub Actions avec deux jobs distincts:

- `tests`: valide les tests unitaires et API
- `pipeline`: exécute le pipeline ETL uniquement si les tests passent.

Pour rouler le pipeline:

1. Sur le dépót Github cliquez sur le boutton `Actions`
2. Sur la barre de gauche vous allez voir écrit: `CI Pipeline`
3. Puis vous pourriez cliquer à droite sur `Run workflow` et celà va trigger le pipeline.

### Limitations et améliarations futures:

- **Utilisation d’un agent avec un stockage persistant**
  Actuellement, chaque exécution du pipeline dans GitHub Actions nécessite la réinstallation des dépendances. En déployant le pipeline sur un agent disposant d’un stockage persistant (ex. : un runner auto-hébergé), on pourrait conserver l’environnement virtuel entre les runs et ainsi réduire significativement le temps d’exécution.

- **Stockage des données dans une base de données centralisée**
  Les données sont actuellement stockées dans une base SQLite locale, ce qui limite leur accessibilité et leur scalabilité. Une amélioration importante serait de persister les données dans une base de données relationnelle (PostgreSQL, MySQL) ou cloud (Azure SQL, BigQuery, etc.), selon les besoins d’accessibilité ou de sécurité (ex. : base de données on-premises pour la conformité).

- **Orchestration via un moteur de workflow dédié**
  GitHub Actions permet l’automatisation de tâches, mais n’est pas conçu spécifiquement pour l’orchestration de flux de données. À terme, il serait pertinent d'utiliser un moteur de workflow comme Apache Airflow ou Databricks Workflows. Ces outils offrent une meilleure gestion des dépendances entre tâches, un suivi visuel de l’exécution, et des fonctionnalités avancées de reprise sur échec, planification, et monitoring.

## Questions (étapes 4 à 7)

### Étape 4

_votre réponse ici_

### Étape 5

_votre réponse ici_

### Étape 6

_votre réponse ici_

### Étape 7

_votre réponse ici_
