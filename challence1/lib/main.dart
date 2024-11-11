import 'package:flutter/material.dart';
import 'dart:convert'; // Pour le décodage des données JSON
import 'package:http/http.dart' as http; // Pour envoyer des requêtes HTTP

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Taux de Change',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ExchangeRatesPage(),
    );
  }
}

class ExchangeRatesPage extends StatefulWidget {
  @override
  _ExchangeRatesPageState createState() => _ExchangeRatesPageState();
}

class _ExchangeRatesPageState extends State<ExchangeRatesPage> {
  bool isLoading = false;
  List<Map<String, dynamic>> exchangeRates = []; // Changer en liste
  final String apiUrl = "http://127.0.0.1:5000/taux"; // URL de l'API

  // Fonction pour récupérer les taux de change depuis l'API
  Future<void> fetchExchangeRates() async {
    setState(() {
      isLoading = true;
    });

    try {
      final response = await http.get(Uri.parse(apiUrl));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        // Vérification de la structure des données
        print('Données récupérées: $data');

        // Vérifier si les données sont une liste
        if (data is List) {
          setState(() {
            exchangeRates = List<Map<String, dynamic>>.from(data);
          });
        } else {
          setState(() {
            exchangeRates = [
              {"message": "Les données ne sont pas sous forme de liste."}
            ];
          });
        }
      } else {
        throw Exception("Erreur lors de la récupération des taux.");
      }
    } catch (e) {
      print("Erreur : $e");
      setState(() {
        exchangeRates = [
          {
            "message":
                "Impossible de récupérer les taux. Veuillez réessayer plus tard."
          }
        ];
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    fetchExchangeRates();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Taux de Change'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            isLoading
                ? CircularProgressIndicator()
                : ElevatedButton(
                    onPressed: fetchExchangeRates,
                    child: Text("Rafraîchir les Taux"),
                  ),
            SizedBox(height: 16),
            exchangeRates.isEmpty
                ? Center(child: Text('Aucun taux de change disponible'))
                : Expanded(
                    child: ListView.builder(
                      itemCount: exchangeRates.length,
                      itemBuilder: (context, index) {
                        var rate = exchangeRates[index];

                        return Card(
                          elevation: 5,
                          margin: EdgeInsets.symmetric(vertical: 8),
                          child: ListTile(
                            title: Text(
                              "1 ${rate['currency_from']} = ${rate['rate']} ${rate['currency_to']}",
                              style: TextStyle(fontWeight: FontWeight.bold),
                            ),
                          ),
                        );
                      },
                    ),
                  ),
          ],
        ),
      ),
    );
  }
}
