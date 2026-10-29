// ═══════════════════════════════════════════════════════════════════
//   market_dashboard / server.js – Akıllı Market Takip Sunucusu
//   Node.js 20+ Uyumlu, Sıfır Harici Paket Bağımlılığı (Zero-Dependency)
// ═══════════════════════════════════════════════════════════════════

const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { normalizeProduct } = require('./normalizer');

const PORT = process.env.PORT || 3030;
const DATA_FILE = path.join(__dirname, 'data', 'market_data.json');
const CSV_FILE = path.join(__dirname, 'data', 'market_data.csv');
const RECEIPTS_DIR = path.join(__dirname, 'public', 'receipts');

// Ensure directories exist
if (!fs.existsSync(path.join(__dirname, 'data'))) {
  fs.mkdirSync(path.join(__dirname, 'data'), { recursive: true });
}
if (!fs.existsSync(RECEIPTS_DIR)) {
  fs.mkdirSync(RECEIPTS_DIR, { recursive: true });
}

// MIME Types
const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.csv': 'text/csv; charset=utf-8'
};

// Data Helper Functions
function loadData() {
  try {
    if (fs.existsSync(DATA_FILE)) {
      const raw = fs.readFileSync(DATA_FILE, 'utf-8');
      return JSON.parse(raw);
    }
  } catch (err) {
    console.error('Error reading market_data.json:', err);
  }
  return [];
}

function saveData(items) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(items, null, 2), 'utf-8');
  
  // Also regenerate CSV
  const csvHeaders = ['ID', 'Tarih', 'Market', 'Ürün Adı', 'Marka', 'Kategori', 'Miktar', 'Birim Fiyat (€)', 'Toplam Fiyat (€)', 'KDV Grubu', 'Fiş No', 'Ödeyen'];
  const csvRows = items.map(it => [
    it.id,
    it.tarih,
    `"${(it.market || '').replace(/"/g, '""')}"`,
    `"${(it.urun || '').replace(/"/g, '""')}"`,
    `"${(it.marka || '').replace(/"/g, '""')}"`,
    `"${(it.kategori || '').replace(/"/g, '""')}"`,
    it.miktar,
    Number(it.birim_fiyat || 0).toFixed(2),
    Number(it.toplam_fiyat || 0).toFixed(2),
    `"${(it.kdv || '').replace(/"/g, '""')}"`,
    `"${(it.fis_no || '').replace(/"/g, '""')}"`,
    `"${(it.odeyen || 'Ortak').replace(/"/g, '""')}"`
  ].join(';'));

  const csvContent = '\uFEFF' + [csvHeaders.join(';'), ...csvRows].join('\r\n');
  fs.writeFileSync(CSV_FILE, csvContent, 'utf-8');
}

function getLocalIp() {
  const interfaces = os.networkInterfaces();
  for (const name of Object.keys(interfaces)) {
    for (const iface of interfaces[name]) {
      if (iface.family === 'IPv4' && !iface.internal) {
        return iface.address;
      }
    }
  }
  return 'localhost';
}

function readJsonBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > 25 * 1024 * 1024) { // 25MB max
        reject(new Error('Payload too large'));
      }
    });
    req.on('end', () => {
      try {
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        reject(err);
      }
    });
    req.on('error', reject);
  });
}

// Request Handler
const server = http.createServer(async (req, res) => {
  const parsedUrl = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const pathname = parsedUrl.pathname;
  const method = req.method;

  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // API Routes
  if (pathname === '/api/info' && method === 'GET') {
    const ip = getLocalIp();
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({
      success: true,
      port: PORT,
      ip: ip,
      localUrl: `http://localhost:${PORT}`,
      networkUrl: `http://${ip}:${PORT}`
    }));
    return;
  }

  // Check Receipt Duplicate Endpoint
  if (pathname === '/api/check-receipt' && method === 'GET') {
    const market = parsedUrl.searchParams.get('market') || '';
    const tarih = parsedUrl.searchParams.get('tarih') || '';
    const fis_no = (parsedUrl.searchParams.get('fis_no') || '').trim();

    if (!fis_no) {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ exists: false }));
      return;
    }

    const items = loadData();
    const existing = items.filter(it => 
      it.fis_no && 
      it.fis_no.toLowerCase() === fis_no.toLowerCase() &&
      (!market || it.market.toLowerCase() === market.toLowerCase()) &&
      (!tarih || it.tarih === tarih)
    );

    if (existing.length > 0) {
      const totalSum = existing.reduce((s, it) => s + (it.toplam_fiyat || 0), 0);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        exists: true,
        count: existing.length,
        totalSum: Number(totalSum.toFixed(2)),
        tarih: existing[0].tarih,
        market: existing[0].market,
        fis_no: existing[0].fis_no,
        fis_resmi: existing[0].fis_resmi || null,
        items: existing.map(it => it.urun)
      }));
      return;
    }

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ exists: false }));
    return;
  }

  if (pathname === '/api/data' && method === 'GET') {
    const items = loadData();
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({ success: true, items }));
    return;
  }

  // Export CSV
  if (pathname === '/api/export-csv' && method === 'GET') {
    if (fs.existsSync(CSV_FILE)) {
      const csv = fs.readFileSync(CSV_FILE);
      res.writeHead(200, {
        'Content-Type': 'text/csv; charset=utf-8',
        'Content-Disposition': 'attachment; filename="market_alisveris_verileri.csv"'
      });
      res.end(csv);
      return;
    } else {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'CSV file not found' }));
      return;
    }
  }

  // Add Single Item
  if (pathname === '/api/item' && method === 'POST') {
    try {
      const data = await readJsonBody(req);
      const items = loadData();
      const maxId = items.reduce((max, it) => Math.max(max, it.id || 0), 0);
      const norm = normalizeProduct(data.urun, data.marka, data.kategori);

      const newItem = {
        id: maxId + 1,
        tarih: data.tarih || new Date().toISOString().split('T')[0],
        market: data.market || 'Diğer',
        urun: data.urun || 'Ürün',
        kanonik_urun: norm.kanonik_urun,
        marka: data.marka || '',
        kategori: norm.kategori,
        alt_kategori: norm.alt_kategori,
        miktar: Number(data.miktar) || 1,
        birim_fiyat: Number(data.birim_fiyat) || 0,
        toplam_fiyat: Number(data.toplam_fiyat) || 0,
        kdv: data.kdv || 'B (7%)',
        fis_no: data.fis_no || '',
        fis_resmi: data.fis_resmi || null,
        odeyen: data.odeyen || 'Ortak'
      };
      items.unshift(newItem);
      saveData(items);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, item: newItem }));
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // Edit Item
  if (pathname.startsWith('/api/item/') && method === 'PUT') {
    try {
      const id = parseInt(pathname.split('/')[3], 10);
      const data = await readJsonBody(req);
      const items = loadData();
      const index = items.findIndex(it => it.id === id);
      if (index === -1) {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Item not found' }));
        return;
      }
      const norm = normalizeProduct(data.urun || items[index].urun, data.marka || items[index].marka, data.kategori || items[index].kategori);
      items[index] = { 
        ...items[index], 
        ...data, 
        kanonik_urun: norm.kanonik_urun,
        kategori: norm.kategori,
        alt_kategori: norm.alt_kategori,
        id 
      };
      saveData(items);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, item: items[index] }));
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // Delete Item
  if (pathname.startsWith('/api/item/') && method === 'DELETE') {
    try {
      const id = parseInt(pathname.split('/')[3], 10);
      let items = loadData();
      const prevLength = items.length;
      items = items.filter(it => it.id !== id);
      if (items.length === prevLength) {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Item not found' }));
        return;
      }
      saveData(items);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true }));
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // Batch Ingest New Receipt with Photo
  if (pathname === '/api/upload-receipt' && method === 'POST') {
    try {
      const payload = await readJsonBody(req);
      const receiptMeta = payload.receiptData || {};
      const fis_no = (receiptMeta.fis_no || '').trim();
      const items = loadData();

      // Duplicate Check Protection
      if (fis_no && !payload.allowDuplicate) {
        const existing = items.filter(it => 
          it.fis_no && 
          it.fis_no.toLowerCase() === fis_no.toLowerCase() &&
          (!receiptMeta.market || it.market.toLowerCase() === receiptMeta.market.toLowerCase()) &&
          (!receiptMeta.tarih || it.tarih === receiptMeta.tarih)
        );

        if (existing.length > 0) {
          const totalSum = existing.reduce((s, it) => s + (it.toplam_fiyat || 0), 0);
          res.writeHead(409, { 'Content-Type': 'application/json; charset=utf-8' });
          res.end(JSON.stringify({
            success: false,
            duplicate: true,
            error: 'Bu fiş daha önce sisteme yüklenmiş!',
            message: `${receiptMeta.tarih} tarihli ${receiptMeta.market} (Fiş #${fis_no}) daha önce ${existing.length} ürünle (€${totalSum.toFixed(2)}) sisteme kaydedilmiştir.`,
            existingCount: existing.length,
            existingTotal: Number(totalSum.toFixed(2))
          }));
          return;
        }
      }

      let imageRelPath = null;

      if (payload.receiptImageBase64) {
        const cleanBase64 = payload.receiptImageBase64.replace(/^data:image\/\w+;base64,/, '');
        const ext = payload.receiptFileName ? path.extname(payload.receiptFileName) || '.png' : '.png';
        const fileName = `receipt_${receiptMeta.tarih || 'date'}_${receiptMeta.fis_no || Date.now()}${ext}`;
        const filePath = path.join(RECEIPTS_DIR, fileName);
        fs.writeFileSync(filePath, Buffer.from(cleanBase64, 'base64'));
        imageRelPath = `/receipts/${fileName}`;
      }

      let maxId = items.reduce((max, it) => Math.max(max, it.id || 0), 0);
      const addedItems = [];

      if (Array.isArray(receiptMeta.items)) {
        for (const item of receiptMeta.items) {
          maxId++;
          const norm = normalizeProduct(item.urun, item.marka, item.kategori);
          const newItem = {
            id: maxId,
            tarih: receiptMeta.tarih || new Date().toISOString().split('T')[0],
            market: receiptMeta.market || 'Diğer',
            urun: item.urun || 'Ürün',
            kanonik_urun: norm.kanonik_urun,
            marka: item.marka || '',
            kategori: norm.kategori,
            alt_kategori: norm.alt_kategori,
            miktar: Number(item.miktar) || 1,
            birim_fiyat: Number(item.birim_fiyat) || 0,
            toplam_fiyat: Number(item.toplam_fiyat) || 0,
            kdv: item.kdv || 'B (7%)',
            fis_no: receiptMeta.fis_no || '',
            fis_resmi: imageRelPath,
            odeyen: receiptMeta.odeyen || 'Ortak'
          };
          items.unshift(newItem);
          addedItems.push(newItem);
        }
      }

      saveData(items);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        success: true,
        message: `${addedItems.length} ürün başarıyla eklendi!`,
        receiptImage: imageRelPath,
        addedItems
      }));
    } catch (err) {
      console.error(err);
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // Import CSV / Tabular Text
  if (pathname === '/api/import-data' && method === 'POST') {
    try {
      const payload = await readJsonBody(req);
      if (!Array.isArray(payload.items)) {
        throw new Error('Geçersiz veri biçimi. Items listesi bekleniyor.');
      }
      let items = loadData();
      if (payload.replace === true) {
        items = [];
      }
      let maxId = items.reduce((max, it) => Math.max(max, it.id || 0), 0);
      for (const it of payload.items) {
        maxId++;
        const norm = normalizeProduct(it.urun, it.marka, it.kategori);
        items.push({
          id: maxId,
          tarih: it.tarih,
          market: it.market,
          urun: it.urun,
          kanonik_urun: norm.kanonik_urun,
          marka: it.marka || '',
          kategori: norm.kategori,
          alt_kategori: norm.alt_kategori,
          miktar: Number(it.miktar) || 1,
          birim_fiyat: Number(it.birim_fiyat) || 0,
          toplam_fiyat: Number(it.toplam_fiyat) || 0,
          kdv: it.kdv || 'B (7%)',
          fis_no: it.fis_no || '',
          fis_resmi: it.fis_resmi || null,
          odeyen: it.odeyen || 'Ortak'
        });
      }
      saveData(items);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ success: true, count: payload.items.length }));
    } catch (err) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: err.message }));
    }
    return;
  }

  // Static File Serving
  let filePath = path.join(__dirname, 'public', pathname === '/' ? 'index.html' : pathname);

  // Security check: prevent directory traversal
  const normalizedPath = path.normalize(filePath);
  const publicDir = path.normalize(path.join(__dirname, 'public'));
  if (!normalizedPath.startsWith(publicDir)) {
    res.writeHead(403, { 'Content-Type': 'text/plain' });
    res.end('Forbidden');
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      res.end('404 Not Found');
      return;
    }

    const ext = path.extname(filePath).toLowerCase();
    const contentType = MIME_TYPES[ext] || 'application/octet-stream';

    res.writeHead(200, { 'Content-Type': contentType });
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, '0.0.0.0', () => {
  const localIp = getLocalIp();
  console.log(`\n======================================================`);
  console.log(`  🛒 MARKET ALIŞVERİŞİ & FİŞ DASHBOARD'U ÇALIŞIYOR!`);
  console.log(`======================================================`);
  console.log(`  👉 Bilgisayarından:   http://localhost:${PORT}`);
  console.log(`  📱 Telefondan / Ortak: http://${localIp}:${PORT}`);
  console.log(`======================================================\n`);
});
