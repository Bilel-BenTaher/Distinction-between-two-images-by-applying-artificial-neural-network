# Importation des librairies nécessaires
import h5py  # Pour la gestion des fichiers HDF5
import numpy as np  # Pour les opérations numériques
import os  # Pour la gestion des fichiers et des répertoires
import matplotlib.pyplot as plt  # Pour l'affichage des courbes de performance
from sklearn.metrics import accuracy_score, log_loss  # Pour l'évaluation des performances du modèle
from tqdm import tqdm  # Pour afficher une barre de progression lors des itérations

# Fonction de chargement des données depuis les fichiers HDF5
def load_data():
    # Définition des chemins des fichiers de données
    train_path = 'C:/Users/hp/OneDrive/DESKTOP/Code/trainset.hdf5'
    test_path = 'C:/Users/hp/OneDrive/Desktop/Code/testset.hdf5'

    # Vérification de l'existence des fichiers
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Le fichier de train {train_path} est introuvable.")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Le fichier de test {test_path} est introuvable.")
    
    # Ouverture des fichiers HDF5 et extraction des données
    with h5py.File(train_path, "r") as train_dataset, h5py.File(test_path, "r") as test_dataset:
        # Chargement des caractéristiques et des labels pour l'entraînement
        X_train = np.array(train_dataset["X_train"][:])
        y_train = np.array(train_dataset["Y_train"][:])
        y_train = y_train.reshape(1, -1)  # Reshape pour assurer une forme (1, n_exemples)
        
        # Chargement des caractéristiques et des labels pour le test
        X_test = np.array(test_dataset["X_test"][:])
        y_test = np.array(test_dataset["Y_test"][:])
        y_test = y_test.reshape(1, -1)

    return X_train, y_train, X_test, y_test

# Fonction d'initialisation des paramètres du réseau
def initialisation(dimensions):
    parametres = {}
    C = len(dimensions)

    np.random.seed(1)  # Fixe la graine pour la reproductibilité des résultats

    # Initialisation des poids et biais pour chaque couche
    for c in range(1, C):
        parametres['W' + str(c)] = np.random.randn(dimensions[c], dimensions[c - 1]) * 0.01  # Poids aléatoires
        parametres['b' + str(c)] = np.zeros((dimensions[c], 1))  # Biais initialisés à zéro

    return parametres

# Fonction de propagation avant (forward propagation) pour calculer les activations
def forward_propagation(X, parametres):
    activations = {'A0': X}
    C = len(parametres) // 2  # Nombre de couches

    # Calcul des activations pour chaque couche
    for c in range(1, C + 1):
        Z = parametres['W' + str(c)].dot(activations['A' + str(c - 1)]) + parametres['b' + str(c)]  # Calcul de Z
        activations['A' + str(c)] = 1 / (1 + np.exp(-Z))  # Activation par fonction sigmoïde

    return activations

# Fonction de rétropropagation pour calculer les gradients
def back_propagation(y, parametres, activations):
    m = y.shape[1]
    C = len(parametres) // 2
    dZ = activations['A' + str(C)] - y  # Calcul de l'erreur de la dernière couche
    gradients = {}

    # Calcul des gradients pour chaque couche en remontant (backpropagation)
    for c in reversed(range(1, C + 1)):
        gradients['dW' + str(c)] = 1 / m * np.dot(dZ, activations['A' + str(c - 1)].T)  # Gradient des poids
        gradients['db' + str(c)] = 1 / m * np.sum(dZ, axis=1, keepdims=True)  # Gradient des biais
        if c > 1:
            dA = np.dot(parametres['W' + str(c)].T, dZ)  # Propagation des erreurs aux couches précédentes
            dZ = dA * activations['A' + str(c - 1)] * (1 - activations['A' + str(c - 1)])  # Derivée de la sigmoïde

    return gradients

# Fonction de mise à jour des paramètres avec la descente de gradient
def update(gradients, parametres, learning_rate):
    C = len(parametres) // 2

    # Mise à jour des poids et des biais pour chaque couche
    for c in range(1, C + 1):
        parametres['W' + str(c)] -= learning_rate * gradients['dW' + str(c)]
        parametres['b' + str(c)] -= learning_rate * gradients['db' + str(c)]

    return parametres

# Fonction de prédiction (utilise la propagation avant pour obtenir les activations finales)
def predict(X, parametres):
    activations = forward_propagation(X, parametres)
    C = len(parametres) // 2
    Af = activations['A' + str(C)]  # Activations de la dernière couche
    return (Af >= 0.5).astype(int)  # Classification binaire (1 ou 0)

# Fonction principale pour entraîner et évaluer le réseau de neurones
def deep_neural_network(X_train, y_train, X_test, y_test, hidden_layers, learning_rate, n_iter):
    # Initialisation des paramètres du réseau
    dimensions = list(hidden_layers)
    dimensions.insert(0, X_train.shape[0])  # Ajouter la dimension d'entrée
    dimensions.append(y_train.shape[0])  # Ajouter la dimension de sortie
    parametres = initialisation(dimensions)

    # Historique des performances (log loss et accuracy)
    training_history = np.zeros((n_iter, 4))  # [train_loss, test_loss, train_acc, test_acc]

    # Gradient descent: boucle d'entraînement
    for i in tqdm(range(n_iter)):
        # Propagation avant pour obtenir les activations sur les données d'entraînement
        activations_train = forward_propagation(X_train, parametres)
        gradients = back_propagation(y_train, parametres, activations_train)
        parametres = update(gradients, parametres, learning_rate)

        # Calcul du log loss et de l'accuracy pour les données d'entraînement
        Af_train = activations_train['A' + str(len(parametres) // 2)]
        training_history[i, 0] = log_loss(y_train.flatten(), Af_train.flatten())  # Log loss
        y_train_pred = predict(X_train, parametres)
        training_history[i, 2] = accuracy_score(y_train.flatten(), y_train_pred.flatten())  # Accuracy

        # Calcul du log loss et de l'accuracy pour les données de test
        activations_test = forward_propagation(X_test, parametres)
        Af_test = activations_test['A' + str(len(parametres) // 2)]
        training_history[i, 1] = log_loss(y_test.flatten(), Af_test.flatten())  # Log loss
        y_test_pred = predict(X_test, parametres)
        training_history[i, 3] = accuracy_score(y_test.flatten(), y_test_pred.flatten())  # Accuracy

    # Affichage des courbes de performance
    plt.figure(figsize=(12, 6))

    # Courbe de log loss
    plt.subplot(1, 2, 1)
    plt.plot(training_history[:, 0], label='Train Loss')
    plt.plot(training_history[:, 1], label='Test Loss')
    plt.xlabel('Iterations')
    plt.ylabel('Log Loss')
    plt.title('Log Loss')
    plt.legend()

    # Courbe de précision
    plt.subplot(1, 2, 2)
    plt.plot(training_history[:, 2], label='Train Accuracy')
    plt.plot(training_history[:, 3], label='Test Accuracy')
    plt.xlabel('Iterations')
    plt.ylabel('Accuracy')
    plt.title('Accuracy')
    plt.legend()

    plt.tight_layout()
    plt.show()

    return training_history


# Chargement des données et prétraitement (reshaping et normalisation)
X_train, y_train, X_test, y_test = load_data()

# Normalisation des données
X_train_reshape = X_train.reshape(X_train.shape[0], -1).T / X_train.max()
X_test_reshape = X_test.reshape(X_test.shape[0], -1).T / X_test.max()

# Entraînement du réseau de neurones
training_history = deep_neural_network(
    X_train_reshape, y_train, X_test_reshape, y_test, 
    hidden_layers=(8, 8, 8), learning_rate=0.01, n_iter=3000)