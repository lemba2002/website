class ExchangeRate {
  final String currencyPair;
  final double rate;

  ExchangeRate({
    required this.currencyPair,
    required this.rate,
  });

  factory ExchangeRate.fromJson(Map<String, dynamic> json) {
    return ExchangeRate(
      currencyPair: json['currency_pair'] ?? 'Inconnu',
      rate: json['rate']?.toDouble() ?? 0.0,
    );
  }
}
