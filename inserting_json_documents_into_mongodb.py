# Avant tout, importons les dependences
import json
from pymongo import MongoClient

# En suite, definissons nos identifiants de connexion à MongoDB
PROTOCOL: str = 'mongodb'
HOST: str = 'mongodb'
PORT: int = 27017


uri: str = f"{PROTOCOL}://{HOST}:{PORT}/"

# Declarons mainteant un client MongoClient qui va se connecter a notre base de donnees NOSQL MongoDB
client = MongoClient(uri)

# Nous pouvons verifier l'etat de la connexion au serveur MongoDB
# print(client.server_info())

# Definissons un nom de base donnees pour notre hopital imaginaire (Cette base de donnees sera cree par le serveur MongoDB si elle n'existe pas)
db = client["hopital_saint_michel"]

# Definissons une collection pour notre base de connaissance (knowledge base) (Cette collection sera cree par le serveur MongoDB si elle n'existe pas)
collection = db["connaissances"]


# Et maintenant, donnons la liste des fichiers JSON et leurs catégories associées respectives
files_and_categories = [
    ("./kb/01_informations_generales.json", "Informations générales"),
    ("./kb/02_pathologies_symptomes.json", "Pathologies et Symptômes"),
    ("./kb/03_medicaments_traitements.json", "Médicaments et Traitements"),
    ("./kb/04_preparation_consultations_interventions.json", "Préparation aux Consultations et Interventions"),
    ("./kb/05_suivi_apres_traitement.json", "Suivi après Traitement ou Intervention"),
    ("./kb/06_conseils_prevention.json", "Conseils de Prévention et de Santé Publique"),
    ("./kb/07_gestion_maladies_chroniques.json", "Gestion des Maladies Chroniques"),
    ("./kb/08_assistance_administrative.json", "Assistance Administrative et Logistique"),
    ("./kb/09_disponibilites_personnels_medicaux.json", "Disponibilités des personnels médicaux")
]


# En suite, nous allons definir une fonction pour insérer des données depuis un fichier JSON
def insert_data_from_json(file_path, category):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        # print(data)
        for item in data:
            document = {
                "categorie": category,
                "question": item.get("question"),
                "reponse": item.get("reponse"),
            }
            try:
                collection.insert_one(document)
            except Exception as e:
                print(f"Error inserting document: {e}")


# Et enfin, nous allons inserer tous nos fichiers JSON qui nous serviront comme base de connaissance
for file_name, category in files_and_categories:
    insert_data_from_json(file_name, category)

print("\n\nDonnées insérées avec succès dans MongoDB.\n\n")
# print(collection.find_one()) 
