import re
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from flask import Flask, jsonify # type: ignore

app = Flask(__name__)

# Nom du fichier JSON pour stocker les données
DATA_FILE = 'data.json'

# Fonction pour lire les données depuis le fichier JSON
def read_data_from_json():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # Si le fichier n'existe pas, retourner un dictionnaire vide
        return {}

# Fonction pour écrire les données dans le fichier JSON
def write_data_to_json(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Fonction pour récupérer les taux de change via Selenium
def scrape_with_selenium_taptap(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Pour ne pas afficher le navigateur
    service = Service('/usr/bin/chromedriver')  # Assurez-vous que le chemin est correct
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)

        # Récupérer le taux de change
        taux_element = driver.find_element(By.ID, "fxRateText")

        if taux_element:
            taux_text = taux_element.text.strip()  # Utilisation de .text pour récupérer le texte
            print(f"Taux récupéré : {taux_text}")
            
            # Expression régulière pour extraire les devises et le taux de change
            match = re.search(r'1\s([A-Za-z]+)\s?=\s?([\d,]+)\s([A-Za-z]+)', taux_text)

            if match:
                currency_from = match.group(1)  # Devise d'origine
                rate = match.group(2)  # Taux de change
                currency_to = match.group(3)  # Devise de destination

                # Affichage des résultats
                print(f"Taux de change : 1 {currency_from} = {rate} {currency_to}")
                
                # Mettre à jour les données dans le fichier JSON
                data = {
                    'currency_from': currency_from,
                    'rate': rate,
                    'currency_to': currency_to
                }
                write_data_to_json(data)
                return data

        # Si le taux de change n'a pas été trouvé
        else:
            print("Taux de change non trouvé.")
            return {}

    except Exception as e:
        print(f"Erreur lors de l'accès à {url}: {e}")
        return {}
    finally:
        driver.quit()


# Tester avec l'URL de taptapsend pour initialiser les taux
url = "https://www.taptapsend.com/"
scrape_with_selenium_taptap(url)

# Route GET pour récupérer les taux de change
@app.route('/taux', methods=['GET'])
def get_exchange_rates():
    data = read_data_from_json()
    if data:
        return jsonify(data)
    else:
        return jsonify({"message": "Les taux de change n'ont pas été rafraîchis."})

# Route POST pour rafraîchir les taux de change
@app.route('/taux/refresh', methods=['POST'])
def refresh_exchange_rates():
    # Rafraîchir les taux en exécutant à nouveau le scraping
    data = scrape_with_selenium_taptap("https://www.taptapsend.com/")
    
    if data:
        return jsonify({
            "message": "Taux de change rafraîchis avec succès!",
            "data": data
        })
    else:
        return jsonify({"message": "Erreur lors de la mise à jour des taux de change."})


if __name__ == '__main__':
    app.run(debug=True)
