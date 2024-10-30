# Avant tout, importons les dependences
import openai
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from os import environ
from llama_index.readers.mongodb import SimpleMongoReader
from llama_index.core import VectorStoreIndex
from langchain_openai import ChatOpenAI 
from warnings import filterwarnings

# Ici, nous allons ignorer tous les avertissements (warnings)
filterwarnings("ignore")

# Pour des raisons de securite, nous allons charger nos identifiant de connection a MongoDB comme variable d'environnement (clé API OpenAI)
load_dotenv(find_dotenv())

# Et maintenant, nous allons nous athentifier aupres de OpenAI en donnant notre cle d'API
openai.api_key = environ["OPENAI_API_KEY"]

# Ici, nous definissons la fonction pour charger les données depuis MongoDB (tout en utilisant la fonctionalite de cache)
@st.cache_resource
def load_index_from_mongodb(host, port, db_name, collection_name):
    try:
        # Ici, nous creons une instance de la class "SimpleMongoReader" pour la lecture depuis MongoDB
        reader = SimpleMongoReader(host=host, port=port)

        # Et en suite, nous allons specifier les champs de donnees qui nous interessen
        field_names = ["categorie", "question", "reponse"]

        # Et maintenant, nous allons stocker tous les documents charges a partir de MongoDb dans une variable "documents"
        documents = reader.load_data(db_name=db_name, collection_name=collection_name, field_names=field_names)

        # Et enfin, nous retournons tous les documents extraits a partir de MongoDB
        return documents
    
    # Au cas, ou il y a une erreur
    except Exception as e:
        st.error(f"Erreur lors du chargement des données depuis MongoDB : {e}")
        return None

# Ici, nous definissons la fonction principale de l'interface utilisateur (Streamlit)
def main():
    # Ici, nous lisons une image de l'ECE a partir du dossier local "static"
    st.image("static/ece-ecole-ingenieurs.png")

    #########################################################################
    #st.subheader("HÔPITAL IMAGINAIRE SAINT-MICHEL", divider="rainbow")
    #st.markdown("## HÔPITAL IMAGINAIRE SAINT-MICHEL")
    ########################################################################

    # Ici, nous dennons un titre a l'interface utilisateur
    st.markdown("## HÔPITAL IMAGINAIRE SAINT-MICHEL")

    # Ici, nous ajoutons quelques styles (CSS) pour une interface utilisateur plus attirante (Rainbow Divider)
    st.markdown(
    """
        <hr style="border: none; height: 5px; background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);">
        """,
        unsafe_allow_html=True
    )

    #st.markdown("###### Cette application répond aux questions des patients.")

    # Ici, nous chargeons les donees a partir de MongoDB tout en specifiant l'adresse du serveur MongoDB, 
    # le port, la base de donnees et la collection
    host = "mongodb"
    port = 27017
    db_name = "hopital_saint_michel"
    collection_name = "connaissances"

    # Et maintenant, nous allons stocker tous les documents charges a partir de MongoDb dans une variable "documents"
    documents = load_index_from_mongodb(host, port, db_name, collection_name)

    if documents:
        # Si les documnets ont ete charges avec succes, nous allons créer un moteur de requête à partir des documents chargés
        index = VectorStoreIndex.from_documents(documents=documents)
        query_engine = index.as_query_engine()

        # Ici, nous creons une zone de texte pour la question de l'utilisateur (avec un message d'indication)
        user_question = st.text_input("Entrez votre question médicale ici :", placeholder="Ex: Est-ce que Docteur Romain sera disponible le 27 novembre 2024 à 10h ?")

        # Si l'utilisateur a saisi une question, nous alloons fait tout ce qui suit
        if user_question:
            try:
                # Nous allons d'abord interroger l'index pour récupérer les segments pertinents
                retrieved_response = query_engine.query(user_question)

                # Nousa llons apres onvertir la réponse en chaîne de caractères (string python)
                retrieved_chunks = str(retrieved_response)  
                # st.write(f"***Question utilisateur : _{user_question}_***")
                
                # Nous allons maintenant utiliser OpenAI pour générer une réponse finale basée sur la question et les informations récupérées
                llm = ChatOpenAI(model="gpt-4", openai_api_key=openai.api_key)

                # Ici, nous definissions le format du promt final (question finales) qui sera envoye au modele de OpenAI
                final_prompt = f"""
                Vous êtes un assistant médical compétent. En vous basant sur les informations suivantes récupérées de la base de données et sur la question de l'utilisateur, 
                générez une réponse complète et précise.

                Informations récupérées :
                {retrieved_chunks}

                Question de l'utilisateur :
                {user_question}
                """
                
                # Et en suite, nous allons envoyer le prompt final au modele de OpenAI et stocker la reponse du models dans une variable "llm_response"
                llm_response = llm.invoke(final_prompt)

                # Et maintenant, nous allons faire apparaitre un bouton "Obtenir la réponse" pour générer la réponse

                # Si l'utilisateur appuie sur le button "Obtenir la réponse"
                if st.button("Obtenir la réponse"):

                    # Nous allons afficher une titre "Réponse finale" en dessous duquel la reponse du modele OpenAI sera afficher
                    st.subheader("Réponse finale")

                    # Et finalement, nous allons afficher la reponse du modele OpenAI sur l'interface utilisateur
                    st.write(f"***{llm_response.content}***")

            except Exception as e:
                st.error(f"Erreur lors de l'interrogation de l'index : {e}")
        else:
            st.info("Veuillez saisir une question pour obtenir une réponse.")
    else:
        st.error("Les données n'ont pas pu être chargées depuis MongoDB.")

# Ici, nous faisons appel a la function principale de l'interface utilisateur pour son execution (Streamlit)
if __name__ == "__main__":
    main()
