// ═══════════════════════════════════════════════════════════════════
//   normalizer.js – Akıllı Ürün & Kategori Normalizasyon Motoru
// ═══════════════════════════════════════════════════════════════════

function cleanProductText(text) {
  if (!text) return '';
  return text
    .replace(/\s*\(\d+[\.,]?\d*\s*kg\)/gi, '') // (0.540 kg), (1.308 kg)
    .replace(/\s*\d+[\.,]?\d*\s*kg\b/gi, '')    // 2.5kg, 1kg
    .replace(/\s*\d+\s*g\b/gi, '')              // 150g, 250g, 600g, 750g, 1000g
    .replace(/\s*\d+[\.,]?\d*\s*L\b/gi, '')     // 0.75L, 1.5L
    .replace(/\s*\d+\s*ml\b/gi, '')             // 650ml, 400ml
    .replace(/\s*\d+['’]?[l|l]ı\b/gi, '')       // 10'lu, 60'lı
    .replace(/\s*\d+\s*yıkama\b/gi, '')         // 40 Yıkama
    .replace(/\s*\d+\s*katlı\b/gi, '')          // 4 Katlı
    .replace(/\s*\d+\s*stk\b/gi, '')            // 3 Stk
    .trim();
}

function normalizeProduct(rawName, rawBrand, rawCategory) {
  const originalName = (rawName || '').trim();
  const lower = originalName.toLowerCase();
  const cleanName = cleanProductText(originalName);

  let canonical = cleanName;
  let masterCategory = 'Diğer';

  // 1. ET & TAVUK & ŞARKÜTERİ
  if ((lower.includes('tavuk') || lower.includes('hähnchen') || lower.includes('pute') || lower.includes('hindi')) && lower.includes('kıyma')) {
    canonical = 'Tavuk / Hindi Kıyma';
    masterCategory = 'Et, Tavuk & Şarküteri';
  } else if (lower.includes('kıyma') || lower.includes('rd-hackfleisch') || lower.includes('hackfleisch') || lower.includes('rinderhack')) {
    canonical = 'Dana Kıyma';
    masterCategory = 'Et, Tavuk & Şarküteri';
  } else if (lower.includes('tavuk') || lower.includes('hähnchen') || lower.includes('hindi') || lower.includes('pute') || lower.includes('fileto') || lower.includes('filet')) {
    canonical = 'Tavuk / Hindi Göğüs Fileto';
    masterCategory = 'Et, Tavuk & Şarküteri';
  } else if (lower.includes('köfte')) {
    canonical = 'Hazır Köfte Topları';
    masterCategory = 'Et, Tavuk & Şarküteri';
  } else if (lower.includes('finesse') || lower.includes('salam') || lower.includes('jambon') || lower.includes('saftschinken')) {
    canonical = 'Şarküteri (Salam / Jambon)';
    masterCategory = 'Et, Tavuk & Şarküteri';
  }

  // 2. SÜT, PEYNİR & YUMURTA
  else if (lower.includes('mitakos') || lower.includes('beyaz peynir') || lower.includes('süzme peynir') || lower.includes('weichkäs')) {
    canonical = 'Beyaz Peynir (Mitakos)';
    masterCategory = 'Süt, Peynir & Yumurta';
  } else if (lower.includes('emmental')) {
    canonical = 'Emmental Peyniri';
    masterCategory = 'Süt, Peynir & Yumurta';
  } else if (lower.includes('gouda')) {
    canonical = 'Gouda Peyniri';
    masterCategory = 'Süt, Peynir & Yumurta';
  } else if (lower.includes('cheddar')) {
    canonical = 'Cheddar Peyniri';
    masterCategory = 'Süt, Peynir & Yumurta';
  } else if (lower.includes('mozzarella')) {
    canonical = 'Mozzarella Peyniri';
    masterCategory = 'Süt, Peynir & Yumurta';
  } else if (lower.includes('yoğurt') || lower.includes('joghurt') || lower.includes('skyr')) {
    canonical = lower.includes('griech') || lower.includes('yunan') ? 'Yunan Yoğurdu' : 'Yoğurt';
    masterCategory = 'Süt, Peynir & Yumurta';
  } else if (lower.includes('tereyağ') || lower.includes('butter') || lower.includes('kerrygold')) {
    canonical = 'Tereyağı (Kerrygold)';
    masterCategory = 'Süt, Peynir & Yumurta';
  } else if (lower.includes('yumurta') || lower.includes('eier')) {
    canonical = 'Yumurta (10\'lu)';
    masterCategory = 'Süt, Peynir & Yumurta';
  } else if (lower.includes('krema') || lower.includes('sahne')) {
    canonical = 'Krema (H-Sahne)';
    masterCategory = 'Süt, Peynir & Yumurta';
  } else if (lower.includes('taze süt') || lower.includes('laktozsuz süt')) {
    canonical = 'İnek Sütü';
    masterCategory = 'Süt, Peynir & Yumurta';
  }

  // 3. İÇECEKLER
  else if (lower.includes('yulaf') || lower.includes('haferdr')) {
    canonical = 'Yulaf Sütü Barista';
    masterCategory = 'İçecekler';
  } else if (lower.includes('ayran')) {
    canonical = 'Ayran';
    masterCategory = 'İçecekler';
  } else if (lower.includes('şarap') || lower.includes('soave') || lower.includes('sauvignon') || lower.includes('pfalz')) {
    canonical = 'Şarap';
    masterCategory = 'İçecekler';
  } else if (lower.includes('bira') || lower.includes('hell') || lower.includes('augustiner')) {
    canonical = 'Bira (Hell)';
    masterCategory = 'İçecekler';
  } else if (lower.includes('spezi') || lower.includes('gazoz') || lower.includes('red bull') || lower.includes('enerji')) {
    canonical = 'Gazoz & Enerji İçeceği';
    masterCategory = 'İçecekler';
  }

  // 4. MEYVE & SEBZE
  else if (lower.includes('muz') || lower.includes('bananen') || lower.includes('chiquita')) {
    canonical = 'Muz';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('domates') && !lower.includes('passata') && !lower.includes('doğranmış')) {
    canonical = 'Domates';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('salatalık') || lower.includes('minigurken')) {
    canonical = 'Salatalık';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('patates') && !lower.includes('cips')) {
    canonical = 'Patates';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('biber')) {
    canonical = 'Biber';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('havuç') || lower.includes('karotten')) {
    canonical = 'Havuç';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('mantar')) {
    canonical = 'Kültür Mantarı';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('soğan') || lower.includes('sarımsak')) {
    canonical = 'Soğan & Sarımsak';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('şeftali') || lower.includes('ahududu')) {
    canonical = 'Taze Meyve';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('zucchini') || lower.includes('kabak')) {
    canonical = 'Kabak (Zucchini)';
    masterCategory = 'Meyve & Sebze';
  } else if (lower.includes('feldsalat') || lower.includes('salata') || lower.includes('kuzu kulağı')) {
    canonical = 'Yeşillik & Salata';
    masterCategory = 'Meyve & Sebze';
  }

  // 5. FIRIN & EKMEK
  else if (lower.includes('baget') || lower.includes('steinofenbag') || lower.includes('ekmek') || lower.includes('bagel') || lower.includes('lavaş') || lower.includes('laugenstange') || lower.includes('schnitte')) {
    canonical = lower.includes('baget') || lower.includes('steinofen') ? 'Taş Fırın Baget Ekmeği' :
                lower.includes('lavaş') ? 'Protein Lavaş' :
                lower.includes('laugenstange') ? 'Laugenstange (Simit)' : 'Ekmek & Fırın';
    masterCategory = 'Fırın & Ekmek';
  }

  // 6. DONDURULMUŞ & HAZIR YEMEK
  else if (lower.includes('pizza')) {
    canonical = 'Dondurulmuş Pizza';
    masterCategory = 'Dondurulmuş & Hazır Yemek';
  } else if (lower.includes('bezelye') || lower.includes('dondurulmuş')) {
    canonical = 'Dondurulmuş Sebze';
    masterCategory = 'Dondurulmuş & Hazır Yemek';
  }

  // 7. ATIŞTIRMALIK & TATLI
  else if (lower.includes('cips') || lower.includes('kartoffelchips')) {
    canonical = 'Patates Cipsi';
    masterCategory = 'Atıştırmalık & Tatlı';
  } else if (lower.includes('çikolata') || lower.includes('kinder') || lower.includes('milka') || lower.includes('choviva')) {
    canonical = 'Çikolata & Bar';
    masterCategory = 'Atıştırmalık & Tatlı';
  } else if (lower.includes('kek') || lower.includes('madlen')) {
    canonical = 'Kek & Bisküvi';
    masterCategory = 'Atıştırmalık & Tatlı';
  }

  // 8. KAHVALTILIK
  else if (lower.includes('nutella') || lower.includes('fındık kreması')) {
    canonical = 'Nutella / Fındık Kreması';
    masterCategory = 'Kahvaltılık';
  } else if (lower.includes('kahve') || lower.includes('dolce gusto')) {
    canonical = 'Kapsül Kahve';
    masterCategory = 'Kahvaltılık';
  } else if (lower.includes('müsli') || lower.includes('granola')) {
    canonical = 'Müsli & Granola';
    masterCategory = 'Kahvaltılık';
  } else if (lower.includes('tahin') || lower.includes('tahini')) {
    canonical = 'Tahin';
    masterCategory = 'Kahvaltılık';
  }

  // 9. TEMEL GIDA & MAKARNA
  else if (lower.includes('makarna') || lower.includes('fusilli') || lower.includes('rigatoni') || lower.includes('spag') || lower.includes('cornetti') || lower.includes('penne')) {
    canonical = 'Makarna';
    masterCategory = 'Temel Gıda & Makarna';
  } else if (lower.includes('kritharaki') || lower.includes('şehriye')) {
    canonical = 'Arpa Şehriye / Kritharaki';
    masterCategory = 'Temel Gıda & Makarna';
  } else if (lower.includes('pirinç') || lower.includes('mercimek') || lower.includes('fasulye') || lower.includes('bohnen')) {
    canonical = 'Bakliyat (Pirinç/Mercimek/Fasulye)';
    masterCategory = 'Temel Gıda & Makarna';
  } else if (lower.includes('un') || lower.includes('dinkel') || lower.includes('irmik') || lower.includes('hartweizen') || lower.includes('panko') || lower.includes('şeker')) {
    canonical = 'Un, İrmik & Şeker';
    masterCategory = 'Temel Gıda & Makarna';
  } else if (lower.includes('zeytinyağı') || lower.includes('sıvı yağ')) {
    canonical = 'Zeytinyağı / Sıvı Yağ';
    masterCategory = 'Temel Gıda & Makarna';
  } else if (lower.includes('leinsamen') || lower.includes('keten tohumu')) {
    canonical = 'Keten Tohumu';
    masterCategory = 'Temel Gıda & Makarna';
  }

  // 10. KONSERVE, SOS & BAHARAT
  else if (lower.includes('passata') || lower.includes('püre domates') || lower.includes('doğranmış domates')) {
    canonical = 'Domates Püresi / Passata';
    masterCategory = 'Konserve, Sos & Baharat';
  } else if (lower.includes('ketçap') || lower.includes('mayonez') || lower.includes('pesto') || lower.includes('soya sosu')) {
    canonical = 'Soslar (Ketçap / Mayonez / Pesto)';
    masterCategory = 'Konserve, Sos & Baharat';
  } else if (lower.includes('tuz') || lower.includes('kekik') || lower.includes('baharat') || lower.includes('sirke') || lower.includes('turşu')) {
    canonical = 'Tuz, Baharat & Sirke';
    masterCategory = 'Konserve, Sos & Baharat';
  }

  // 11. EV & TEMİZLİK
  else if (lower.includes('tuvalet kağıdı') || lower.includes('deterjan') || lower.includes('çöp torbası') || lower.includes('müllb') || lower.includes('temizlik') || lower.includes('bez') || lower.includes('kireç') || lower.includes('sprey') || lower.includes('klozet') || lower.includes('wc')) {
    canonical = lower.includes('tuvalet kağıdı') ? 'Tuvalet Kağıdı' :
                lower.includes('çöp') || lower.includes('müllb') ? 'Çöp Torbası' :
                lower.includes('deterjan') ? 'Çamaşır Deterjanı' : 'Temizlik & Hijyen';
    masterCategory = 'Ev & Temizlik';
  }

  // 12. KİŞİSEL BAKIM
  else if (lower.includes('duş jeli') || lower.includes('sabun') || lower.includes('diş') || lower.includes('pamuk') || lower.includes('listerine') || lower.includes('aseton')) {
    canonical = lower.includes('diş') ? 'Diş Bakımı' :
                lower.includes('duş') || lower.includes('sabun') ? 'Duş Jeli & Sabun' : 'Kişisel Bakım';
    masterCategory = 'Kişisel Bakım';
  }

  // 13. DEPOZİTO & DİĞER
  else if (lower.includes('pfand') || lower.includes('depozito')) {
    canonical = 'Depozito (Pfand)';
    masterCategory = 'Depozito';
  } else if (lower.includes('poşet') || lower.includes('tasche')) {
    canonical = 'Alışveriş Poşeti';
    masterCategory = 'Diğer';
  } else if (lower.includes('mum') || lower.includes('ampul') || lower.includes('sürahi') || lower.includes('brita') || lower.includes('kap')) {
    canonical = 'Ev & Mutfak Gereçleri';
    masterCategory = 'Ev & Mutfak Gereçleri';
  } else {
    // Fallback to reasonable category if provided
    if (rawCategory && rawCategory !== 'Diğer') {
      masterCategory = rawCategory;
    }
  }

  return {
    kanonik_urun: canonical,
    kategori: masterCategory,
    alt_kategori: rawCategory || masterCategory
  };
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { normalizeProduct, cleanProductText };
}
