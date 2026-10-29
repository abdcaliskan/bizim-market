// ═══════════════════════════════════════════════════════════════════
//   market_dashboard / app.js – İstemci Tarafı Yönetim & Analitik
// ═══════════════════════════════════════════════════════════════════

let allItems = [];
let filteredItems = [];
let currentPage = 1;
const pageSize = 20;

let timelineChartInstance = null;
let marketChartInstance = null;
let categoryChartInstance = null;
let vatChartInstance = null;
let comparatorChartInstance = null;

let selectedReceiptBase64 = null;
let selectedReceiptFileName = null;

let networkInfo = {
  ip: '192.168.0.173',
  networkUrl: 'http://192.168.0.173:3030',
  localUrl: 'http://localhost:3030'
};
let qrcodeInstance = null;
let duplicateCheckTimer = null;
let activeDuplicateReceipt = null;

// Supermarket Brand Color Map
const MARKET_COLORS = {
  'PENNY': '#cf0820',
  'HIT': '#e30613',
  'EDEKA': '#005ca9',
  'ALDI SÜD': '#002069',
  'dm': '#7b2b82',
  'tegut...': '#d97706',
  'Wolt Market': '#06b6d4',
  'Diğer': '#64748b'
};

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  if (window.lucide) {
    lucide.createIcons();
  }
  loadBudgetGoal();
  await fetchSystemInfo();
  await fetchData();
  renderPriceComparator();
  renderReceiptGallery();
});

// Fetch system network info for mobile sharing
async function fetchSystemInfo() {
  try {
    const res = await fetch('/api/info');
    if (res.ok) {
      const info = await res.json();
      if (info.success) {
        networkInfo = info;
        const shareEl = document.getElementById('shareNetworkUrl');
        if (shareEl) shareEl.textContent = info.networkUrl;
      }
    }
  } catch (err) {
    console.warn('System info alinamadi, varsayilan kullaniliyor.');
  }
}

// Load data from Backend API (with local fallback for standalone file:// mode)
async function fetchData() {
  try {
    const res = await fetch('/api/data');
    if (!res.ok) throw new Error('API response not ok');
    const json = await res.json();
    if (json.success && Array.isArray(json.items)) {
      allItems = json.items;
      populateCategoryDropdown();
      applyFilters();
      return;
    }
  } catch (err) {
    console.warn('API erisilemedi, yerel veri yukleniyor:', err);
  }

  // Fallback to embedded initial data
  if (window.INITIAL_MARKET_DATA && Array.isArray(window.INITIAL_MARKET_DATA)) {
    allItems = [...window.INITIAL_MARKET_DATA];
    populateCategoryDropdown();
    applyFilters();
  }
}

// Master Category List
const MASTER_CATEGORIES = [
  'Et, Tavuk & Şarküteri',
  'Meyve & Sebze',
  'Süt, Peynir & Yumurta',
  'Fırın & Ekmek',
  'Temel Gıda & Makarna',
  'Konserve, Sos & Baharat',
  'Kahvaltılık',
  'Atıştırmalık & Tatlı',
  'İçecekler',
  'Dondurulmuş & Hazır Yemek',
  'Ev & Temizlik',
  'Kişisel Bakım',
  'Depozito',
  'Diğer'
];

// Populate Category Filter Dropdown
function populateCategoryDropdown() {
  const categorySelect = document.getElementById('categoryFilter');
  const itemKategoriSelect = document.getElementById('itemKategori');
  
  categorySelect.innerHTML = '<option value="all">Tüm Kategoriler (' + MASTER_CATEGORIES.length + ')</option>';
  itemKategoriSelect.innerHTML = '';

  MASTER_CATEGORIES.forEach(cat => {
    const opt = document.createElement('option');
    opt.value = cat;
    opt.textContent = cat;
    categorySelect.appendChild(opt);

    const opt2 = document.createElement('option');
    opt2.value = cat;
    opt2.textContent = cat;
    itemKategoriSelect.appendChild(opt2);
  });
}

// Quick Market Pill Selector
function setMarketPill(market) {
  document.getElementById('marketFilter').value = market;
  document.querySelectorAll('.market-pill').forEach(btn => {
    btn.classList.remove('ring-2', 'ring-emerald-500', 'font-bold');
  });
  const activePill = document.getElementById(`pill-${market}`);
  if (activePill) {
    activePill.classList.add('ring-2', 'ring-emerald-500', 'font-bold');
  }
  applyFilters();
}

// Filter Logic
function applyFilters() {
  const query = (document.getElementById('searchInput').value || '').toLowerCase().trim();
  const dateOption = document.getElementById('dateFilter').value;
  const market = document.getElementById('marketFilter').value;
  const category = document.getElementById('categoryFilter').value;
  const payer = document.getElementById('payerFilter').value;

  filteredItems = allItems.filter(item => {
    // Search query
    if (query) {
      const match = (item.urun || '').toLowerCase().includes(query) ||
                    (item.marka || '').toLowerCase().includes(query) ||
                    (item.kategori || '').toLowerCase().includes(query) ||
                    (item.market || '').toLowerCase().includes(query) ||
                    (item.fis_no || '').toLowerCase().includes(query);
      if (!match) return false;
    }

    // Market filter
    if (market !== 'all' && item.market !== market) {
      return false;
    }

    // Category filter
    if (category !== 'all' && item.kategori !== category) {
      return false;
    }

    // Payer filter
    if (payer !== 'all' && (item.odeyen || 'Ortak') !== payer) {
      return false;
    }

    // Date filter
    if (dateOption === 'current_month') {
      if (!item.tarih.startsWith('2026-10')) return false;
    } else if (dateOption === 'prev_month') {
      if (!item.tarih.startsWith('2026-09')) return false;
    } else if (dateOption === 'last_7_days') {
      // items from 2026-10-22 to 2026-10-29
      const itemDate = new Date(item.tarih);
      const minDate = new Date('2026-10-22');
      if (itemDate < minDate) return false;
    }

    return true;
  });

  currentPage = 1;
  updateKPICards();
  renderCharts();
  renderTable();
  updateBudgetDisplay();
}

// Update KPI Cards
function updateKPICards() {
  const totalSpend = filteredItems.reduce((acc, it) => acc + (it.toplam_fiyat || 0), 0);
  document.getElementById('kpiTotalSpend').textContent = `€${totalSpend.toFixed(2)}`;
  document.getElementById('kpiItemCount').textContent = `${filteredItems.length} kalem ürün`;

  // October vs September calculation (from full allItems)
  const octSpend = allItems
    .filter(it => it.tarih && it.tarih.startsWith('2026-10'))
    .reduce((acc, it) => acc + (it.toplam_fiyat || 0), 0);
  const sepSpend = allItems
    .filter(it => it.tarih && it.tarih.startsWith('2026-09'))
    .reduce((acc, it) => acc + (it.toplam_fiyat || 0), 0);
  
  document.getElementById('kpiMonthSpend').textContent = `€${octSpend.toFixed(2)}`;
  document.getElementById('kpiMonthComp').textContent = `Eylül: €${sepSpend.toFixed(2)}`;

  // Distinct Receipts count
  const distinctReceipts = new Set(
    filteredItems.map(it => `${it.tarih}_${it.market}_${it.fis_no}`)
  );
  const receiptCount = distinctReceipts.size;
  document.getElementById('kpiReceiptCount').textContent = receiptCount;

  // Average Basket
  const avgBasket = receiptCount > 0 ? (totalSpend / receiptCount) : 0;
  document.getElementById('kpiAvgBasket').textContent = `€${avgBasket.toFixed(2)}`;

  // Top Supermarket by spend
  const marketMap = {};
  filteredItems.forEach(it => {
    marketMap[it.market] = (marketMap[it.market] || 0) + (it.toplam_fiyat || 0);
  });
  let topMarket = '-';
  let topMarketSpend = 0;
  Object.keys(marketMap).forEach(m => {
    if (marketMap[m] > topMarketSpend) {
      topMarketSpend = marketMap[m];
      topMarket = m;
    }
  });
  document.getElementById('kpiTopMarket').textContent = topMarket;
  const topPercent = totalSpend > 0 ? ((topMarketSpend / totalSpend) * 100).toFixed(0) : 0;
  document.getElementById('kpiTopMarketSpend').textContent = `€${topMarketSpend.toFixed(2)} (%${topPercent})`;

  // Pfand (Deposit) Balance
  const pfandItems = filteredItems.filter(it => 
    (it.kategori || '').toLowerCase().includes('depozito') || 
    (it.urun || '').toLowerCase().includes('pfand')
  );
  let pfandRefund = 0;
  let pfandPaid = 0;
  pfandItems.forEach(it => {
    if (it.toplam_fiyat < 0) {
      pfandRefund += Math.abs(it.toplam_fiyat);
    } else {
      pfandPaid += it.toplam_fiyat;
    }
  });
  const pfandNet = pfandRefund - pfandPaid;
  document.getElementById('kpiPfandNet').textContent = `${pfandNet >= 0 ? '+' : ''}€${pfandNet.toFixed(2)}`;
  document.getElementById('kpiPfandDetail').textContent = `İade: €${pfandRefund.toFixed(2)} | Ödenen: €${pfandPaid.toFixed(2)}`;
}

// Monthly Budget Logic
function loadBudgetGoal() {
  const saved = localStorage.getItem('monthly_budget_goal');
  const goal = saved ? parseFloat(saved) : 450;
  document.getElementById('budgetGoalInput').value = goal;
  document.getElementById('displayBudgetGoal').textContent = `€${goal.toFixed(2)}`;
}

function saveBudgetGoal() {
  const goal = parseFloat(document.getElementById('budgetGoalInput').value) || 450;
  localStorage.setItem('monthly_budget_goal', goal);
  document.getElementById('displayBudgetGoal').textContent = `€${goal.toFixed(2)}`;
  closeBudgetModal();
  updateBudgetDisplay();
}

function updateBudgetDisplay() {
  const saved = localStorage.getItem('monthly_budget_goal');
  const goal = saved ? parseFloat(saved) : 450;
  const octSpend = allItems
    .filter(it => it.tarih && it.tarih.startsWith('2026-10'))
    .reduce((acc, it) => acc + (it.toplam_fiyat || 0), 0);

  const percent = Math.min(100, Math.round((octSpend / goal) * 100));
  const remaining = goal - octSpend;

  document.getElementById('displayCurrentMonthSpend').textContent = `€${octSpend.toFixed(2)}`;
  document.getElementById('displayBudgetPercent').textContent = `%${percent}`;
  
  const progressBar = document.getElementById('budgetProgressBar');
  progressBar.style.width = `${percent}%`;

  if (percent > 90) {
    progressBar.className = 'h-full bg-gradient-to-r from-amber-500 to-rose-500 rounded-full transition-all duration-700';
  } else {
    progressBar.className = 'h-full bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full transition-all duration-700';
  }

  const remainingEl = document.getElementById('displayRemainingBudget');
  if (remaining >= 0) {
    remainingEl.innerHTML = `Kalan: <strong class="text-emerald-600">€${remaining.toFixed(2)}</strong>`;
  } else {
    remainingEl.innerHTML = `Aşıldı: <strong class="text-rose-600">-€${Math.abs(remaining).toFixed(2)}</strong>`;
  }
}

// Render Charts
function renderCharts() {
  renderTimelineChart();
  renderMarketChart();
  renderCategoryChart();
  renderVatChart();
}

// 1. Spending Over Time
function renderTimelineChart() {
  const dailySpendMap = {};
  filteredItems.forEach(it => {
    if (!it.tarih) return;
    dailySpendMap[it.tarih] = (dailySpendMap[it.tarih] || 0) + (it.toplam_fiyat || 0);
  });

  const sortedDates = Object.keys(dailySpendMap).sort();
  const seriesData = sortedDates.map(d => parseFloat(dailySpendMap[d].toFixed(2)));

  const options = {
    series: [{
      name: 'Günlük Harcama (€)',
      data: seriesData
    }],
    chart: {
      type: 'area',
      height: 270,
      fontFamily: 'Plus Jakarta Sans, sans-serif',
      toolbar: { show: false }
    },
    colors: ['#10b981'],
    fill: {
      type: 'gradient',
      gradient: {
        shadeIntensity: 1,
        opacityFrom: 0.45,
        opacityTo: 0.05,
        stops: [0, 95, 100]
      }
    },
    dataLabels: { enabled: false },
    stroke: { curve: 'smooth', width: 2.5 },
    xaxis: {
      categories: sortedDates.map(d => d.slice(5)), // MM-DD
      labels: { style: { colors: '#64748b', fontSize: '11px' } }
    },
    yaxis: {
      labels: {
        formatter: (val) => `€${val.toFixed(0)}`,
        style: { colors: '#64748b', fontSize: '11px' }
      }
    },
    tooltip: {
      y: { formatter: (val) => `€${val.toFixed(2)}` }
    },
    grid: { borderColor: '#f1f5f9' }
  };

  if (timelineChartInstance) {
    timelineChartInstance.destroy();
  }
  timelineChartInstance = new ApexCharts(document.querySelector("#timelineChart"), options);
  timelineChartInstance.render();
}

// 2. Market Breakdown
function renderMarketChart() {
  const marketMap = {};
  filteredItems.forEach(it => {
    marketMap[it.market] = (marketMap[it.market] || 0) + (it.toplam_fiyat || 0);
  });

  const labels = Object.keys(marketMap);
  const series = labels.map(m => parseFloat(marketMap[m].toFixed(2)));
  const colors = labels.map(m => MARKET_COLORS[m] || '#64748b');

  const options = {
    series: series,
    labels: labels,
    chart: {
      type: 'donut',
      height: 270,
      fontFamily: 'Plus Jakarta Sans, sans-serif'
    },
    colors: colors,
    legend: {
      position: 'bottom',
      fontSize: '11px',
      labels: { colors: '#475569' }
    },
    dataLabels: {
      enabled: true,
      formatter: (val) => `%${val.toFixed(0)}`
    },
    tooltip: {
      y: { formatter: (val) => `€${val.toFixed(2)}` }
    },
    plotOptions: {
      pie: {
        donut: {
          size: '65%',
          labels: {
            show: true,
            total: {
              show: true,
              label: 'Toplam',
              formatter: () => `€${series.reduce((a, b) => a + b, 0).toFixed(0)}`
            }
          }
        }
      }
    }
  };

  if (marketChartInstance) {
    marketChartInstance.destroy();
  }
  marketChartInstance = new ApexCharts(document.querySelector("#marketChart"), options);
  marketChartInstance.render();
}

// 3. Category Breakdown (Horizontal Bar)
function renderCategoryChart() {
  const catMap = {};
  filteredItems.forEach(it => {
    catMap[it.kategori] = (catMap[it.kategori] || 0) + (it.toplam_fiyat || 0);
  });

  const sortedCats = Object.keys(catMap).sort((a, b) => catMap[b] - catMap[a]).slice(0, 7);
  const seriesData = sortedCats.map(c => parseFloat(catMap[c].toFixed(2)));

  const options = {
    series: [{
      name: 'Harcama (€)',
      data: seriesData
    }],
    chart: {
      type: 'bar',
      height: 270,
      fontFamily: 'Plus Jakarta Sans, sans-serif',
      toolbar: { show: false }
    },
    plotOptions: {
      bar: {
        borderRadius: 6,
        horizontal: true,
        barHeight: '60%'
      }
    },
    colors: ['#8b5cf6'],
    dataLabels: {
      enabled: true,
      textAnchor: 'start',
      style: { colors: ['#fff'], fontSize: '10px' },
      formatter: (val) => `€${val.toFixed(1)}`,
      offsetX: 0
    },
    xaxis: {
      categories: sortedCats,
      labels: {
        formatter: (val) => `€${val.toFixed(0)}`,
        style: { colors: '#64748b', fontSize: '11px' }
      }
    },
    yaxis: {
      labels: { style: { colors: '#334155', fontSize: '11px', fontWeight: 500 } }
    },
    tooltip: {
      y: { formatter: (val) => `€${val.toFixed(2)}` }
    },
    grid: { borderColor: '#f1f5f9' }
  };

  if (categoryChartInstance) {
    categoryChartInstance.destroy();
  }
  categoryChartInstance = new ApexCharts(document.querySelector("#categoryChart"), options);
  categoryChartInstance.render();
}

// 4. VAT Distribution
function renderVatChart() {
  const vatMap = { 'B (%7 Gıda)': 0, 'A (%19 Genel)': 0, 'Diğer (%7)': 0 };
  filteredItems.forEach(it => {
    const kdv = (it.kdv || '').toUpperCase();
    if (kdv.includes('7') || kdv.includes('B')) {
      vatMap['B (%7 Gıda)'] += (it.toplam_fiyat || 0);
    } else if (kdv.includes('19') || kdv.includes('A')) {
      vatMap['A (%19 Genel)'] += (it.toplam_fiyat || 0);
    } else {
      vatMap['Diğer (%7)'] += (it.toplam_fiyat || 0);
    }
  });

  const labels = Object.keys(vatMap);
  const series = labels.map(k => parseFloat(vatMap[k].toFixed(2)));

  const options = {
    series: series,
    labels: labels,
    chart: {
      type: 'pie',
      height: 270,
      fontFamily: 'Plus Jakarta Sans, sans-serif'
    },
    colors: ['#10b981', '#f59e0b', '#06b6d4'],
    legend: {
      position: 'bottom',
      fontSize: '11px'
    },
    tooltip: {
      y: { formatter: (val) => `€${val.toFixed(2)}` }
    }
  };

  if (vatChartInstance) {
    vatChartInstance.destroy();
  }
  vatChartInstance = new ApexCharts(document.querySelector("#vatChart"), options);
  vatChartInstance.render();
}

// 5. Smart Price & Inflation Radar Comparator
function renderPriceComparator() {
  const selectEl = document.getElementById('comparatorSelect');
  
  // Populate options dynamically with canonical items
  if (!selectEl.dataset.initialized) {
    const popularKeys = [
      'Dana Kıyma',
      'Tavuk / Hindi Göğüs Fileto',
      'Yumurta (10\'lu)',
      'Yulaf Sütü Barista',
      'Muz',
      'Tereyağı (Kerrygold)',
      'Patates Cipsi',
      'Beyaz Peynir (Mitakos)',
      'Emmental Peyniri',
      'Yunan Yoğurdu',
      'Nutella / Fındık Kreması',
      'Makarna',
      'Dondurulmuş Pizza',
      'Ayran',
      'Kapsül Kahve',
      'Salatalık',
      'Havuç'
    ];
    selectEl.innerHTML = popularKeys.map(k => `<option value="${k}">${k}</option>`).join('');
    selectEl.dataset.initialized = 'true';
  }

  const selectedKey = selectEl.value;
  const matchingItems = allItems.filter(it => 
    (it.kanonik_urun && it.kanonik_urun.toLowerCase() === selectedKey.toLowerCase()) ||
    (it.urun || '').toLowerCase().includes(selectedKey.toLowerCase())
  );

  const container = document.getElementById('comparatorCards');
  if (matchingItems.length === 0) {
    container.innerHTML = `<div class="col-span-3 text-center py-6 text-slate-400">Bu ürünle ilgili henüz kayıt bulunamadı.</div>`;
    return;
  }

  // Find Min, Max, Avg unit prices
  let minPrice = Infinity;
  let minMarket = '';
  let maxPrice = -Infinity;
  let maxMarket = '';
  let sumPrice = 0;

  matchingItems.forEach(it => {
    const p = it.birim_fiyat || 0;
    if (p < minPrice && p > 0) {
      minPrice = p;
      minMarket = it.market;
    }
    if (p > maxPrice) {
      maxPrice = p;
      maxMarket = it.market;
    }
    sumPrice += p;
  });

  const avgPrice = sumPrice / matchingItems.length;
  const diffPercent = minPrice > 0 ? (((maxPrice - minPrice) / minPrice) * 100).toFixed(0) : 0;

  container.innerHTML = `
    <!-- Card 1: Lowest Price Store -->
    <div class="bg-emerald-950/40 border border-emerald-500/40 rounded-xl p-4 flex items-center justify-between">
      <div>
        <span class="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider">En Ucuz Market</span>
        <div class="text-xl font-extrabold text-white mt-0.5">${minMarket}</div>
        <div class="text-xs text-emerald-300 font-medium">Birim Fiyat: €${minPrice.toFixed(2)}</div>
      </div>
      <div class="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-lg">
        🏆
      </div>
    </div>

    <!-- Card 2: Highest Price Store -->
    <div class="bg-rose-950/40 border border-rose-500/40 rounded-xl p-4 flex items-center justify-between">
      <div>
        <span class="text-[11px] font-semibold text-rose-400 uppercase tracking-wider">En Pahalı Market</span>
        <div class="text-xl font-extrabold text-white mt-0.5">${maxMarket}</div>
        <div class="text-xs text-rose-300 font-medium">Birim Fiyat: €${maxPrice.toFixed(2)}</div>
      </div>
      <div class="w-10 h-10 rounded-xl bg-rose-500/20 text-rose-400 flex items-center justify-center text-lg">
        📈
      </div>
    </div>

    <!-- Card 3: Price Gap / Saving Opportunity -->
    <div class="bg-slate-800/80 border border-slate-700 rounded-xl p-4 flex items-center justify-between">
      <div>
        <span class="text-[11px] font-semibold text-amber-400 uppercase tracking-wider">Tasarruf Fırsatı</span>
        <div class="text-xl font-extrabold text-white mt-0.5">%${diffPercent} Fark</div>
        <div class="text-xs text-slate-300 font-medium">Ortalama Fiyat: €${avgPrice.toFixed(2)} (${matchingItems.length} alışveriş)</div>
      </div>
      <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg">
        💡
      </div>
    </div>
  `;

  // Render Comparator Mini Line Chart
  const sortedMatches = [...matchingItems].sort((a, b) => a.tarih.localeCompare(b.tarih));
  const chartDates = sortedMatches.map(it => `${it.tarih.slice(5)} (${it.market})`);
  const chartPrices = sortedMatches.map(it => it.birim_fiyat);

  const options = {
    series: [{
      name: 'Birim Fiyat (€)',
      data: chartPrices
    }],
    chart: {
      type: 'line',
      height: 200,
      fontFamily: 'Plus Jakarta Sans, sans-serif',
      toolbar: { show: false }
    },
    colors: ['#38bdf8'],
    stroke: { curve: 'straight', width: 3 },
    markers: { size: 5, colors: ['#0284c7'] },
    xaxis: {
      categories: chartDates,
      labels: { style: { colors: '#94a3b8', fontSize: '10px' } }
    },
    yaxis: {
      labels: {
        formatter: (val) => `€${val.toFixed(2)}`,
        style: { colors: '#94a3b8', fontSize: '10px' }
      }
    },
    tooltip: {
      theme: 'dark',
      y: { formatter: (val) => `€${val.toFixed(2)}` }
    },
    grid: { borderColor: '#334155' }
  };

  if (comparatorChartInstance) {
    comparatorChartInstance.destroy();
  }
  comparatorChartInstance = new ApexCharts(document.querySelector("#comparatorChart"), options);
  comparatorChartInstance.render();
}

// 6. Render Receipts Gallery
function renderReceiptGallery() {
  const container = document.getElementById('receiptGalleryContainer');
  
  // Find all distinct receipts with images
  const receiptCards = [
    {
      date: '2026-10-29',
      market: 'PENNY',
      receiptNo: '7965',
      total: '€27.08',
      itemCount: 8,
      img: '/receipts/receipt_2026-10-29_7965.png'
    },
    {
      date: '2026-10-28',
      market: 'PENNY',
      receiptNo: '7449',
      total: '€16.99',
      itemCount: 13,
      img: '/receipts/receipt_2026-10-28_7449.png'
    },
    {
      date: '2026-10-26',
      market: 'PENNY',
      receiptNo: '1053',
      total: '€17.40',
      itemCount: 7,
      img: '/receipts/receipt_2026-10-26_1053.png'
    },
    {
      date: '2026-10-26',
      market: 'PENNY',
      receiptNo: '5573',
      total: '€9.14',
      itemCount: 5,
      img: '/receipts/receipt_2026-10-26_5573.png'
    },
    {
      date: '2026-10-22',
      market: 'PENNY',
      receiptNo: '5950',
      total: '€5.27',
      itemCount: 3,
      img: '/receipts/receipt_2026-10-22_5950.png'
    }
  ];

  container.innerHTML = receiptCards.map(rc => `
    <div onclick="openLightbox('${rc.img}', '${rc.market} • ${rc.date} (Beleg #${rc.receiptNo}) - Toplam: ${rc.total}')" 
         class="group bg-slate-50 hover:bg-slate-100 rounded-xl p-2.5 border border-slate-200 transition-all cursor-pointer hover:shadow-md hover:border-emerald-300">
      <div class="relative overflow-hidden rounded-lg bg-slate-200 aspect-[3/4] mb-2 flex items-center justify-center">
        <img src="${rc.img}" class="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300" alt="Fiş ${rc.receiptNo}">
        <span class="absolute bottom-1.5 right-1.5 px-2 py-0.5 rounded text-[10px] font-bold bg-slate-900/80 text-white backdrop-blur-xs">
          ${rc.total}
        </span>
      </div>
      <div class="text-xs">
        <div class="flex items-center justify-between font-bold text-slate-800">
          <span class="text-red-700">${rc.market}</span>
          <span class="text-slate-400 font-normal text-[11px]">#${rc.receiptNo}</span>
        </div>
        <div class="flex justify-between items-center text-[11px] text-slate-500 mt-0.5">
          <span>${rc.date}</span>
          <span>${rc.itemCount} ürün</span>
        </div>
      </div>
    </div>
  `).join('');

  if (window.lucide) lucide.createIcons();
}

// 7. Render Detailed Items Table
function renderTable() {
  const tbody = document.getElementById('itemsTableBody');
  document.getElementById('tableFilterSummary').textContent = `Filtrelenen: ${filteredItems.length} ürün (Toplam ${allItems.length} kayıttan)`;

  const startIdx = (currentPage - 1) * pageSize;
  const pageItems = filteredItems.slice(startIdx, startIdx + pageSize);

  if (pageItems.length === 0) {
    tbody.innerHTML = `<tr><td colspan="12" class="text-center py-8 text-slate-400">Aradığınız kriterlere uygun kayıt bulunamadı.</td></tr>`;
    renderPagination(0);
    return;
  }

  tbody.innerHTML = pageItems.map(it => {
    const marketColor = it.market === 'PENNY' ? 'bg-red-50 text-red-700 border-red-200' :
                        it.market === 'HIT' ? 'bg-rose-50 text-rose-700 border-rose-200' :
                        it.market === 'EDEKA' ? 'bg-blue-50 text-blue-700 border-blue-200' :
                        it.market === 'ALDI SÜD' ? 'bg-indigo-50 text-indigo-700 border-indigo-200' :
                        it.market === 'dm' ? 'bg-purple-50 text-purple-700 border-purple-200' :
                        'bg-slate-100 text-slate-700 border-slate-200';

    const isNegative = it.toplam_fiyat < 0;
    const priceClass = isNegative ? 'text-emerald-600 font-bold' : 'text-slate-900 font-semibold';

    const receiptLink = it.fis_resmi ? `
      <button onclick="openLightbox('${it.fis_resmi}', '${it.market} Fişi #${it.fis_no}')" class="text-emerald-600 hover:text-emerald-800 hover:underline inline-flex items-center space-x-1" title="Fiş Fotoğrafını Gör">
        <span>${it.fis_no || '-'}</span>
        <i data-lucide="image" class="w-3 h-3 inline"></i>
      </button>
    ` : `<span>${it.fis_no || '-'}</span>`;

    return `
      <tr class="hover:bg-slate-50/80 transition-colors">
        <td class="py-2.5 px-4 whitespace-nowrap text-slate-600 font-mono text-[11px]">${it.tarih}</td>
        <td class="py-2.5 px-3 whitespace-nowrap">
          <span class="px-2 py-0.5 rounded-md border text-[11px] font-bold ${marketColor}">${it.market}</span>
        </td>
        <td class="py-2.5 px-3">
          <div class="font-bold text-slate-900">${it.kanonik_urun || it.urun}</div>
          ${it.kanonik_urun && it.kanonik_urun !== it.urun ? `<div class="text-[10px] text-slate-400 font-mono">${it.urun}</div>` : ''}
        </td>
        <td class="py-2.5 px-3 text-slate-500">${it.marka || '-'}</td>
        <td class="py-2.5 px-3">
          <span class="px-2 py-0.5 rounded-full bg-slate-100 text-slate-700 text-[10px] font-semibold border border-slate-200">${it.kategori || 'Diğer'}</span>
        </td>
        <td class="py-2.5 px-3 text-right font-mono text-slate-700">${it.miktar}</td>
        <td class="py-2.5 px-3 text-right font-mono text-slate-600">€${(it.birim_fiyat || 0).toFixed(2)}</td>
        <td class="py-2.5 px-3 text-right font-mono ${priceClass}">€${(it.toplam_fiyat || 0).toFixed(2)}</td>
        <td class="py-2.5 px-3 text-center text-slate-400 text-[11px]">${it.kdv || '-'}</td>
        <td class="py-2.5 px-3 text-center text-[11px]">${receiptLink}</td>
        <td class="py-2.5 px-3 text-center">
          <span class="px-2 py-0.5 rounded-full text-[10px] font-medium ${it.odeyen === 'Ben' ? 'bg-blue-100 text-blue-700' : it.odeyen === 'Kız Arkadaşım' ? 'bg-pink-100 text-pink-700' : 'bg-emerald-100 text-emerald-700'}">
            ${it.odeyen || 'Ortak'}
          </span>
        </td>
        <td class="py-2.5 px-4 text-center whitespace-nowrap">
          <button onclick="editItem(${it.id})" class="p-1 text-slate-400 hover:text-blue-600 transition-colors" title="Düzenle">
            <i data-lucide="edit-2" class="w-3.5 h-3.5"></i>
          </button>
          <button onclick="deleteItem(${it.id})" class="p-1 text-slate-400 hover:text-rose-600 transition-colors" title="Sil">
            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
          </button>
        </td>
      </tr>
    `;
  }).join('');

  renderPagination(filteredItems.length);
  if (window.lucide) lucide.createIcons();
}

// Pagination Controls
function renderPagination(totalCount) {
  const totalPages = Math.ceil(totalCount / pageSize);
  const startIdx = totalCount === 0 ? 0 : (currentPage - 1) * pageSize + 1;
  const endIdx = Math.min(currentPage * pageSize, totalCount);

  document.getElementById('paginationInfo').textContent = `Toplam ${totalCount} kayıttan ${startIdx}-${endIdx} arası`;

  const buttonsContainer = document.getElementById('paginationButtons');
  if (totalPages <= 1) {
    buttonsContainer.innerHTML = '';
    return;
  }

  let html = `
    <button onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:bg-slate-200"'} class="px-2 py-1 border border-slate-200 rounded text-slate-600">Önceki</button>
    <span class="px-2 text-slate-700 font-semibold">${currentPage} / ${totalPages}</span>
    <button onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled class="opacity-40 cursor-not-allowed"' : 'class="hover:bg-slate-200"'} class="px-2 py-1 border border-slate-200 rounded text-slate-600">Sonraki</button>
  `;
  buttonsContainer.innerHTML = html;
}

function changePage(page) {
  currentPage = page;
  renderTable();
}

// ========================================================
// RECEIPT UPLOAD MODAL & DUPLICATE DETECTION LOGIC
// ========================================================
function openReceiptUploadModal() {
  document.getElementById('newReceiptDate').value = new Date().toISOString().split('T')[0];
  document.getElementById('newReceiptMarket').value = 'PENNY';
  document.getElementById('newReceiptNo').value = '';
  document.getElementById('receiptLinesBody').innerHTML = '';
  document.getElementById('forceDuplicateCheck').checked = false;
  hideDuplicateWarning();
  clearReceiptImage();

  // Add 3 default blank rows to get started
  addReceiptLine();
  addReceiptLine();
  addReceiptLine();

  document.getElementById('receiptModal').classList.remove('hidden');
  if (window.lucide) lucide.createIcons();
}

function closeReceiptModal() {
  document.getElementById('receiptModal').classList.add('hidden');
  hideDuplicateWarning();
}

// Real-time Duplicate Receipt Detection
function onReceiptMetaChanged() {
  clearTimeout(duplicateCheckTimer);
  duplicateCheckTimer = setTimeout(() => {
    checkDuplicateReceipt();
  }, 250);
}

function checkDuplicateReceipt() {
  const fisNo = (document.getElementById('newReceiptNo').value || '').trim();
  const tarih = document.getElementById('newReceiptDate').value;
  const market = document.getElementById('newReceiptMarket').value;

  if (!fisNo) {
    hideDuplicateWarning();
    return;
  }

  // Look for match in allItems
  const matches = allItems.filter(it => 
    it.fis_no && 
    it.fis_no.toLowerCase() === fisNo.toLowerCase() &&
    (!market || it.market.toLowerCase() === market.toLowerCase()) &&
    (!tarih || it.tarih === tarih)
  );

  if (matches.length > 0) {
    const totalSum = matches.reduce((s, it) => s + (it.toplam_fiyat || 0), 0);
    activeDuplicateReceipt = {
      tarih: matches[0].tarih,
      market: matches[0].market,
      fis_no: matches[0].fis_no,
      count: matches.length,
      totalSum: totalSum.toFixed(2),
      fis_resmi: matches[0].fis_resmi || null
    };

    const warningEl = document.getElementById('duplicateWarningBox');
    const warningText = document.getElementById('duplicateWarningText');
    warningText.innerHTML = `
      <strong>${activeDuplicateReceipt.tarih}</strong> tarihli <strong>${activeDuplicateReceipt.market}</strong> (Fiş No: <strong>#${activeDuplicateReceipt.fis_no}</strong>) daha önce 
      <strong>${activeDuplicateReceipt.count} kalem ürün</strong> ile (toplam <strong>€${activeDuplicateReceipt.totalSum}</strong>) sisteme kaydedilmiş!
      <br><span class="text-xs text-amber-800">Mükerrer (çift) kayıt oluşturmamak için lütfen fişi kontrol ediniz.</span>
    `;
    warningEl.classList.remove('hidden');
  } else {
    hideDuplicateWarning();
  }
}

function hideDuplicateWarning() {
  activeDuplicateReceipt = null;
  const warningEl = document.getElementById('duplicateWarningBox');
  if (warningEl) warningEl.classList.add('hidden');
  const forceCheck = document.getElementById('forceDuplicateCheck');
  if (forceCheck) forceCheck.checked = false;
}

function previewExistingReceipt() {
  if (!activeDuplicateReceipt) return;
  if (activeDuplicateReceipt.fis_resmi) {
    openLightbox(activeDuplicateReceipt.fis_resmi, `${activeDuplicateReceipt.market} Fişi #${activeDuplicateReceipt.fis_no}`);
  } else {
    // Filter table by this receipt no
    closeReceiptModal();
    document.getElementById('searchInput').value = activeDuplicateReceipt.fis_no;
    applyFilters();
  }
}

function handleReceiptImageSelected(event) {
  const file = event.target.files[0];
  if (!file) return;

  selectedReceiptFileName = file.name;
  const reader = new FileReader();
  reader.onload = function(e) {
    selectedReceiptBase64 = e.target.result;
    document.getElementById('receiptImagePreview').src = selectedReceiptBase64;
    document.getElementById('receiptImagePreview').classList.remove('hidden');
    document.getElementById('dropzonePrompt').classList.add('hidden');
    document.getElementById('receiptImageRemoveBtn').classList.remove('hidden');
  };
  reader.readAsDataURL(file);
}

function clearReceiptImage() {
  selectedReceiptBase64 = null;
  selectedReceiptFileName = null;
  document.getElementById('receiptFileInput').value = '';
  document.getElementById('receiptImagePreview').classList.add('hidden');
  document.getElementById('receiptImagePreview').src = '';
  document.getElementById('dropzonePrompt').classList.remove('hidden');
  document.getElementById('receiptImageRemoveBtn').classList.add('hidden');
}

function onReceiptRowUrunInput(input) {
  const val = input.value.trim();
  if (!val) return;
  if (typeof normalizeProduct === 'function') {
    const norm = normalizeProduct(val);
    const tr = input.closest('tr');
    const catSelect = tr.querySelector('.row-cat');
    if (catSelect && norm.kategori) {
      catSelect.value = norm.kategori;
    }
  }
}

function addReceiptLine(defaultValues = {}) {
  const tbody = document.getElementById('receiptLinesBody');
  const tr = document.createElement('tr');
  tr.className = 'receipt-row hover:bg-slate-50 transition-colors';

  tr.innerHTML = `
    <td class="py-1.5 px-3">
      <input type="text" placeholder="Ürün adı" value="${defaultValues.urun || ''}" oninput="onReceiptRowUrunInput(this)" class="row-urun w-full px-2 py-1 text-xs border border-slate-200 rounded focus:ring-1 focus:ring-emerald-500">
    </td>
    <td class="py-1.5 px-2">
      <select class="row-cat w-full px-2 py-1 text-xs border border-slate-200 rounded focus:ring-1 focus:ring-emerald-500">
        ${MASTER_CATEGORIES.map(c => `<option value="${c}" ${defaultValues.kategori === c ? 'selected' : ''}>${c}</option>`).join('')}
      </select>
    </td>
    <td class="py-1.5 px-2">
      <input type="number" step="0.001" value="${defaultValues.miktar || 1}" oninput="calcModalLine(this)" class="row-qty w-full px-2 py-1 text-xs text-right border border-slate-200 rounded focus:ring-1 focus:ring-emerald-500">
    </td>
    <td class="py-1.5 px-2">
      <input type="number" step="0.01" value="${defaultValues.birim_fiyat || 0.00}" oninput="calcModalLine(this)" class="row-unit w-full px-2 py-1 text-xs text-right border border-slate-200 rounded focus:ring-1 focus:ring-emerald-500">
    </td>
    <td class="py-1.5 px-2">
      <input type="number" step="0.01" value="${defaultValues.toplam_fiyat || 0.00}" oninput="updateModalTotals()" class="row-total w-full px-2 py-1 text-xs text-right font-semibold text-emerald-700 border border-slate-200 rounded focus:ring-1 focus:ring-emerald-500">
    </td>
    <td class="py-1.5 px-2 text-center">
      <select class="row-kdv px-1.5 py-1 text-xs border border-slate-200 rounded">
        <option value="B (7%)">B (7%)</option>
        <option value="A (19%)">A (19%)</option>
      </select>
    </td>
    <td class="py-1.5 px-2 text-center">
      <button onclick="removeReceiptLine(this)" class="text-slate-400 hover:text-rose-600 p-1">
        <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
      </button>
    </td>
  `;

  tbody.appendChild(tr);
  updateModalTotals();
  if (window.lucide) lucide.createIcons();
}

function removeReceiptLine(btn) {
  btn.closest('tr').remove();
  updateModalTotals();
}

function calcModalLine(input) {
  const tr = input.closest('tr');
  const qty = parseFloat(tr.querySelector('.row-qty').value) || 0;
  const unit = parseFloat(tr.querySelector('.row-unit').value) || 0;
  const totalInput = tr.querySelector('.row-total');
  
  if (unit !== 0) {
    totalInput.value = (qty * unit).toFixed(2);
  }
  updateModalTotals();
}

function updateModalTotals() {
  const rows = document.querySelectorAll('.receipt-row');
  let sum = 0;
  let count = 0;

  rows.forEach(r => {
    const urun = r.querySelector('.row-urun').value.trim();
    const tot = parseFloat(r.querySelector('.row-total').value) || 0;
    if (urun || tot > 0) count++;
    sum += tot;
  });

  document.getElementById('modalLineCount').textContent = count;
  document.getElementById('modalTotalSum').textContent = `€${sum.toFixed(2)}`;
}

async function submitNewReceipt() {
  // DUPLICATE RECEIPT CHECK
  const isForceChecked = document.getElementById('forceDuplicateCheck').checked;
  if (activeDuplicateReceipt && !isForceChecked) {
    alert(`⚠️ DİKKAT: Bu fişi daha önce zaten yüklediniz!\n\n${activeDuplicateReceipt.tarih} tarihli ${activeDuplicateReceipt.market} (#${activeDuplicateReceipt.fis_no}) daha önce €${activeDuplicateReceipt.totalSum} (${activeDuplicateReceipt.count} ürün) ile sisteme kaydedilmiş.\n\nİki kez mükerrer harcama kaydetmemek için lütfen kontrol ediniz. Eğer bilerek tekrar eklemek istiyorsanız uyarı kutusundaki 'Yine de mükerrer olarak kaydet' seçeneğini işaretleyiniz.`);
    return;
  }

  const rows = document.querySelectorAll('.receipt-row');
  const itemsToAdd = [];

  rows.forEach(r => {
    const urun = r.querySelector('.row-urun').value.trim();
    if (!urun) return;
    const kategori = r.querySelector('.row-cat').value;
    const miktar = parseFloat(r.querySelector('.row-qty').value) || 1;
    const birim_fiyat = parseFloat(r.querySelector('.row-unit').value) || 0;
    const toplam_fiyat = parseFloat(r.querySelector('.row-total').value) || (miktar * birim_fiyat);
    const kdv = r.querySelector('.row-kdv').value;

    itemsToAdd.push({ urun, kategori, miktar, birim_fiyat, toplam_fiyat, kdv });
  });

  if (itemsToAdd.length === 0) {
    alert('Lütfen en az bir ürün kalemi giriniz!');
    return;
  }

  const payload = {
    allowDuplicate: isForceChecked,
    receiptImageBase64: selectedReceiptBase64,
    receiptFileName: selectedReceiptFileName,
    receiptData: {
      tarih: document.getElementById('newReceiptDate').value,
      market: document.getElementById('newReceiptMarket').value,
      fis_no: document.getElementById('newReceiptNo').value.trim(),
      odeyen: document.getElementById('newReceiptPayer').value,
      items: itemsToAdd
    }
  };

  try {
    const res = await fetch('/api/upload-receipt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    if (result.success) {
      closeReceiptModal();
      await fetchData();
      renderPriceComparator();
      renderReceiptGallery();
      alert(`🎉 Fiş başarıyla kaydedildi! (${itemsToAdd.length} ürün eklendi)`);
    } else if (result.duplicate) {
      alert(`⚠️ UYARI: ${result.message}\n\nMükerrer kayıt engellendi. Kaydetmek için 'Yine de mükerrer olarak kaydet' seçeneğini kullanabilirsiniz.`);
    } else {
      alert('Kayıt başarısız: ' + (result.error || 'Bilinmeyen hata'));
    }
  } catch (err) {
    console.error(err);
    alert('Sunucu hatası: ' + err.message);
  }
}

// ========================================================
// SHARE MODAL & QR CODE LOGIC (GIRLFRIEND MOBILE ACCESS)
// ========================================================
function openShareModal() {
  const modal = document.getElementById('shareModal');
  const targetUrl = networkInfo.networkUrl || `http://${location.hostname}:3030`;
  document.getElementById('shareNetworkUrl').textContent = targetUrl;

  const qrContainer = document.getElementById('qrcodeContainer');
  qrContainer.innerHTML = '';

  if (window.QRCode) {
    qrcodeInstance = new QRCode(qrContainer, {
      text: targetUrl,
      width: 170,
      height: 170,
      colorDark: '#0f172a',
      colorLight: '#ffffff',
      correctLevel: QRCode.CorrectLevel.M
    });
  } else {
    qrContainer.innerHTML = `<a href="${targetUrl}" target="_blank" class="text-xs text-emerald-600 underline font-mono">${targetUrl}</a>`;
  }

  modal.classList.remove('hidden');
  if (window.lucide) lucide.createIcons();
}

function closeShareModal(event) {
  document.getElementById('shareModal').classList.add('hidden');
}

function copyShareLink() {
  const targetUrl = document.getElementById('shareNetworkUrl').textContent;
  navigator.clipboard.writeText(targetUrl).then(() => {
    const btn = document.getElementById('copyShareBtn');
    btn.innerHTML = `<i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600"></i><span class="text-emerald-700">Kopyalandı!</span>`;
    if (window.lucide) lucide.createIcons();
    setTimeout(() => {
      btn.innerHTML = `<i data-lucide="copy" class="w-3.5 h-3.5"></i><span>Kopyala</span>`;
      if (window.lucide) lucide.createIcons();
    }, 2000);
  });
}

// ========================================================
// SINGLE ITEM QUICK ADD / EDIT MODAL LOGIC
// ========================================================
function onSingleItemUrunInput(input) {
  const val = input.value.trim();
  if (!val) return;
  if (typeof normalizeProduct === 'function') {
    const norm = normalizeProduct(val);
    const catSelect = document.getElementById('itemKategori');
    if (catSelect && norm.kategori) {
      catSelect.value = norm.kategori;
    }
  }
}

function openQuickItemModal() {
  document.getElementById('itemModalTitle').textContent = 'Yeni Ürün Ekle';
  document.getElementById('editItemId').value = '';
  document.getElementById('itemTarih').value = new Date().toISOString().split('T')[0];
  document.getElementById('itemMarket').value = 'PENNY';
  document.getElementById('itemUrun').value = '';
  document.getElementById('itemMarka').value = '';
  document.getElementById('itemFisNo').value = '';
  document.getElementById('itemMiktar').value = '1';
  document.getElementById('itemBirimFiyat').value = '0.00';
  document.getElementById('itemToplamFiyat').value = '0.00';
  document.getElementById('itemKdv').value = 'B (7%)';
  document.getElementById('itemOdeyen').value = 'Ortak';
  document.getElementById('itemModal').classList.remove('hidden');
}

function editItem(id) {
  const item = allItems.find(it => it.id === id);
  if (!item) return;

  document.getElementById('itemModalTitle').textContent = 'Ürünü Düzenle';
  document.getElementById('editItemId').value = item.id;
  document.getElementById('itemTarih').value = item.tarih;
  document.getElementById('itemMarket').value = item.market;
  document.getElementById('itemKategori').value = item.kategori;
  document.getElementById('itemUrun').value = item.urun;
  document.getElementById('itemMarka').value = item.marka || '';
  document.getElementById('itemFisNo').value = item.fis_no || '';
  document.getElementById('itemMiktar').value = item.miktar;
  document.getElementById('itemBirimFiyat').value = (item.birim_fiyat || 0).toFixed(2);
  document.getElementById('itemToplamFiyat').value = (item.toplam_fiyat || 0).toFixed(2);
  document.getElementById('itemKdv').value = item.kdv || 'B (7%)';
  document.getElementById('itemOdeyen').value = item.odeyen || 'Ortak';
  document.getElementById('itemModal').classList.remove('hidden');
}

function closeItemModal() {
  document.getElementById('itemModal').classList.add('hidden');
}

function calcItemTotal() {
  const qty = parseFloat(document.getElementById('itemMiktar').value) || 0;
  const unit = parseFloat(document.getElementById('itemBirimFiyat').value) || 0;
  document.getElementById('itemToplamFiyat').value = (qty * unit).toFixed(2);
}

async function submitItemForm(event) {
  event.preventDefault();
  const editId = document.getElementById('editItemId').value;
  const itemData = {
    tarih: document.getElementById('itemTarih').value,
    market: document.getElementById('itemMarket').value,
    kategori: document.getElementById('itemKategori').value,
    urun: document.getElementById('itemUrun').value.trim(),
    marka: document.getElementById('itemMarka').value.trim(),
    fis_no: document.getElementById('itemFisNo').value.trim(),
    miktar: parseFloat(document.getElementById('itemMiktar').value) || 1,
    birim_fiyat: parseFloat(document.getElementById('itemBirimFiyat').value) || 0,
    toplam_fiyat: parseFloat(document.getElementById('itemToplamFiyat').value) || 0,
    kdv: document.getElementById('itemKdv').value,
    odeyen: document.getElementById('itemOdeyen').value
  };

  try {
    const url = editId ? `/api/item/${editId}` : '/api/item';
    const method = editId ? 'PUT' : 'POST';

    const res = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(itemData)
    });
    const result = await res.json();
    if (result.success) {
      closeItemModal();
      await fetchData();
      renderPriceComparator();
    }
  } catch (err) {
    alert('Hata oluştu: ' + err.message);
  }
}

async function deleteItem(id) {
  if (!confirm('Bu ürünü silmek istediğinize emin misiniz?')) return;
  try {
    const res = await fetch(`/api/item/${id}`, { method: 'DELETE' });
    const result = await res.json();
    if (result.success) {
      await fetchData();
      renderPriceComparator();
    }
  } catch (err) {
    alert('Silinemedi: ' + err.message);
  }
}

// Lightbox Modal
function openLightbox(imgSrc, title) {
  document.getElementById('lightboxImage').src = imgSrc;
  document.getElementById('lightboxTitle').innerHTML = `
    <i data-lucide="receipt" class="w-4 h-4 text-emerald-400 mr-1.5"></i>
    <span>${title || 'Fiş Detayı'}</span>
  `;
  document.getElementById('lightboxDownloadBtn').href = imgSrc;
  document.getElementById('lightboxModal').classList.remove('hidden');
  if (window.lucide) lucide.createIcons();
}

function closeLightbox(event) {
  document.getElementById('lightboxModal').classList.add('hidden');
}

// Budget Modal
function openBudgetModal() {
  document.getElementById('budgetModal').classList.remove('hidden');
}
function closeBudgetModal() {
  document.getElementById('budgetModal').classList.add('hidden');
}

// Import Modal
function openImportModal() {
  document.getElementById('importModal').classList.remove('hidden');
}
function closeImportModal() {
  document.getElementById('importModal').classList.add('hidden');
}

async function executeImport() {
  const fileInput = document.getElementById('importFileInput');
  if (!fileInput.files || fileInput.files.length === 0) {
    alert('Lütfen bir dosya seçin!');
    return;
  }
  const file = fileInput.files[0];
  const replace = document.getElementById('importReplaceCheck').checked;

  const reader = new FileReader();
  reader.onload = async function(e) {
    try {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: 'array' });
      const firstSheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[firstSheetName];
      const jsonRows = XLSX.utils.sheet_to_json(worksheet, { header: 1 });

      if (jsonRows.length <= 1) {
        alert('Dosyada geçerli veri bulunamadı!');
        return;
      }

      // Convert rows to objects
      const importedItems = [];
      for (let i = 1; i < jsonRows.length; i++) {
        const r = jsonRows[i];
        if (!r || r.length < 3) continue;
        importedItems.push({
          tarih: r[1] || r[0] || '2026-10-29',
          market: r[2] || r[1] || 'Diğer',
          urun: r[3] || r[2] || 'Ürün',
          marka: r[4] || '',
          kategori: r[5] || 'Diğer',
          miktar: parseFloat(r[6]) || 1,
          birim_fiyat: parseFloat(r[7]) || 0,
          toplam_fiyat: parseFloat(r[8]) || 0,
          kdv: r[9] || 'B (7%)',
          fis_no: String(r[10] || ''),
          odeyen: r[11] || 'Ortak'
        });
      }

      const res = await fetch('/api/import-data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ items: importedItems, replace })
      });
      const result = await res.json();
      if (result.success) {
        closeImportModal();
        await fetchData();
        alert(`Başarıyla ${result.count} ürün içeri aktarıldı!`);
      }
    } catch (err) {
      alert('İçe aktarma hatası: ' + err.message);
    }
  };
  reader.readAsArrayBuffer(file);
}

// Export to Excel (XLSX)
function exportToExcel() {
  const exportData = filteredItems.map(it => ({
    'ID': it.id,
    'Tarih': it.tarih,
    'Market': it.market,
    'Ürün Adı': it.urun,
    'Marka': it.marka,
    'Kategori': it.kategori,
    'Miktar': it.miktar,
    'Birim Fiyat (€)': it.birim_fiyat,
    'Toplam Fiyat (€)': it.toplam_fiyat,
    'KDV Grubu': it.kdv,
    'Fiş No': it.fis_no,
    'Ödeyen': it.odeyen || 'Ortak'
  }));

  const worksheet = XLSX.utils.json_to_sheet(exportData);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Market Alışverişleri");
  XLSX.writeFile(workbook, "Market_Alisverisleri_Munih.xlsx");
}

// ========================================================
// LIVE CAMERA VIEWFINDER & DIRECT PHOTO CAPTURE
// ========================================================
let activeCameraStream = null;
let currentFacingMode = 'environment'; // 'environment' for rear camera, 'user' for front

async function openLiveCameraModal() {
  const modal = document.getElementById('cameraModal');
  modal.classList.remove('hidden');
  if (window.lucide) lucide.createIcons();

  await startCameraStream();
}

async function startCameraStream() {
  if (activeCameraStream) {
    stopCameraStream();
  }

  const video = document.getElementById('cameraVideo');
  try {
    const constraints = {
      video: {
        facingMode: { ideal: currentFacingMode },
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      },
      audio: false
    };

    activeCameraStream = await navigator.mediaDevices.getUserMedia(constraints);
    video.srcObject = activeCameraStream;
    await video.play();
  } catch (err) {
    console.warn('Canli kamera erisimi saglanamadi, dogrudan kamera inputuna yonlendiriliyor:', err);
    closeLiveCameraModal();
    // Trigger native camera capture input
    const nativeInput = document.getElementById('cameraInput');
    if (nativeInput) nativeInput.click();
  }
}

function stopCameraStream() {
  if (activeCameraStream) {
    activeCameraStream.getTracks().forEach(t => t.stop());
    activeCameraStream = null;
  }
}

function closeLiveCameraModal() {
  stopCameraStream();
  document.getElementById('cameraModal').classList.add('hidden');
}

function captureLivePhoto() {
  const video = document.getElementById('cameraVideo');
  const canvas = document.getElementById('cameraCanvas');
  
  if (!video.videoWidth || !video.videoHeight) {
    alert('Kamera görüntüsü henüz hazır değil, lütfen 1 saniye bekleyin.');
    return;
  }

  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  selectedReceiptBase64 = canvas.toDataURL('image/jpeg', 0.92);
  selectedReceiptFileName = `live_camera_${Date.now()}.jpg`;

  // Update UI preview
  const preview = document.getElementById('receiptImagePreview');
  preview.src = selectedReceiptBase64;
  preview.classList.remove('hidden');
  document.getElementById('dropzonePrompt').classList.add('hidden');
  document.getElementById('receiptImageRemoveBtn').classList.remove('hidden');

  closeLiveCameraModal();
}

async function toggleCameraFacing() {
  currentFacingMode = currentFacingMode === 'environment' ? 'user' : 'environment';
  await startCameraStream();
}
