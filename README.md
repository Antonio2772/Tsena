# Tsena - Gestion de Marchés

## Description
Tsena est une application de gestion pour les marchés et les locations de box commerciaux. Elle permet de suivre les paiements des loyers, gérer les emplacements et visualiser l'état des paiements par période. L'application utilise Microsoft Access comme base de données, avec une interface utilisateur développée en Python via PyQt.

## Fonctionnalités
- Visualisation des emplacements sur un plan interactif
- Gestion des paiements de loyer par box commercial
- Système de suivi avec code couleur (vert pour payé, rouge pour impayé)
- Gestion des différents types de paiements:
  - Paiements en retard
  - Paiements en avance
  - Paiements partiels
- Suivi des paiements par périodes (mois/année)
- Gestion des périodes tarifaires spéciales

## Structure du projet
```
Tsena
├── src
│   ├── main.py                 # Point d'entrée de l'application
│   ├── database                # Module pour la gestion de la base de données
│   │   ├── __init__.py
│   │   ├── connection.py       # Connexion à la base de données Access
│   │   └── queries.py          # Exécution des requêtes SQL
│   ├── gui                     # Module pour l'interface graphique
│   │   ├── __init__.py
│   │   ├── main_window.py      # Fenêtre principale de l'application
│   │   ├── widgets             # Widgets personnalisés
│   │   │   ├── __init__.py
│   │   │   ├── box_map.py      # Visualisation du marché et des emplacements
│   │   │   └── payment_form.py # Formulaire de gestion des paiements
│   │   └── views               # Vues pour afficher les données
│   │       ├── __init__.py
│   │       └── payment_view.py # Vue pour le suivi des paiements
│   ├── models                  # Modèles de données
│   │   ├── __init__.py
│   │   ├── box_model.py        # Modèle pour les emplacements commerciaux
│   │   └── payment_model.py    # Modèle pour les paiements
│   └── utils                   # Utilitaires
│       ├── __init__.py
│       └── helpers.py          # Fonctions utilitaires
├── requirements.txt            # Dépendances du projet
├── config.ini                  # Configuration de l'application
└── README.md                   # Documentation du projet
```

## Installation
1. Clonez le dépôt :
   ```
   git clone https://github.com/Davekun017/Tsena.git
   cd Tsena
   ```

2. Installez les dépendances :
   ```
   pip install -r requirements.txt
   ```

3. Configurez la base de données dans `config.ini`.

## Utilisation
Pour démarrer l'application, exécutez le fichier `main.py` :
```
python src/main.py
```

## Configuration
Le système permet de configurer:
- Les tarifs par m² selon les marchés (ex: Andravohangy: 12k Ar/m², Anosibe: 14k Ar/m²)
- Les périodes tarifaires spéciales (comme pour les périodes de fêtes)
- Les dimensions et identifiants des box commerciaux

## Technologies utilisées
- Python (Développement)
- Microsoft Access (Base de données)
- PyQt (Interface graphique)
- pandas (Manipulation des données)

## Contribuer
Les contributions sont les bienvenues ! Veuillez soumettre une demande de tirage pour toute amélioration ou correction.