class ExchangeRate {
  final String currency; // Devise (ex: USD, EUR)
  final double rate; // Taux de change
  final String currencyPair; // Le couple de devises (ex: USD-EUR)

  // Constructeur avec le couple de devises comme paramètre
  ExchangeRate({
    required this.currency,
    required this.rate,
    required this.currencyPair, // On le garde comme paramètre requis
  });

  // Factory pour créer un objet ExchangeRate à partir d'un JSON
  factory ExchangeRate.fromJson(Map<String, dynamic> json) {
    return ExchangeRate(
      currency:
          json['currency'] ?? 'Inconnu', // Valeur par défaut si non trouvée
      rate: json['rate']?.toDouble() ??
          0.0, // Convertion en double avec une valeur par défaut
      currencyPair: json['currency_pair'] ??
          'Inconnu', // On prend 'currency_pair' comme couple de devises, sinon 'Inconnu'
    );
  }
}
