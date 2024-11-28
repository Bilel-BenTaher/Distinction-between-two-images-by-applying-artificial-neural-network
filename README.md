# Distinction entre deux images par l’application du réseau de neurones artificiels

## Description

Ce projet implémente un réseau de neurones artificiels pour distinguer deux types d'images : **chat** et **chien**. Le modèle est entraîné sur un ensemble d'images, où chaque image est étiquetée comme étant un chat ou un chien. Le réseau utilise une architecture de couches cachées avec des poids et biais ajustés via la rétropropagation et la descente de gradient. Les performances du modèle sont évaluées à l'aide des métriques de **log loss** et **précision**.

## Fonctionnalités

- Chargement et prétraitement des données depuis des fichiers HDF5.
- Réseau de neurones avec plusieurs couches cachées, personnalisable.
- Utilisation de la descente de gradient pour l’entraînement.
- Affichage des courbes de **log loss** et de **précision** pendant l’entraînement.
- Évaluation du modèle sur les ensembles d'entraînement et de test.

## Fichiers de données

Le fichier `datasets` contient les données nécessaires pour l'entraînement et le test du modèle, incluant les ensembles d'images étiquetées pour les **chats** et **chiens**.

## Prérequis

Pour exécuter ce projet, vous devez avoir installé les bibliothèques suivantes :

- Python 3.x
- `numpy`
- `matplotlib`
- `scikit-learn`
- `h5py`
- `tqdm`
