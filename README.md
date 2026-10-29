# 💑 Bizim Market Paneli – Grocery & Receipt Tracker (München 🥨)

Kız arkadaşınızla birlikte market alışverişlerini kontrol edebileceğiniz, kasa fişlerinin fotoğraflarını çekip dijitalleştirebileceğiniz, ortak bütçeyi anlık takip edebileceğiniz modern web ve mobil dashboard'u.

---

## 🌟 Öne Çıkan Özellikler

- **📸 Fiş Fotoğrafı Çekme / Yükleme:**
  - Telefonda doğrudan **arka kamerayı** açarak fişi masaya koyup anında çekme.
  - Bilgisayarda / laptopta **Canlı Kamera (Webcam)** vizörüyle kadraja hizalayıp çekme.
  - Dosyadan veya galeriden seçerek yükleme.
- **⚠️ "Bu Fişi Zaten Yüklediniz!" Mükerrer Kayıt Koruması:**
  - Fiş numarası veya tarihi yazıldığı anda veritabanını tarar; aynı fiş daha önce eklenmişse uyarı verir ve mükerrer harcama kaydını engeller.
- **🧠 Akıllı Kanonik Ürün & Kategori Normalizasyonu:**
  - Gramaj farkları (`600g`, `0.540 kg`, `1kg`) veya Almanca kasa kısaltmaları (`RD-Hackfleisch`, `Bananen`, `Mitakos Weichkäs`) ürünleri ayırmaz.
  - 14 temiz Master Kategoriye otomatik yönlendirir (örn: Tavuk kıyma, tavuk göğsü ve dana kıyma hepsi *Et, Tavuk & Şarküteri* altında toplanır).
- **📱 Sevgilimle Paylaş (QR Kod):**
  - Sağ üstteki butona tıklayınca açılan QR kodu telefon kamerasıyla taratarak uygulamayı saniyeler içinde mobilde açma.
- **🔍 Akıllı Fiyat Karşılaştırıcısı:**
  - Sık alınan ürünleri (Dana Kıyma, Yumurta, Yulaf Sütü, Muz, Tereyağı...) marketler arasında (PENNY, HIT, EDEKA, ALDI SÜD, dm...) kıyaslar ve en ucuz marketi gösterir.
- **💑 Ortak Bütçe & Ko-Kontrol:**
  - Aylık bütçe hedefi belirleme (örn. €450), harcanan tutar, kalan bakiye ve *Kim Ödedi?* (Ortak 50/50, Ben, Kız Arkadaşım) filtreleme.
- **📥/📤 Excel & CSV Desteği:**
  - Tek tıkla tüm verileri Excel (.xlsx) veya CSV olarak indirme veya yükleme.

---

## 🚀 Çalıştırma

### 1. Yerel Olarak Çalıştırma (Node.js)
```bash
npm start
# veya
node server.js
```
Tarayıcınızda açın:
- Bilgisayar: `http://localhost:3030`
- Telefon (aynı Wi-Fi): Terminalde gösterilen yerel IP (`http://192.168.x.x:3030`)

### 2. Streamlit Alternatifi
```bash
pip install -r requirements.txt
streamlit run app_streamlit.py
```

### 3. Bulutta 7/24 Canlıya Alma (Render / Railway / Vercel)
Bu repoyu [render.com](https://render.com) üzerine "Web Service" olarak bağladığınızda sıfır konfigürasyon ile doğrudan çalışır ve `https://bizim-market.onrender.com` gibi kalıcı bir link üretir.
