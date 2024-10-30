# Avant tout, importons les dependences
import openai
import streamlit as st
from dotenv import find_dotenv, load_dotenv
from os import environ
from langchain_openai import ChatOpenAI 
from warnings import filterwarnings

# Ici, nous allons ignorer tous les avertissements (warnings)
filterwarnings("ignore")

# Pour des raisons de securite, nous allons charger nos identifiant de connection a MongoDB comme variable d'environnement (clé API OpenAI)
load_dotenv(find_dotenv())

# Et maintenant, nous allons nous athentifier aupres de OpenAI en donnant notre cle d'API
openai.api_key = environ["OPENAI_API_KEY"]


# Ici, nous definissons la fonction principale de l'interface utilisateur (Streamlit)
def main():
    # Ici, nous lisons une image de l'ECE a partir du dossier local "static"
    st.image("static/ece-ecole-ingenieurs.png")

    #########################################################################
    #st.subheader("HÔPITAL IMAGINAIRE SAINT-MICHEL", divider="rainbow")
    #st.markdown("## HÔPITAL IMAGINAIRE SAINT-MICHEL")
    ########################################################################

    # Ici, nous dennons un titre a l'interface utilisateur
    st.markdown("### HÔPITAL IMAGINAIRE SAINT-MICHEL SANS RAG")

    # Ici, nous ajoutons quelques styles (CSS) pour une interface utilisateur plus attirante (Rainbow Divider)
    st.markdown(
    """
        <hr style="border: none; height: 5px; background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);">
        """,
        unsafe_allow_html=True
    )

 

    # Ici, nous creons une zone de texte pour la question de l'utilisateur (avec un message d'indication)
    user_question = st.text_input("Entrez votre question médicale ici :", placeholder="Ex: Est-ce que Docteur Romain sera disponible le 27 novembre 2024 à 10h ?")

        # Si l'utilisateur a saisi une question, nous alloons fait tout ce qui suit
    if user_question:
        try:
                
            # Nous allons maintenant utiliser OpenAI pour générer une réponse finale basée sur la question et les informations récupérées
            llm = ChatOpenAI(model="gpt-4", openai_api_key=openai.api_key)

            # Ici, nous definissions le format du promt final (question finales) qui sera envoye au modele de OpenAI
            final_prompt = f"""Vous êtes un assistant médical compétent. Veuillez générer une réponse complète et précise à la question posée.

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
            st.error(f"Erreur : \n{e}")
  

# Ici, nous faisons appel a la function principale de l'interface utilisateur pour son execution (Streamlit)
if __name__ == "__main__":
    main()
