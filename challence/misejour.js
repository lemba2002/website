const cron = require('node-cron');
const rateService = require('services');

cron.schedule('0 * * * *', async () => {
  await rateService.updateExchangeRates();
  console.log("Taux de change mis à jour");
});
