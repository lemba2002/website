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
        return {}

# Fonction pour écrire les données dans le fichier JSON
def write_data_to_json(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Fonction pour récupérer les taux de change depuis Taptap
def scrape_with_selenium_taptap(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Pour ne pas afficher le navigateur
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)

        # Récupérer le taux de change
        taux_element = driver.find_element(By.ID, "fxRateText")

        if taux_element:
            taux_text = taux_element.text.strip()
            print(f"Taux récupéré de Taptap : {taux_text}")

            match = re.search(r'1\s([A-Za-z]+)\s?=\s?([\d,]+)\s([A-Za-z]+)', taux_text)

            if match:
                currency_from = match.group(1)
                rate = match.group(2)
                currency_to = match.group(3)

                data = {
                    'currency_from': currency_from,
                    'rate': rate,
                    'currency_to': currency_to
                }

                return data
        else:
            print("Taux de change non trouvé sur Taptap.")
            return {}

    except Exception as e:
        print(f"Erreur lors de l'accès à {url}: {e}")
        return {}
    finally:
        driver.quit()

# Fonction pour récupérer les taux de change depuis Transfergratis
def scrape_with_selenium_transfer(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Pour ne pas afficher le navigateur
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)

        frais_element = driver.find_element(By.XPATH, "//div[@class='form_row']//span[contains(text(), 'Frais totaux')]")
        taux_element = driver.find_element(By.XPATH, "//div[@class='form_row']//p[contains(text(), 'Le taux de change actuel')]")

        if frais_element and taux_element:
            frais_text = frais_element.text.strip()
            taux_text = taux_element.text.strip()

            print(f"Frais : {frais_text}")
            print(f"Taux récupéré de Transfergratis : {taux_text}")

            match = re.search(r'1([A-Za-z]+)=\s?([\d,]+)\s([A-Za-z]+)', taux_text)

            if match:
                currency_from = match.group(1)
                rate = match.group(2)
                currency_to = match.group(3)

                data = {
                    'currency_from': currency_from,
                    'rate': rate,
                    'currency_to': currency_to
                }

                return data
        else:
            print("Taux de change non trouvé sur Transfergratis.")
            return {}

    except Exception as e:
        print(f"Erreur lors de l'accès à {url}: {e}")
        return {}
    finally:
        driver.quit()

# Fonction pour rafraîchir les taux des deux sites
def refresh_exchange_rates():
    # Rafraîchir les taux pour les deux sites
    data_taptap = scrape_with_selenium_taptap("https://www.taptapsend.com/")
    data_transfer = scrape_with_selenium_transfer("https://transfergratis.com/")

    # Combiner les données dans un seul dictionnaire
    data = {
        'taptap': data_taptap,
        'transfergratis': data_transfer
    }

    # Écrire les nouvelles données dans le fichier JSON
    write_data_to_json(data)
    
    return data

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
def refresh_exchange_rates_route():
    data = refresh_exchange_rates()
    return jsonify({
        "message": "Taux de change rafraîchis avec succès!",
        "data": data
    })

if __name__ == '__main__':
    app.run(debug=True)
