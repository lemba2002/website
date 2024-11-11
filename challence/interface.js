import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import axios from 'axios';

const ExchangeRateList = () => {
  const [rates, setRates] = useState([]);

  useEffect(() => {
    fetchExchangeRates();
  }, []);

  const fetchExchangeRates = async () => {
    try {
      const response = await axios.get('https://GandyamPay.com/taux/refresh');
      setRates(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <FlatList
      data={rates}
      keyExtractor={(item) => item.id.toString()}
      renderItem={({ item }) => (
        <View style={styles.card}>
          <Text style={styles.serviceName}>{item.service_name}</Text>
          <Text style={styles.rate}>Rate: {item.rate}</Text>
        </View>
      )}
    />
  );
};

const styles = StyleSheet.create({
  card: { padding: 10, margin: 10, backgroundColor: '#fff', borderRadius: 8 },
  serviceName: { fontSize: 18, fontWeight: 'bold' },
  rate: { fontSize: 16 },
});

export default ExchangeRateList;
