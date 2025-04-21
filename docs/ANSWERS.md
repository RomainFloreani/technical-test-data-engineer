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

Pour une mise en production d’un pipeline de données, je recommande l’utilisation de la base de données relationnelle PostgreSQL, ou l’une de ses variantes gérées dans le cloud, telles que Azure Database for PostgreSQL ou Amazon RDS.

- PostgreSQL permet l’utilisation de requêtes SQL complexes et de fonctions personnalisées.
- PostgreSQL prend en charge une large variété de types natif mais aussi des types complexes comme `JSON`.
- PostgreSQL garantit l’Atomicité, la Cohérence, l’Isolation et la Durabilité des transactions, assurant ainsi l’intégrité des données.
- PostgreSQL peut être connecté à des outils de visualisation comme Power BI, à des pipelines de machine learning, ou peut être utiliser dans d'autres cas d'usages.

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

Pour suivre la santé du pipeline de données exécuté quotidiennement, il est important de mettre en place une combinaison de logs, de métriques et éventuellement d’alertes.

Les logs permettent de tracer l'exécution de chaque étape (extraction, transformation, chargement) et d'identifier rapidement l’origine d’un échec. Des métriques simples comme la durée d'exécution, le nombre d’enregistrements extraits ou insérés, ou la réussite des tests automatisés sont essentielles pour évaluer le bon fonctionnement global du pipeline.

Voici quelques exemple de métriques utiles pour évaluer la santé du pipeline :

```
| Métrique                         | Description                                                        |
|----------------------------------|--------------------------------------------------------------------|
| Statut d’exécution               | Succès ou échec des jobs (tests, pipeline)                         |
| Temps d’exécution                | Durée totale du pipeline et de chaque étape (ETL)                  |
| Disponibilité de l’API           | Résultat de l’étape `test_endpoints()`                             |
| Volume de données extraites      | Nombre d’éléments extraits pour chaque source (`tracks`, etc.)     |
| Réussite des tests               | Nombre d’erreurs rencontrées dans les tests                        |
```

Des alertes peuvent être définies en fonction de ces métriques clés, mais également en cas d’échec d’un test unitaire.

#### Évolutions futures:

Il serait aussi possible d'ajouter des tests d’intégration ou de type smoke test pour valider l’état général de l’environnement avant de lancer l’exécution du pipeline.

Enfin, bien que GitHub Actions soit suffisant pour une première version, la migration vers un moteur de workflow de données comme Databricks permettrait de bénéficier de fonctionnalités natives de surveillance, de planification avancée et de gestion des échecs de tâches.

### Étape 6

Une fois les données extraites et enregistrées chaque jour, il devient possible d’automatiser le calcul de recommandations musicales basées sur le comportement d’écoute des utilisateurs.

L’idée est d’ajouter une étape juste après le pipeline ETL, qui analyserait l’historique d’écoute des utilisateurs et leur proposerait des morceaux qu’ils pourraient aimer. Par exemple, les recommandations pourraient se baser sur leurs genres musicaux préférés, leurs artistes les plus écoutés, ou sur des comportements similaires observés chez d'autres utilisateurs.

Une première approche consisterait à utiliser un modèle simple de type KNN (K-Nearest Neighbors). Le modèle utiliserait les données combinées des trois tables (`users`, `tracks`, `listen_history`) pour créer une représentation de chaque utilisateur.

#### Architecture proposée

1. Transformation des données :
   Combiner les données des trois tables pour créer une table par utilisateur contenant des caractéristiques (features) clés.

2. Création de colonnes enrichies :
   Par exemple :

- Le genre le plus écouté
- L’artiste le plus écouté
- Le moment de la journée le plus fréquent pour écouter de la musique
- La diversité des genres écoutés

3. Construction de la table d’apprentissage :
   Cette table contiendra une ligne par utilisateur avec les colonnes créées ci-dessus. On pourra aussi y inclure des agrégats statistiques (nombre total d’écoutes, durée moyenne, etc.).

4. Application du modèle KNN :
   En utilisant ces données, on peut appliquer un algorithme KNN pour identifier des utilisateurs similaires. Ensuite, on peut recommander des morceaux qu’ils ont écoutés mais que l’utilisateur cible n’a pas encore découverts.

5. Sauvegarde des recommandations :
   Les recommandations générées peuvent être enregistrées dans une table recommendations, avec les champs suivants : user_id, track_id, score, date_calcul.

6. Automatisation :
   Ce calcul peut être déclenché automatiquement chaque jour après le pipeline ETL. Il peut être intégré dans le même workflow GitHub Actions, ou bien orchestré via une plateforme dédiée comme Databricks afin d’assurer un meilleur suivi et une gestion des dépendances entre les étapes.

### Étape 7

Une fois qu’un modèle de recommandation est mis en place, il est important de le réentraîner régulièrement pour qu’il continue à proposer des résultats pertinents. Les préférences des utilisateurs peuvent évoluer, de nouveaux morceaux peuvent apparaître, et certains comportements peuvent changer avec le temps.

L’objectif ici est donc d’automatiser ce processus de réentraînement, de manière planifiée, en utilisant les données actualisées du pipeline.

Le réentraînement ne doit pas forcément ce faire de façon hebdomadaire ou mensuelle est souvent satisfaisate.

Solution proposée:

1. Réentraînement du modèle
   Le modèle (par exemple un KNN) est réentraîné avec les nouvelles données. Cela peut se faire via un script Python déclenché automatiquement, qui charge les données, entraîne le modèle, puis le sauvegarde.
2. Sauvegarde et versionning du modèle
   Le modèle entraîné est sauvegardé dans un fichier. Cela permet de suivre l’évolution du modèle dans le temps et de revenir à une version antérieure en cas de problème.
3. Remplacement du modèle utilisé en production
   Une fois le nouveau modèle validé, il peut remplacer celui utilisé pour le calcul quotidien des recommandations.
4. Procéder au réeentraînement dans un moteur de workflow comme Databricks.

Il faut aussi implémenter un système de suivi pour savoir si le modèle fonctoinne et les utilisateurs sont satisfaits:

- Un champ `feedback` (like/dislike) ou un taux de clic sur les morceaux recommandés.
- Une analyse de si l’utilisateur a effectivement écouté ou ignoré le morceau recommandé
- Le suivi de la performance des recommandations dans le temps (adoption, taux d’écoute, skip rate)

Ces données permettent ensuite de réévaluer la qualité du modèle et d'ajuster les algorithmes ou les règles.

Pour améliorer les performances du modèle de machine learning, il serait possible d'ajouter des APIs supplémentaires afin de récupérer davantage d'informations sur les utilisateurs, les morceaux ou leur contexte d'écoute. Cependant, il est important de nuancer : plus de données ne signifie pas nécessairement un meilleur modèle.

L’essentiel est de mettre en place un bon processus de feature engineering, c’est-à-dire identifier les variables réellement utiles et pertinentes pour le modèle. Il faut donc tester, analyser et sélectionner les colonnes qui ont le plus d’impact sur la qualité des recommandations, plutôt que de multiplier les sources de données sans objectif clair.
