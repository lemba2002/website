import json
import os

def store_data_in_json(data, filename='data.json'):
    # Vérifie si le fichier existe déjà
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            existing_data = json.load(file)
            existing_data.append(data)  # Ajoute les nouvelles données
    else:
        existing_data = [data]  # Crée une nouvelle liste avec les données

    # Sauvegarde les données dans le fichier JSON
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)
    print(f'Données enregistrées dans {filename}.')

# Exemple de données à stocker
data = {
    'currency_from': 'CAD',
    'rate': '439',
    'currency_to': 'CFA'
}

store_data_in_json(data)
