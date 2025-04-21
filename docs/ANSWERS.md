# Réponses du test

## Etapes 1 à 3:

### Sommaire:

Cette solution consiste en la conception et l’implémentation d’un pipeline ETL complet, capable de récupérer des données via une API FastAPI, de les transformer, puis de les charger dans une base de données SQLite. L’ensemble du processus est automatisé via GitHub Actions, et accompagné d’un ensemble de tests automatisés. Le procesus contient un champ `schedule` pour être éxécuter tous les jours à 9:00 UTC.

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

#### Quel système de base données

Pour une mise en production d'une pipeline de données, je recommande l'utilisaiton de base de données **PostgreSQL**, ou l'une variantes gérées dans le cloud (Azure PostgreSql, Amazon RDS ou Google Cloud SQL).

- Robustesse et fiabilité: PostreSQL est un SGBD open source éprouvé, reconnu pour sa stablité en produciton.
- Support avancé des types données: Excellente prise en charge des types complexes comme `JSON`, `ARRAY`, ou `TIMESTAMP`, utiles dans le contexte de la modélisation des données musicales ou historique.
- Scalabilité: Peut évoluer pour gérer de grands volume de données avec des options de partionnement, indexaiton et replication.
- Écosystème riche: Compatible avec de nombreux outils d’analytique, de visualisation (ex. : Metabase, Power BI), ou de machine learning.
- sécurité et conformité: Possibilité d'intégration avec des systèmes d'authentification d'entreprise et de configuration fine des droits d'accès.

#### Schéma relationnel proposé

Les données récupérées depuis l'API sont structurées dans une base de données relationnelle composée des trois tables suivants:

`tracks`

```
| Colonne       | Type      | Description                           |
|---------------|-----------|---------------------------------------|
| id            | INTEGER   | Identifiant unique du morceau         |
| name          | TEXT      | Nom du morceau                        |
| artist        | TEXT      | Nom de l’artiste                      |
| songwriters   | TEXT      | Auteurs-compositeurs                  |
| duration      | TEXT      | Durée du morceau (format HH:MM:SS)    |
| genres        | TEXT      | Genre musical                         |
| album         | TEXT      | Nom de l’album                        |
| created_at    | DATETIME  | Date de création de l’enregistrement  |
| updated_at    | DATETIME  | Date de dernière mise à jour          |

```

`users`

```
| Colonne           | Type      | Description                           |
|-------------------|-----------|---------------------------------------|
| id                | INTEGER   | Identifiant unique de l’utilisateur   |
| first_name        | TEXT      | Prénom                                |
| last_name         | TEXT      | Nom de famille                        |
| email             | TEXT      | Adresse e-mail                        |
| gender            | TEXT      | Genre                                 |
| favorite_genres   | TEXT      | Genres musicaux préférés              |
| created_at        | DATETIME  | Date de création de l’enregistrement  |
| updated_at        | DATETIME  | Date de dernière mise à jour          |
```

`listen_history`

```
| Colonne           | Type      | Description                           |
|-------------------|-----------|---------------------------------------|
| user_id           | INTEGER   | Identifiant unique de l’utilisateur   |
| track_id          | TEXT      | Identifiant unique du morceau         |
| created_at        | DATETIME  | Date de création de l’enregistrement  |
| updated_at        | DATETIME  | Date de dernière mise à jour          |
```

### Étape 5

Pour assurer la fiabilité et la transparence de l’exécution quotidienne du pipeline de données, il est essentiel de mettre en place un système de supervision (monitoring). Cela permet de détecter rapidement les anomalies, les échecs ou les dégradations de performance.

Dans un premier temps, une approche simple et efficace consiste à :

- Utiliser les logs des étapes du pipeline : chaque étape (extract, transform, load) génère des messages explicites sur son état (✅ terminé, ❌ échec, etc.).
- Superviser les statuts d’exécution via GitHub Actions : l’interface CI fournit un aperçu rapide des succès/échecs, avec des étapes bien segmentées.
- Utiliser des notifications automatiques (optionnel) : on peut configurer des notifications par e-mail ou Slack via GitHub Actions en cas d’échec.

Voici quelques indicateurs utiles pour évaluer la santé du pipeline :

```
| Métrique                         | Description                                                        |
|----------------------------------|--------------------------------------------------------------------|
| Statut d’exécution               | Succès ou échec des jobs (tests, pipeline)                         |
| Temps d’exécution                | Durée totale du pipeline et de chaque étape (ETL)                  |
| Disponibilité de l’API           | Résultat de l’étape `test_endpoints()`                             |
| Volume de données extraites      | Nombre d’éléments extraits pour chaque source (`tracks`, etc.)     |
| Erreurs de parsing/transformation| Nombre ou type d’erreurs rencontrées                               |
| Taux d’insertion en base         | Nombre de lignes insérées avec succès vs. échecs                   |
```

#### Évolutions futures:

À moyen terme, il serait pertinent d’ajouter un moteur de workflow tel que Databricks, qui offrent :

- Un tableau de bord de monitoring intégré
- La possibilité de redémarrer des étapes échouées
- Un historique détaillé des exécutions
- Des alertes natives en cas d’anomalie

### Étape 6

L’objectif est d’automatiser le calcul des recommandations musicales à partir des données déjà extraites et stockées dans la base. Ce calcul pourrait, par exemple, s’appuyer sur l’historique d’écoute des utilisateurs pour leur proposer des morceaux similaires ou populaires dans leurs genres préférés.

#### Architecture proposée:

Voici les étapes du processus d’automatisation :

1. Déclencheur quotidien : une tâche planifiée (cron) lance le calcul chaque jour, après la fin du pipeline ETL.
2. Lecture des données : les données sont chargées depuis la base de données (ex. : SQLite, PostgreSQL).
3. Application d’un algorithme de recommandation :
   - Recommandation basée sur les genres favoris
   - Fréquence d’écoute par utilisateur
   - Coécoute (collaborative filtering)
4. Enregistrement des résultats dans une table dédiée recommendations :
   - `user_id`,`track_id`,`score`,`date_calcul`

Cette tâche peut être orchestrée à l'aide de:

- Un job GitHub Actions supplémentaire déclenché après l’ETL
- Ou idéalement, un moteur de workflow comme Prefect, Airflow, ou Databricks Workflows, permettant :
  - La gestion des dépendences (exécuter le calcul après l'ETL)
  - La gestion des échecs
  - La visualization de l'exécution

```
def calculate_recommendations():
    # Connexion à la base
    conn = sqlite3.connect("music_data.db")

    # Exemple simplifié : recommandations par genre préféré
    query = """
    SELECT users.id as user_id, tracks.id as track_id, tracks.genres
    FROM users
    JOIN tracks ON tracks.genres = users.favorite_genres
    """
    rows = conn.execute(query).fetchall()

    # Transformation en résultats de recommandations
    recommendations = [
        {"user_id": r[0], "track_id": r[1], "score": 1.0} for r in rows
    ]

    # Insertion dans une table recommendations
    ...
```

![Diagramme mermaid]()

### Étape 7

Pour que le système de recommandation reste pertinent dans le temps, il est essentiel de mettre à jour régulièrement le modèle utilisé. Cela permet de tenir compte des nouveaux utilisateurs, morceaux, comportements d’écoute ou tendances musicales.

1. Déclancheur programmé:
   Le réentraînement peut être planifié à une fréquence adaptée (par exemple chaque semaine ou chaque mois) à l’aide :

   - D'une tâche `cron`
   - D'un moteur de workflow tel que Prefect, Airflow, ou Databricks

2. Chargement des données actualisées
   Le script de réentraînement se base sur les données extraites et transformées, présentes en base (ex. : listen_history, users, tracks).

3. Prétraitement & feature engineering

   - Construction de matrices utilisateurs/morceaux
   - Encodage des genres, fréquence d'écoute, etc.

4. Entraînement du modèle:

   - Algorithmes possibles : KNN, SVD, ALS, modèles de deep learning, etc.
   - Évaluation automatique des performances (précision, rappel, etc.)

5. Versionnement et déploiement

   - Le modèle est enregistré (ex. : via joblib, MLflow ou pickle)
   - Il peut être versionné et utilisé par le calcul quotidien des recommandations

6. Journalisation et monitoring

   - Journal des performances du modèle
   - Notifications en cas d’échec ou de baisse de qualité

Exemple d'orchestration:

- exécution de la donnée RAW
- Roule le réentrainement chaque semaine.
- Générer des recommendations à partir du modèle entraîné.

![Diagramme Mermaid]()
