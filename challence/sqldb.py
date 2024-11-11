import sqlite3

# Créer une base de données SQLite (ou se connecter à une existante)
def save_data_to_db(data):
    conn = sqlite3.connect("exchange_rate.db")
    cursor = conn.cursor()
    
    # Créer une table si elle n'existe pas déjà
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rates (
        currency_from TEXT,
        rate TEXT,
        currency_to TEXT
    )
    ''')
    
    # Insérer les données
    cursor.execute('''
    INSERT INTO rates (currency_from, rate, currency_to)
    VALUES (?, ?, ?)
    ''', (data['currency_from'], data['rate'], data['currency_to']))
    
    # Valider les changements et fermer la connexion
    conn.commit()
    conn.close()
    print("Les données ont été sauvegardées dans la base de données.")

# Sauvegarder les données récupérées dans la base de données
if data:
    save_data_to_db(data)
