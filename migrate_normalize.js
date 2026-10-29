const fs = require('fs');
const path = require('path');
const { normalizeProduct } = require('./normalizer');

const dataFile = path.join(__dirname, 'data', 'market_data.json');
const csvFile = path.join(__dirname, 'data', 'market_data.csv');
const dataJsFile = path.join(__dirname, 'public', 'data.js');

const raw = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
const updated = raw.map(it => {
  const norm = normalizeProduct(it.urun, it.marka, it.kategori);
  return {
    ...it,
    kanonik_urun: norm.kanonik_urun,
    alt_kategori: norm.alt_kategori,
    kategori: norm.kategori
  };
});

fs.writeFileSync(dataFile, JSON.stringify(updated, null, 2), 'utf-8');

// Update CSV
const csvHeaders = ['ID', 'Tarih', 'Market', 'Kanonik Ürün', 'Orijinal Ürün Adı', 'Marka', 'Kategori', 'Alt Kategori', 'Miktar', 'Birim Fiyat (€)', 'Toplam Fiyat (€)', 'KDV Grubu', 'Fiş No', 'Ödeyen'];
const csvRows = updated.map(it => [
  it.id,
  it.tarih,
  `"${(it.market || '').replace(/"/g, '""')}"`,
  `"${(it.kanonik_urun || '').replace(/"/g, '""')}"`,
  `"${(it.urun || '').replace(/"/g, '""')}"`,
  `"${(it.marka || '').replace(/"/g, '""')}"`,
  `"${(it.kategori || '').replace(/"/g, '""')}"`,
  `"${(it.alt_kategori || '').replace(/"/g, '""')}"`,
  it.miktar,
  Number(it.birim_fiyat || 0).toFixed(2),
  Number(it.toplam_fiyat || 0).toFixed(2),
  `"${(it.kdv || '').replace(/"/g, '""')}"`,
  `"${(it.fis_no || '').replace(/"/g, '""')}"`,
  `"${(it.odeyen || 'Ortak').replace(/"/g, '""')}"`
].join(';'));

fs.writeFileSync(csvFile, '\uFEFF' + [csvHeaders.join(';'), ...csvRows].join('\r\n'), 'utf-8');

// Update data.js
fs.writeFileSync(dataJsFile, 'window.INITIAL_MARKET_DATA = ' + JSON.stringify(updated) + ';', 'utf-8');

console.log(`Successfully normalized ${updated.length} items!`);
