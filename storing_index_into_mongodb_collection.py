# Avant tout, importons les dependences
from pymongo import MongoClient
from dotenv import find_dotenv, load_dotenv
from os import environ
import openai
# from langchain.chat_models import ChatOpenAI
from llama_index.core import VectorStoreIndex
from llama_index.readers.mongodb import SimpleMongoReader
# from IPython.display import Markdown, display

from warnings import filterwarnings

filterwarnings("ignore")

# Pour des raisons de securite, nous allons charger nos identifiant de connection a MongoDB comme variable d'environement
load_dotenv(find_dotenv())

# Et maintenant, nous allons nous athentifier aupres de OpenAI en donnant notre cle d'API
openai.api_key = environ.get(key="OPENAI_API_KEY")


# En suite, definissons nos identifiants de connexion à MongoDB
PROTOCOL: str = 'mongodb'
HOST: str = 'mongodb'
PORT: int = 27017

uri: str = f"{PROTOCOL}://{HOST}:{PORT}/"

# Declarons mainteant un client MongoClient qui va se connecter a notre base de donnees NOSQL MongoDB
client = MongoClient(uri)

# En suite, precisons le nom de base donnees a laquelle on veut se connecter 
db = client["hopital_saint_michel"]

# Definissons une collection pour les representations vectorielles de nos segments de texte (Cette collection sera cree par le serveur MongoDB si elle n'existe pas
embeddings_collection = db["embeddings"] 


# Precisons le nom de base donnees a laquelle on veut se connecter 
DATABASE = "hopital_saint_michel"

# Precisons le nom de collection a laquelle on veut se connecter (base de connaissance / knowledge base)
COLLECTION = "connaissances"


# Et en suite, nous allons specifier les champs de donnees qui nous interessent 
field_names = ["categorie", "question", "reponse"]

# Et miantenant, nous allons definir un object de la class "SimpleMongoReader" qui va aller consommer les documents sur MongoDB
reader = SimpleMongoReader("mongodb", 27017)

# Et maintenant, nous allons stocker tous les documents charges a partir de MongoDb dans une variable "documents"
documents = reader.load_data(DATABASE, COLLECTION, field_names)

# Et en suite, nous allons creer des segments (morceaux) de texte, des representation vectorielles et des indices (index)
index = VectorStoreIndex.from_documents(documents=documents)

# En suite, nous allons extraire les embeddings (representation vectorielles)
embeddings = index.storage_context.to_dict()

# En suite, nous allons sauvegarder les embeddings dans MongoDB
for doc_id, embedding in embeddings.items():
    embeddings_collection.insert_one({"_id": doc_id, "embedding": embedding})

# Nous allons maintenant tester nos indices (index) en les requettant avec une question
query_engine = index.as_query_engine()

# Maintenant, l'envoie de la question et la reception de la reponse
response = query_engine.query("Est ce que Docteur romain sera disponible le 27 Novembre 2024 a 10H ?")

# display(Markdown(f"<b>{response}</b>"))
print(f"\n\n{response}\n\n")
