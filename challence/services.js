// service/rateService.js
const axios = require('axios');

async function getExchangeRatesFromServiceA() {
  const response = await axios.get('https://GandyamPay.com/taux');
  return response.data;
}
async function getExchangeRatesFromServicepostA() {
    const response = await axios.post('https://GandyamPay.com/taux/refresh ');
    return response.data;
  }

async function getExchangeRatesFromServiceB() {
  const response = await axios.get('https://www.taptapsend.com/taux');
  return response.data;
}

async function getExchangeRatesFromServicepostB() {
    const response = await axios.get('https://www.taptapsend.com/taux/refresh');
    return response.data;
  }

module.exports = {
  getExchangeRatesFromServiceA,
  getExchangeRatesFromServiceB,
  getExchangeRatesFromServicepostB,
  getExchangeRatesFromServicepostA,
};
