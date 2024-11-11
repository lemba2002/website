import 'dart:convert';
import 'package:challence1/exchange_rate.dart';
import 'package:http/http.dart' as http;

class ApiService {
  // L'URL de l'API à récupérer
  static const String apiUrl = 'http://localhost:3000/taux';

  // Fonction pour récupérer les taux de change
  static Future<List<ExchangeRate>> fetchExchangeRates() async {
    try {
      final response = await http.get(Uri.parse(apiUrl));

      // Vérification du statut de la réponse HTTP
      if (response.statusCode == 200) {
        final data = json.decode(response.body);

        // Liste pour stocker les taux de change extraits
        List<ExchangeRate> rates = [];

        if (data.containsKey('rates')) {
          data['rates'].forEach((key, value) {
          
            final currencyPair = key; 
            final rate = value.toDouble(); // Le taux de change

            
            rates.add(ExchangeRate(
                currencyPair: currencyPair, rate: rate, currency: ''));
          });
        }

        return rates;
      } else {
        throw Exception('Failed to load exchange rates');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
