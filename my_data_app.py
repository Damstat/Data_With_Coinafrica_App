import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from scraping_animaux import scraper_animaux
import altair as alt


url_chiens = "https://sn.coinafrique.com/categorie/chiens"
url_moutons = "https://sn.coinafrique.com/categorie/moutons"
url_lpl = "https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons"
url_autres ="https://sn.coinafrique.com/categorie/autres-animaux"


# Configuration de la page
st.set_page_config(page_title="Data Scraper Coinafrica App", layout="wide")

# Sidebar
st.sidebar.markdown("""
    <h2 style='color: #003366;
        font-size: 24px;
        text-align: center;
        font-weight: bold;'>
        Option Utilisateur
    </h2> """, unsafe_allow_html=True)

# Éléments interactifs

option = st.sidebar.selectbox(
    "Options",
    options=["Scraper avec BeautifulSoup", "Charger données Web Scraper", "visualisation des donees", "formulaire d'evaluation"]
    )


# Contenu principal

st.markdown("<h1 style='text-align: center; color: black;'>Scraper data with Coinafrica</h1>", unsafe_allow_html=True)
   
st.markdown("""
    <div style='text-align: center;'>
    <p>
    Cette application développée avec Streamlit permet de scraper, charger, visualiser et exporter des données
    d'annonces d'animaux depuis le site Coinafrique Sénégal.
    Elle s'adresse aux utilisateurs souhaitant collecter et analyser des données de marché sur les animaux domestiques en vente.
    Data source: <a href='https://sn.coinafrique.com'>Coinafrique</a>
     </p>

    </div>
    """, unsafe_allow_html=True)


if option == "Scraper avec BeautifulSoup":
    
    nb_pages = st.sidebar.selectbox("Nombre de pages à scraper", options=list(range(1, 200)), index=1)

    # contenaire centrer 
    st.subheader(" Sélection d'une catégorie à scraper")

    # Scraper les chiens
    if st.button("Scraper les chiens"):
        st.info(f"Scraping des chiens sur {nb_pages} en cours...")
        df_chiens = scraper_animaux(url_chiens, nb_pages)
        st.success(f"{len(df_chiens)} annonces récupérées")
        st.write('Data dimension: ' + str(df_chiens.shape[0]) + ' rows and ' + str(df_chiens.shape[1]) + ' columns.')
        st.dataframe(df_chiens)
        csv = df_chiens.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Télécharger CSV", data=csv, file_name="chiens.csv", mime='text/csv')

    # Scraper les moutons
    if st.button("Scraper les moutons"):
        st.info(f"Scraping des moutons sur {nb_pages} en cours...")
        df_moutons = scraper_animaux(url_moutons, nb_pages)
        st.success(f"{len(df_moutons)} annonces récupérées")
        st.write('Data dimension: ' + str(df_moutons.shape[0]) + ' rows and ' + str(df_moutons.shape[1]) + ' columns.')
        st.dataframe(df_moutons)
        csv = df_moutons.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Télécharger CSV", data=csv, file_name="moutons.csv", mime='text/csv')

    # Scraper lapin poule pigeon
    if st.button("Scraper lapin poules pigeon"):
        st.info(f"Scraping des lapin poule pigeon sur {nb_pages} en cours...")
        df_LPL = scraper_animaux(url_lpl, nb_pages)
        st.success(f"{len(df_LPL)} annonces récupérées")
        st.write('Data dimension: ' + str(df_LPL.shape[0]) + ' rows and ' + str(df_LPL.shape[1]) + ' columns.')
        st.dataframe(df_LPL)
        csv = df_LPL.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Télécharger CSV", data=csv, file_name="Poules_Lapins_Pigeons.csv", mime='text/csv')

    # Scraper autre animaux
    if st.button("Scraper autre animaux"):
        st.info(f"Scraping des autre animaux sur {nb_pages} en cours...")
        df_Autres_animaux = scraper_animaux(url_autres, nb_pages)
        st.success(f"{len(df_Autres_animaux)} annonces récupérées")
        st.write('Data dimension: ' + str(df_Autres_animaux.shape[0]) + ' rows and ' + str(df_Autres_animaux.shape[1]) + ' columns.')
        st.dataframe(df_Autres_animaux)
        csv = df_Autres_animaux.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Télécharger CSV", data=csv, file_name="animaux.csv", mime='text/csv')

        # Fin du conteneur

elif option == "Charger données Web Scraper":

    # Fonction de loading des données
    def load_(dataframe, title, key) :
    

        if st.button(title,key):
        
            st.subheader('Display data dimension')
            st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
            st.dataframe(dataframe)
            csv = dataframe.to_csv(index=False).encode('utf-8-sig')
            st.download_button("Télécharger CSV", data=csv, file_name=title+".csv", mime='text/csv')



            
    # Charger les données 
    load_(pd.read_csv('data/Donnees_chiens.csv'), 'Donnees sur les chiens', '1')
    load_(pd.read_csv('data/Donnees_moutons.csv'), 'Donnees sur les moutons', '2')
    load_(pd.read_csv('data/Donnees_plp.csv'), 'Donnees sur Poules / Lapins / Pigeons', '3')
    load_(pd.read_csv('data/Donnees_Autre_animaux.csv'), 'Donnees sur les autre animaux', '4')

elif option == "visualisation des donees":
    
    st.markdown("### Visualisation des données nettoyées")

    fichier = st.selectbox("Choisir une catégorie", 
                           options=["Chiens", "Moutons", "Poules / Lapins / Pigeons", "Autres animaux"])

    # Charger le fichier en fonction du choix
    if fichier == "Chiens":
        df = pd.read_csv("data/Donnees_chiens.csv")
    elif fichier == "Moutons":
        df = pd.read_csv("data/Donnees_moutons.csv")
    elif fichier == "Poules / Lapins / Pigeons":
        df = pd.read_csv("data/Donnees_plp.csv")
    elif fichier == "Autres animaux":
        df = pd.read_csv("data/Donnees_Autre_animaux.csv")

    # Affichage rapide et nettoyage
    st.write("###  Aperçu des données")
    df = df[["nom", "prix", "adresse","image_links-src"]]
    df.rename(columns={
        "nom": "Nom",
        "prix": "Prix (CFA)",
        "adresse": "Adresse",
        "image_links-src": "Lien image"
        }, inplace=True)
    
        # Nettoyer les prix : enlever "CFA", les espaces, les caractères parasites
    df["Prix (CFA)"] = df["Prix (CFA)"].astype(str)
    df["Prix (CFA)"] = df["Prix (CFA)"].str.replace("FCFA", "", regex=False)
    df["Prix (CFA)"] = df["Prix (CFA)"].str.replace("CFA", "", regex=False)
    df["Prix (CFA)"] = df["Prix (CFA)"].str.replace(" ", "", regex=False)

    #  Convertir en entier (si possible)
    df["Prix (CFA)"] = pd.to_numeric(df["Prix (CFA)"], errors='coerce') 
    st.dataframe(df.head())

    # Métriques résumées
    col1, col2, col3 = st.columns(3)
    col1.metric(" Prix Max", f"{df['Prix (CFA)'].max():,.0f} CFA")
    col2.metric(" Prix Min", f"{df['Prix (CFA)'].min():,.0f} CFA")
    col3.metric(" Prix Moyen", f"{df['Prix (CFA)'].mean():,.0f} CFA")

    st.markdown("---")

    # Répartition des annonces par lieu
    st.markdown("### Répartition des annonces par lieu")
    lieux_counts = df["Adresse"].value_counts().reset_index()
    lieux_counts.columns = ["Adresse", "Nombre"]

    chart_lieux = alt.Chart(lieux_counts).mark_bar().encode(
        x=alt.X("Nombre:Q", title="Nombre d'annonces"),
        y=alt.Y("Adresse:N", sort='-x'),
        color=alt.value("#1f77b4")
    ).properties(height=400)

    st.altair_chart(chart_lieux, use_container_width=True)

    # 🔹 Distribution des prix (histogramme)
    st.write("### Distribution des prix")
    hist = alt.Chart(df).mark_bar(color="#ff7f0e").encode(
        alt.X("Prix (CFA):Q", bin=alt.Bin(maxbins=30), title="Prix (CFA)"),
        y='count()'
    ).properties(height=400)

    st.altair_chart(hist, use_container_width=True)

    # 🔹 Prix moyen par lieu
    st.write("### Prix moyen par lieu")
    prix_par_ville = df.groupby("Adresse")["Prix (CFA)"].mean().reset_index().sort_values(by="Prix (CFA)", ascending=False)

    chart_prix_ville = alt.Chart(prix_par_ville).mark_bar().encode(
        x=alt.X("Prix (CFA):Q", title="Prix moyen (CFA)"),
        y=alt.Y("Adresse:N", sort='-x'),
        color=alt.value("#2ca02c")
    ).properties(height=400)

    st.altair_chart(chart_prix_ville, use_container_width=True)

    # 🔹 Noms les plus fréquents
    st.write("### Noms les plus fréquents")
    top_noms = df["Nom"].value_counts().head(10).reset_index()
    top_noms.columns = ["Nom", "Fréquence"]

    chart_noms = alt.Chart(top_noms).mark_bar().encode(
        x=alt.X("Fréquence:Q"),
        y=alt.Y("Nom:N", sort='-x'),
        color=alt.value("#d62728")
    ).properties(height=400)

    st.altair_chart(chart_noms, use_container_width=True)

    # 🔹 (Optionnel) Filtre par adresse
    st.write("### Filtrer les annonces par lieu")
    lieux_unique = df["Adresse"].dropna().unique()
    lieu_choisi = st.selectbox("Choisir une adresse", lieux_unique)

    df_filtré = df[df["Adresse"] == lieu_choisi]
    st.write(f"**{len(df_filtré)} annonces à {lieu_choisi} :**")
    st.dataframe(df_filtré.reset_index(drop=True))


else:
    components.html(""" 
         <div style="display: flex; justify-content: center;">
           

            <iframe src="https://ee.kobotoolbox.org/i/aDJsScKJ" width="800" height="1000"></iframe>
                    
        </div>


        """,
        height=1000,
    )




# Personnalisation avec le css

st.markdown("""
    <style>
    .main {
        background-image: url(""https://www.codewithrandom.com/wp-content/uploads/2022/10/Number-Guessing-Game-using-JavaScript-3.png"");
        color: black;
    }
    .stButton button {
        background-color: bold;
        color: black;
        font-weight: #FFFFFF ;
        width: 300px;
        height: 50px;
        border-radius: 10px;
    }
            
    /* Fond personnalisé de la barre lateral(siderbar) */
        section[data-testid="stSidebar"] {
        background-image: url("https://www.codewithrandom.com/wp-content/uploads/2022/10/Number-Guessing-Game-using-JavaScript-3.png");
      }

    /* Changer la couleur des titres et textes dans la sidebar */
        section[data-testid="stSidebar"] {
        color: bold ! important; 
        font-weight: #FFFFFF;
    }

    /* Facultatif : pour changer la couleur de fond des selectbox */
        section[data-testid="stSidebar"].stSelectbox {
        background-color: #FFFFFF;
        border-radius: 8px;
    }
            
     /* centrage des bonton et mise en forme */
     
    div.stButton {text-align:center}
            
    .stButton>button {
        font-size: 12px;
        height: 5em;
        width: 25em;
    }
            
    </style> """, unsafe_allow_html=True)





