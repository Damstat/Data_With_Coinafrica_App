# scraping_animaux.py
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get

def scraper_animaux(url_base, nb_pages):

    df = pd.DataFrame()

    for p in range(1, nb_pages + 1):
        url = f"{url_base}?page={p}"
        html = get(url)

        soup = bs(html.content, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')

        data_list = []
        for container in containers:
            try:
                nom = container.find('p', class_='ad__card-description').text.strip()

                # nettoyage du  clonne prix
                try:
                    prix_brut = container.find('p', class_='ad__card-price').text.strip()
                    prix_nettoye = prix_brut.replace("CFA", "").replace(" ", "").replace("\u202f", "")
                    prix = int(prix_nettoye)
                except:
                    prix = None

                adresse = container.find('p', class_='ad__card-location').span.text.strip()
                image_lien = container.find('img', class_='ad__card-img')['src']
                data_list.append({
                    "Nom": nom,
                    "Prix (CFA)": prix,
                    "Adresse": adresse,
                    "Lien image": image_lien
                })

            except:
                pass 

        DF = pd.DataFrame(data_list)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)

    return df
