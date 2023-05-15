# Prédiction Erreur JetVarnish3D

## Objectif

Ce projet vise à prédire si le prochain travail d'impression de l'imprimante JetVarnish3D va générer un évènement du type "arrêt d'urgence", "erreur", "défaut" ou "bourrage". En utilisant un modèle entraîné sur les données historiques, nous cherchons à identifier une corrélation entre les données des travaux d'impression et la survenanace d'un évènement mettant le status de l'imprimante en erreur. La prédiction d'erreur permettra de prendre des mesures préventives pour éviter les problèmes potentiels, d'améliorer la qualité des travaux d'impression et de minimiser les interruptions de production.

## Données

Les données fournies par l'équipe MGI ont été analysées et concaténées pour créer un jeu de données consolidé. Les fichiers CSV utilisés sont les suivants :

- `metrics.csv` : Ce fichier contient les status de l'imprimante à intervals réguliers parfois associés à un ou plusieurs évènements.

- `jobs.csv` : Ce fichier contient des informations sur les travaux d'impression, tels que le type de travail, la taille, la durée, etc.

- `job_events.csv` : Ce fichier contient les données associés aux travaux d'impression, en début, en cours et en fin de travail.

L'exécution des notebooks 01 et 03 permet de vérifier l'existance en local de ces fichiers dans le répertoire local '/data/raw', sinon le téléchargement depuis le stockage Azure Blob.


## Modèles

Plusieurs modèles ont été utilisés pour entraîner et évaluer la prédiction d'erreur pour le prochain travail d'impression. Les modèles suivants ont été considérés :

1. SVM (Support Vector Machine) : Un modèle d'apprentissage supervisé utilisé pour la classification et la régression.

2. Arbre de décision : Un modèle d'apprentissage supervisé qui utilise une structure d'arbre pour prendre des décisions basées sur les caractéristiques des données.

3. XGBoost : Une implémentation optimisée du gradient boosting, un algorithme d'apprentissage automatique populaire pour les problèmes de classification et de régression.

4. LSTM (Long Short-Term Memory) : Un type de réseau de neurones récurrents (RNN) capable de prendre en compte les dépendances à long terme dans les séquences de données.

Ces modèles ont été choisis en raison de leur efficacité dans la classification et la prédiction de données structurées.


## Etapes

01 - fractionnement des colonnes de metrics

02 - nettoyage des données de metrics

03 - fractionnement des colonnes de job_events

04 - nettoyage de job_events

05 - nettoyage de jobs

06 - fusion de jobs et job_events

07 - concanténation de jobs/job_events et metrics générant un dataset pour le preprocess

08 - analyse et nettoyage du dataset preprocess générant un dataset pour le training (sans encodage, ni normalisation)


## Dépendances

Le code Python de ce projet nécessite notamment les dépendances suivantes :
- numpy
- pandas
- scikit-learn
- keras (avec TensorFlow backend)

Veillez à les installer les requirements.txt avant d'exécuter le code.

## Auteurs

Ce projet a été réalisé par l'équipe IA de Fabéon : Allan, Arthur et Audrey.

---

*Note : Assurez-vous d'avoir les fichiers de données 'metrics.csv', 'jobs.csv' et 'job_events.csv' dans le répertoire de travail