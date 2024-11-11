const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const { exec } = require('child_process');
const app = express();
const PORT = 3000;

// Connexion à la base de données SQLite
const db = new sqlite3.Database('./exchange_rates.db');

// Route GET : /taux - Retourne les taux de change stockés
app.get('/taux', (req, res) => {
    db.all("SELECT * FROM rates ORDER BY timestamp DESC", [], (err, rows) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ rates: rows });
    });
});

// Route POST : /taux/refresh - Exécute le script de scraping pour mettre à jour les taux
app.post('/taux/refresh', (req, res) => {
    exec('python3 scraping_script.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Erreur d'exécution : ${error.message}`);
            return res.status(500).json({ error: "Erreur lors de l'actualisation des taux." });
        }
        if (stderr) {
            console.error(`Erreur de script : ${stderr}`);
            return res.status(500).json({ error: "Erreur dans le script de scraping." });
        }
        res.json({ message: "Les taux de change ont été actualisés avec succès." });
    });
});

app.listen(PORT, () => {
    console.log(`Serveur en cours d'exécution sur http://localhost:${PORT}`);
});
