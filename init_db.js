const fs = require('fs');
const path = require('path');

// Raw text data provided by user
const rawText = `2026-09-18	HIT	Şeftali	Jumbo / Manav	Meyve & Sebze	1	€1,99	€1,99	B (7%)	1701
2026-09-18	HIT	Kapsül Kahve	Nescafé Dolce Gusto	Kahve & Sıcak İçecek	1	€5,99	€5,99	B (7%)	1701
2026-09-18	HIT	Kapsül Kahve	Nescafé Dolce Gusto	Kahve & Sıcak İçecek	1	€5,99	€5,99	B (7%)	1701
2026-09-18	HIT	Doğranmış Domates	REWE	Konserve & Sos	1	€1,29	€1,29	B (7%)	1701
2026-09-18	HIT	Makarna (Penne)	Delverde	Kuru Gıda & Makarna	2	€1,89	€3,78	B (7%)	1701
2026-09-18	HIT	Salam / Şarküteri	WSH HIT Klassik	Şarküteri & Et	1	€3,65	€3,65	B (7%)	1701
2026-09-18	HIT	Yulaf Sütü (Haferdrink)	Daily	İçecek & Süt	1	€1,79	€1,79	A (19%)	1701
2026-09-18	HIT	Beyaz Şarap (Pfalz Sauvignon)	GW Pfalz	İçecek & Alkol	1	€3,29	€3,29	A (19%)	1701
2026-09-18	HIT	Leke Çıkarıcı / Temizleyici	Dr. Beckmann	Ev & Temizlik	1	€2,45	€2,45	A (19%)	1701
2026-09-18	HIT	Banyo Temizleyici Sprey	Cillit Bang	Ev & Temizlik	1	€2,99	€2,99	A (19%)	1701
2026-09-18	HIT	Yağ Çözücü Sprey	Cillit Bang	Ev & Temizlik	1	€2,99	€2,99	A (19%)	1701
2026-09-18	HIT	Klozet Bloğu	WC Frisch	Ev & Temizlik	1	€3,29	€3,29	A (19%)	1701
2026-09-18	HIT	WC Temizleyici Jel	Sagrotan	Ev & Temizlik	1	€3,49	€3,49	A (19%)	1701
2026-09-18	HIT	Tuvalet Kağıdı	Zewa	Temizlik & Kağıt	1	€5,99	€5,99	A (19%)	1701
2026-09-18	HIT	Çöp Torbası 5L	Ivi	Ev & Mutfak	1	€0,85	€0,85	A (19%)	1701
2026-09-18	HIT	Sünger Bez	QM	Ev & Temizlik	1	€0,45	€0,45	A (19%)	1701
2026-09-18	HIT	Nemli Temizlik Bezi	Manschgler	Ev & Temizlik	1	€1,25	€1,25	A (19%)	1701
2026-09-18	HIT	Kokulu Çöp Torbası	Ivi	Ev & Mutfak	1	€1,79	€1,79	A (19%)	1701
2026-09-18	HIT	LED Mum / Ampul 470lm	HIT	Ev Gereçleri	1	€4,99	€4,99	A (19%)	1701
2026-09-18	HIT	Depozito İadesi (Pfand)	Pfand	Depozito	7	-€0,25	-€1,75	A (19%)	1701
2026-09-20	EDEKA	Yoğurt	Körfez	Süt Ürünleri	1	€2,99	€2,99	A (7%)	5846
2026-09-20	EDEKA	Bira (Hell)	Augustiner	İçecek & Alkol	2	€1,79	€3,58	B (19%)	5846
2026-09-20	EDEKA	Şişe Depozitosu (Pfand)	Pfand	Depozito	2	€0,08	€0,16	B (19%)	5846
2026-09-20	EDEKA	Dana Kıyma	EDEKA	Et & Tavuk	1	€6,99	€6,99	A (7%)	5846
2026-09-20	EDEKA	Kültür Mantarı	Gut & Günstig	Meyve & Sebze	1	€2,49	€2,49	A (7%)	5846
2026-09-20	EDEKA	Kuru Sarımsak	Manav	Meyve & Sebze	1	€1,99	€1,99	A (7%)	5846
2026-09-20	EDEKA	Soğan (0.540 kg)	Manav	Meyve & Sebze	0,54	€3,99	€2,15	A (7%)	5846
2026-09-20	dm	Mikrofiber Temizlik Bezi	Vileda	Temizlik & Ev	1	€4,65	€4,65	1 (19%)	3073
2026-09-20	dm	Islak Yer Bezi	Swiffer	Temizlik & Ev	1	€2,45	€2,45	1 (19%)	3073
2026-09-20	dm	Renkliler İçin Sıvı Deterjan	Denkmit	Temizlik & Çamaşır	1	€3,15	€3,15	1 (19%)	3073
2026-09-20	dm	Siyahlar İçin Sıvı Deterjan 40 Yıkama	Denkmit	Temizlik & Çamaşır	1	€2,15	€2,15	1 (19%)	3073
2026-09-20	dm	Kireç Önleyici Tablet 60'lı	Denkmit	Temizlik & Çamaşır	1	€3,25	€3,25	1 (19%)	3073
2026-09-20	dm	Organik Pamuk Ped 60'lı	ebelin	Kişisel Bakım	1	€0,95	€0,95	1 (19%)	3073
2026-09-20	dm	Zeytin Özlü Duş Jeli 650ml	Palmolive	Kişisel Bakım	1	€2,95	€2,95	1 (19%)	3073
2026-09-21	tegut...	Rendelenmiş Mozzarella	tegut...	Süt Ürünleri	1	€1,79	€1,79	C (7%)	2206
2026-09-21	tegut...	Patates Cipsi	funny-frisch	Atıştırmalık & Cips	1	€1,99	€1,99	C (7%)	2206
2026-09-21	tegut...	Madlen Kek	Ibis	Fırın & Atıştırmalık	1	€1,99	€1,99	C (7%)	2206
2026-09-21	tegut...	Organik Muz (0.888 kg)	tegut... Bio	Meyve & Sebze	1	€1,99	€1,77	C (7%)	2206
2026-09-23	PENNY	Organik Patates	Penny Bio	Meyve & Sebze	1	€1,99	€1,99	B (7%)	2933
2026-09-23	PENNY	Kafes Yumurta 10'lu	Penny	Şarküteri & Yumurta	1	€4,19	€4,19	B (7%)	2933
2026-09-23	PENNY	Yulaf Sütü Barista	Naturgut	İçecek & Süt	2	€2,55	€5,10	A (19%)	2933
2026-09-23	PENNY	Krema %12 (H-Sahne)	Penny	Süt Ürünleri	2	€0,59	€1,18	B (7%)	2933
2026-09-23	PENNY	Burgu Makarna (Fusilli)	Bernbacher	Kuru Gıda & Makarna	1	€1,79	€1,79	B (7%)	2933
2026-09-23	PENNY	Boru Makarna (Rigatoni)	Bernbacher	Kuru Gıda & Makarna	1	€1,79	€1,79	B (7%)	2933
2026-09-23	PENNY	Müsli	Naturgut	Kahvaltılık	1	€1,99	€1,99	B (7%)	2933
2026-09-23	PENNY	Ketçap	Heinz	Sos & Baharat	1	€2,79	€2,79	B (7%)	2933
2026-09-23	PENNY	Mayonez	Heinz / Penny	Sos & Baharat	1	€2,79	€2,79	B (7%)	2933
2026-09-23	PENNY	Diş Fırçası	Today Dent / Penny	Kişisel Bakım	1	€0,65	€0,65	A (19%)	2933
2026-09-24	PENNY	Salkım Domates (0.440 kg)	Manav	Meyve & Sebze	0,44	€2,89	€1,27	B (7%)	3938
2026-09-24	PENNY	Hindi Göğüs Fileto	Penny	Et & Tavuk	1	€2,79	€2,79	B (7%)	3938
2026-09-24	PENNY	Genç Gouda Dilimli Peynir	Penny	Şarküteri & Peynir	1	€1,65	€1,65	B (7%)	3938
2026-09-24	PENNY	Çok Tahıllı Bagel Ekmeği	Penny	Fırın & Ekmek	1	€1,39	€1,39	B (7%)	3938
2026-09-24	PENNY	Hazır Köfte Topları	Penny	Et & Hazır Yemek	1	€2,99	€2,99	B (7%)	3938
2026-09-24	PENNY	Salatalık	Manav	Meyve & Sebze	2	€0,59	€1,18	B (7%)	3938
2026-09-24	PENNY	Kırmızı Kapya Biber	Manav	Meyve & Sebze	1	€1,99	€1,99	B (7%)	3938
2026-09-24	PENNY	Sivri Biber	Manav	Meyve & Sebze	1	€2,49	€2,49	B (7%)	3938
2026-09-24	PENNY	Alp Tuzu	Bad Reichenhaller / Penny	Sos & Baharat	1	€0,75	€0,75	B (7%)	3938
2026-09-24	PENNY	Pesto Sos	San Fabio	Sos & Baharat	1	€0,89	€0,89	B (7%)	3938
2026-09-24	PENNY	Püre Domates (Passata)	Penny	Konserve & Sos	1	€0,69	€0,69	B (7%)	3938
2026-09-24	PENNY	Bira (Hell)	Augustiner	İçecek & Alkol	2	€1,05	€2,10	A (19%)	3938
2026-09-24	PENNY	Şişe Depozitosu (Pfand)	Pfand	Depozito	2	€0,08	€0,16	A (19%)	3938
2026-09-24	PENNY	Alışveriş Poşeti	Penny	Diğer	1	€0,25	€0,25	A (19%)	3938
2026-09-25	HIT	Muz (0.772 kg)	Banderole	Meyve & Sebze	1	€1,29	€1,00	B (7%)	1327
2026-09-25	HIT	Domates (Coeur de Boeuf 0.356 kg)	Manav	Meyve & Sebze	0	€5,99	€2,13	B (7%)	1327
2026-09-25	HIT	Biberli Pizza Atıştırmalık	HIT	Atıştırmalık & Dondurulmuş	1	€0,99	€0,99	B (7%)	1327
2026-09-25	HIT	Taş Fırın Ekmeği	REWE Bio	Fırın & Ekmek	1	€1,39	€1,39	B (7%)	1327
2026-09-25	HIT	Makarna	Delverde	Kuru Gıda & Makarna	1	€0,79	€0,79	B (7%)	1327
2026-09-25	HIT	Makarna	Delverde	Kuru Gıda & Makarna	2	€0,79	€1,58	B (7%)	1327
2026-09-25	HIT	Sirke Ruhu %25 (Essigessenz)	Surig	Temel Gıda	1	€1,59	€1,59	B (7%)	1327
2026-09-25	HIT	Sirke Ruhu (Essigessenz)	Surig	Temel Gıda	1	€3,49	€3,49	B (7%)	1327
2026-09-25	HIT	Konserve Fasulye	Delikatess	Konserve & Bakliyat	2	€2,49	€4,98	B (7%)	1327
2026-09-25	HIT	Dana Kıyma	HIT	Et & Tavuk	1	€4,60	€4,60	B (7%)	1327
2026-09-25	HIT	Biber Turşusu (Pfefferoni)	Ostsee	Konserve & Meze	1	€1,09	€1,09	B (7%)	1327
2026-09-25	HIT	Kekik (Oregano)	Ostsee	Baharat	1	€1,59	€1,59	B (7%)	1327
2026-09-25	HIT	Kırmızı Mercimek	T&L	Bakliyat	1	€2,39	€2,39	B (7%)	1327
2026-09-25	HIT	Yoğurt	Körfez	Süt Ürünleri	1	€2,59	€2,59	B (7%)	1327
2026-09-25	HIT	Tereyağı	Kerrygold	Süt Ürünleri	1	€1,99	€1,99	B (7%)	1327
2026-09-25	HIT	Ağız Çalkalama Suyu	Listerine	Kişisel Bakım	1	€4,95	€4,95	A (19%)	1327
2026-09-25	HIT	LED Mum / Ampul	HIT	Ev Gereçleri	1	€0,89	€0,89	A (19%)	1327
2026-09-25	HIT	Şeffaf Sürahi	HIT	Mutfak & Züccaciye	1	€0,39	€0,39	A (19%)	1327
2026-09-25	HIT	Tereyağlık Kabı	HIT	Mutfak & Züccaciye	1	€0,35	€0,35	A (19%)	1327
2026-10-02	PENNY	Tavuk Göğüs Fileto	Penny	Et & Tavuk	1	€6,79	€6,79	B (7%)	2441
2026-10-02	PENNY	Rendelenmiş Emmental Peyniri	Penny	Şarküteri & Peynir	1	€1,79	€1,79	B (7%)	2441
2026-10-02	PENNY	Taş Fırın Baget Ekmeği	Penny	Fırın & Ekmek	1	€1,19	€1,19	B (7%)	2441
2026-10-02	PENNY	Kafes Yumurta 10'lu	Penny	Şarküteri & Yumurta	1	€4,19	€4,19	B (7%)	2441
2026-10-02	PENNY	Sade Skyr	Penny	Süt Ürünleri	1	€1,29	€1,29	B (7%)	2441
2026-10-02	PENNY	Püre Domates (Passata)	Penny	Konserve & Sos	1	€0,69	€0,69	B (7%)	2441
2026-10-02	PENNY	Tuzlu Patates Cipsi	Lay's	Atıştırmalık & Cips	1	€1,99	€1,99	B (7%)	2441
2026-10-05	PENNY	Emmental Peyniri 250g	Penny	Şarküteri & Peynir	1	€2,29	€2,29	B (7%)	9965
2026-10-05	PENNY	Weltmeister Çavdar Ekmeği	Penny	Fırın & Ekmek	1	€1,59	€1,59	B (7%)	9965
2026-10-05	PENNY	Çengelköy / Mini Salatalık	Manav	Meyve & Sebze	2	€0,49	€0,98	B (7%)	9965
2026-10-05	PENNY	Organik Siyez / Dinkel Unu	Penny Bio	Temel Gıda & Un	1	€1,25	€1,25	B (7%)	9965
2026-10-05	PENNY	Esmer Şeker	Südzucker	Temel Gıda & Şeker	1	€1,69	€1,69	B (7%)	9965
2026-10-05	PENNY	Müsli Bar	Corny	Atıştırmalık	1	€2,39	€2,39	B (7%)	9965
2026-10-05	PENNY	Patates Cipsi	Penny	Atıştırmalık & Cips	1	€0,99	€0,99	B (7%)	9965
2026-10-05	PENNY	Beyazlatıcı Diş Macunu	Today Dent / Penny	Kişisel Bakım	1	€1,45	€1,45	A (19%)	9965
2026-10-05	PENNY	Alışveriş Poşeti	Penny	Diğer	1	€0,25	€0,25	A (19%)	9965
2026-10-06	PENNY	Dana Kıyma (%5 Yağlı)	Penny	Et & Tavuk	1	€5,49	€5,49	B (7%)	874
2026-10-06	PENNY	Rendelenmiş Emmental Peyniri	Penny	Şarküteri & Peynir	1	€1,79	€1,79	B (7%)	874
2026-10-06	PENNY	Ayran	Penny	İçecek & Süt	1	€0,89	€0,89	B (7%)	874
2026-10-06	PENNY	Patates 2.5kg	Penny	Meyve & Sebze	1	€2,49	€2,49	B (7%)	874
2026-10-06	PENNY	Çeri Domates	Manav	Meyve & Sebze	1	€1,19	€1,19	B (7%)	874
2026-10-06	PENNY	Kırmızı Kapya Biber	Manav	Meyve & Sebze	1	€1,99	€1,99	B (7%)	874
2026-10-06	PENNY	Dondurulmuş Pizza Margherita	Penny	Dondurulmuş & Hazır Yemek	1	€2,99	€2,99	B (7%)	874
2026-10-06	PENNY	Dondurulmuş Pizza Diavolo	Penny	Dondurulmuş & Hazır Yemek	1	€3,49	€3,49	B (7%)	874
2026-10-06	PENNY	Mayonez	Penny	Sos & Baharat	1	€2,79	€2,79	B (7%)	874
2026-10-06	PENNY	Patates Cipsi	Penny	Atıştırmalık & Cips	1	€0,99	€0,99	B (7%)	874
2026-10-06	PENNY	Aseton / Oje Çıkarıcı	Today / Penny	Kişisel Bakım	1	€1,25	€1,25	A (19%)	874
2026-10-08	PENNY	Muz (1.308 kg)	Chiquita	Meyve & Sebze	1	€2,49	€3,26	B (7%)	2968
2026-10-08	PENNY	Kuru Soğan 2kg	Penny	Meyve & Sebze	1	€1,99	€1,99	B (7%)	2968
2026-10-08	PENNY	Laktozsuz Süt %1.5	Penny	Süt Ürünleri	1	€1,05	€1,05	B (7%)	2968
2026-10-08	PENNY	Pirinç	Landfreund	Kuru Gıda & Bakliyat	1	€1,39	€1,39	B (7%)	2968
2026-10-08	PENNY	Soya Sosu	Taste of Asia (ToA)	Sos & Baharat	1	€1,39	€1,39	B (7%)	2968
2026-10-08	PENNY	Dondurulmuş Bezelye & Havuç	Greenland	Dondurulmuş	1	€1,69	€1,69	B (7%)	2968
2026-10-08	PENNY	Püre Domates (Passata)	San Fabio	Konserve & Sos	1	€0,65	€0,65	B (7%)	2968
2026-10-09	ALDI SÜD	Tuvalet Kağıdı 4 Katlı 10'lu	Topa	Temizlik & Kağıt	1	€4,85	€4,85	B (7%)	6519
2026-10-09	ALDI SÜD	Depozito İadesi (Pfand)	Pfand	Depozito	1	-€1,00	-€1,00	B (7%)	6519
2026-10-09	ALDI SÜD	Sıvı El Sabunu	ALDI	Kişisel Bakım	1	€1,95	€1,95	B (7%)	6519
2026-10-09	ALDI SÜD	Yulaf Sütü (Haferdrink)	Daily	İçecek & Süt	1	€2,55	€2,55	B (7%)	6519
2026-10-09	ALDI SÜD	Türk Yoğurdu 1kg	ALDI	Süt Ürünleri	1	€2,09	€2,09	A (19%)	6519
2026-10-09	ALDI SÜD	Kafes Yumurta 10'lu	ALDI	Şarküteri & Yumurta	1	€4,19	€4,19	A (19%)	6519
2026-10-09	HIT	Tereyağı	Kerrygold	Süt Ürünleri	1	€1,49	€1,49	B (7%)	89
2026-10-09	HIT	Su Filtreli Sürahi (Aluna + 1 Maxtra)	Brita	Ev Gereçleri	1	€19,99	€19,99	A (19%)	89
2026-09-14	PENNY	Ahududu (Himbeeren)	Penny	Meyve & Sebze	2	€2,49	€4,98	B (7%)	5494
2026-09-14	PENNY	Kinder Çikolata Bar	Kinder	Atıştırmalık & Çikolata	1	€3,29	€3,29	B (7%)	5494
2026-09-14	PENNY	Kinder İndirimi (%25)	Kinder	İndirim	1	-€0,82	-€0,82	B (7%)	5494
2026-09-14	PENNY	Enerji İçeceği (Kutu)	Red Bull	İçecek & Enerji	1	€0,99	€0,99	A (19%)	5494
2026-09-14	PENNY	Kutu Depozitosu (Pfand)	Pfand	Depozito	1	€0,25	€0,25	A (19%)	5494
2026-10-10	PENNY	Tavuk Göğüs Fileto	Penny	Et & Tavuk	1	€6,79	€6,79	B (7%)	2377
2026-10-10	PENNY	Aromalı / Baharatlı Cheddar	Penny	Şarküteri & Peynir	1	€2,19	€2,19	B (7%)	2377
2026-10-10	PENNY	Rendelenmiş Gouda Peyniri	Penny	Şarküteri & Peynir	1	€1,79	€1,79	B (7%)	2377
2026-10-10	PENNY	Kestane Mantarı (Kahverengi)	Manav	Meyve & Sebze	1	€2,19	€2,19	B (7%)	2377
2026-10-10	PENNY	Taze Süt	Weihenstephan	Süt Ürünleri	1	€1,59	€1,59	B (7%)	2377
2026-10-10	PENNY	Krema %12 (H-Sahne)	Penny	Süt Ürünleri	1	€0,59	€0,59	B (7%)	2377
2026-10-10	PENNY	Kruvazan / Boyoz Makarna (Cornetti)	Bernbacher	Kuru Gıda & Makarna	1	€1,89	€1,89	B (7%)	2377
2026-10-10	PENNY	Patates Cipsi	Penny	Atıştırmalık & Cips	1	€0,99	€0,99	B (7%)	2377
2026-10-10	PENNY	İtalyan Beyaz Şarap (Soave DOC)	Soave	İçecek & Alkol	1	€1,99	€1,99	A (19%)	2377
2026-10-10	PENNY	Kapsül Kahve (Grande 16er)	Nescafé Dolce Gusto	Kahve & Sıcak İçecek	1	€5,99	€5,99	B (7%)	2377
2026-10-12	ALDI SÜD	Protein Ekmeği (Proteinbrot)	ALDI	Fırın & Ekmek	1	€1,99	€1,99	A (7%)	7460
2026-10-12	ALDI SÜD	Tuzlu Patates Cipsi	ALDI	Atıştırmalık & Cips	1	€0,99	€0,99	A (7%)	7460
2026-10-14	PENNY	Hazır Köfte Topları	Penny	Et & Hazır Yemek	1	€2,99	€2,99	B (7%)	6795
2026-10-14	PENNY	Muz (1.010 kg)	Chiquita	Meyve & Sebze	1,01	€2,49	€2,51	B (7%)	6795
2026-10-14	PENNY	Çengelköy / Mini Salatalık	Manav	Meyve & Sebze	3	€0,49	€1,47	B (7%)	6795
2026-10-14	PENNY	Kırmızı Kapya Biber	Manav	Meyve & Sebze	1	€1,99	€1,99	B (7%)	6795
2026-10-14	PENNY	Yulaf Sütü Barista	Naturgut	İçecek & Süt	1	€2,55	€2,55	A (19%)	6795
2026-10-14	PENNY	Yunan Yoğurdu	Penny	Süt Ürünleri	1	€2,19	€2,19	B (7%)	6795
2026-10-14	PENNY	Ekşi Kremalı Cips (Sour Cream & Onion)	Lay's	Atıştırmalık & Cips	1	€1,99	€1,99	B (7%)	6795
2026-10-15	Wolt Market	Tuzlu Patates Cipsi 150g	Lay's	Atıştırmalık & Cips	1	€1,25	€1,25	7%	2461222
2026-10-15	Wolt Market	Sirkeli Cips (Salt & Vinegar) 150g	Lay's	Atıştırmalık & Cips	1	€1,25	€1,25	7%	2461222
2026-10-15	Wolt Market	Kakaolu Fındık Kreması 750g	Nutella	Kahvaltılık & Sürülebilir	1	€6,29	€6,29	7%	2461222
2026-10-15	Wolt Market	Tavuk Göğüs Fileto 600g	ja!	Et & Tavuk	1	€6,79	€6,79	7%	2461222
2026-10-15	Wolt Market	Jambon (Saftschinken) 100g	Herta	Şarküteri & Et	1	€2,29	€2,29	7%	2461222
2026-10-15	Wolt Market	Galeta Unu / Panko 400g	Leimer	Temel Gıda	1	€1,59	€1,59	7%	2461222
2026-10-15	Wolt Market	Sızma Zeytinyağı 0.75L	ja!	Temel Gıda & Sıvı Yağ	1	€5,99	€5,99	7%	2461222
2026-10-16	PENNY	Organik Müsli Bar	Naturgut	Atıştırmalık	1	€2,29	€2,29	B (7%)	7825
2026-10-16	PENNY	Granola Müsli Bar	Penny	Atıştırmalık	1	€1,49	€1,49	B (7%)	7825
2026-10-16	PENNY	Siyah Çikolata %85	Penny	Atıştırmalık & Çikolata	1	€1,85	€1,85	B (7%)	7825
2026-10-16	PENNY	Oreo'lu Çikolata	Milka	Atıştırmalık & Çikolata	1	€1,99	€1,99	B (7%)	7825
2026-10-16	PENNY	Meyveli Gazoz (Spezi)	Paulaner	İçecek & Gazoz	1	€0,95	€0,95	A (19%)	7825
2026-10-16	PENNY	Kutu Depozitosu (Pfand)	Pfand	Depozito	1	€0,25	€0,25	A (19%)	7825
2026-10-17	PENNY	Kafes Yumurta 10'lu	Penny	Şarküteri & Yumurta	1	€4,19	€4,19	B (7%)	4097
2026-10-17	PENNY	Dondurulmuş Salamlı Pizza	Penny	Dondurulmuş & Hazır Yemek	2	€3,99	€7,98	B (7%)	4097
2026-10-19	PENNY	Rendelenmiş Emmental Peyniri	Penny	Şarküteri & Peynir	1	€1,79	€1,79	B (7%)	4744
2026-10-19	PENNY	Hazır Köfte Topları	Penny	Et & Hazır Yemek	1	€2,99	€2,99	B (7%)	4744
2026-10-19	PENNY	Ekşi Kremalı Cips (Sour Cream & Onion)	Lay's	Atıştırmalık & Cips	1	€1,99	€1,99	B (7%)	4744
2026-10-20	PENNY	Dana Kıyma	Penny	Et & Tavuk	1	€5,49	€5,49	B (7%)	4921
2026-10-20	PENNY	Yüksek Proteinli Lavaş / Lavaş Ekmek	Penny	Fırın & Ekmek	3	€1,49	€4,47	B (7%)	4921
2026-10-20	PENNY	Ayran	Penny	İçecek & Süt	2	€0,89	€1,78	B (7%)	4921
2026-10-20	PENNY	Muz (1.264 kg)	Chiquita	Meyve & Sebze	1,264	€1,99	€2,52	B (7%)	4921
2026-10-20	PENNY	Çeri Domates	Manav	Meyve & Sebze	1	€1,19	€1,19	B (7%)	4921
2026-10-20	PENNY	Fıstık Ezmeli Atıştırmalık	ChoViva	Atıştırmalık	1	€1,99	€1,99	B (7%)	4921
2026-10-22	HIT	Havuç (0.154 kg)	Manav	Meyve & Sebze	0,154	€1,99	€0,31	B (7%)	458
2026-10-22	HIT	Beyaz Kültür Mantarı	HIT	Meyve & Sebze	1	€1,99	€1,99	B (7%)	458
2026-10-22	HIT	Kuzu Kulağı / Yeşillik Salatası (Feldsalat)	HIT	Meyve & Sebze	1	€1,89	€1,89	B (7%)	458
2026-10-22	HIT	Kırmızı Kapya Biber	Manav	Meyve & Sebze	1	€2,19	€2,19	B (7%)	458
2026-10-22	HIT	Muz (0.976 kg)	Chiquita	Meyve & Sebze	0,976	€2,49	€2,43	B (7%)	458
2026-10-22	HIT	Kapsül Kahve	Nescafé Dolce Gusto	Kahve & Sıcak İçecek	1	€5,99	€5,99	B (7%)	458
2026-10-22	HIT	Salam / Şarküteri (WSH HIT Klassik)	WSH HIT Klassik	Şarküteri & Et	1	€5,66	€5,66	B (7%)	458
2026-10-22	PENNY	Yumuşak Beyaz Peynir / Süzme Peynir	Mitakos	Şarküteri & Peynir	1	€1,79	€1,79	B (7%)	5950
2026-10-22	PENNY	ProVital Dilim Ekmek / Dilim	Penny	Fırın & Ekmek	1	€1,29	€1,29	B (7%)	5950
2026-10-22	PENNY	Yunan Yoğurdu	Penny	Süt Ürünleri	1	€2,19	€2,19	B (7%)	5950`;

function parsePrice(str) {
  if (!str) return 0;
  return parseFloat(str.replace('€', '').replace(/\s/g, '').replace(',', '.'));
}

function parseQty(str) {
  if (!str) return 1;
  return parseFloat(str.replace(/\s/g, '').replace(',', '.'));
}

const items = [];
let currentId = 1;

const lines = rawText.trim().split('\n');
for (let line of lines) {
  const parts = line.split('\t').map(s => s.trim());
  if (parts.length >= 8) {
    const tarih = parts[0];
    const market = parts[1];
    const urun = parts[2];
    const marka = parts[3];
    const kategori = parts[4];
    const miktar = parseQty(parts[5]);
    const birim_fiyat = parsePrice(parts[6]);
    const toplam_fiyat = parsePrice(parts[7]);
    const kdv = parts[8] || 'B (7%)';
    const fis_no = parts[9] || '';

    let fis_resmi = null;
    if (fis_no === '5950') {
      fis_resmi = '/receipts/receipt_2026-10-22_5950.png';
    }

    items.push({
      id: currentId++,
      tarih,
      market,
      urun,
      marka,
      kategori,
      miktar,
      birim_fiyat,
      toplam_fiyat,
      kdv,
      fis_no,
      fis_resmi,
      odeyen: 'Ortak'
    });
  }
}

// 4 New Receipts from User Images
// 1. 2026-10-26 PENNY (5573) Total 9.14 EUR
const receipt5573 = [
  { urun: "Finesse Hindi Füme", marka: "Herta / Penny", kategori: "Şarküteri & Et", miktar: 1, birim_fiyat: 2.59, toplam_fiyat: 2.59, kdv: "B (7%)" },
  { urun: "Laugenstange (Pretzel Çubuğu)", marka: "Penny Fırın", kategori: "Fırın & Ekmek", miktar: 3, birim_fiyat: 0.39, toplam_fiyat: 1.17, kdv: "B (7%)" },
  { urun: "Dondurulmuş Pizza Margherita", marka: "Penny", kategori: "Dondurulmuş & Hazır Yemek", miktar: 1, birim_fiyat: 0.99, toplam_fiyat: 0.99, kdv: "B (7%)" },
  { urun: "Muz (1.424 kg)", marka: "Manav", kategori: "Meyve & Sebze", miktar: 1.424, birim_fiyat: 1.29, toplam_fiyat: 1.84, kdv: "B (7%)" },
  { urun: "Yulaf Sütü Barista", marka: "Naturgut", kategori: "İçecek & Süt", miktar: 1, birim_fiyat: 2.55, toplam_fiyat: 2.55, kdv: "A (19%)" }
];

for (let it of receipt5573) {
  items.push({
    id: currentId++,
    tarih: "2026-10-26",
    market: "PENNY",
    urun: it.urun,
    marka: it.marka,
    kategori: it.kategori,
    miktar: it.miktar,
    birim_fiyat: it.birim_fiyat,
    toplam_fiyat: it.toplam_fiyat,
    kdv: it.kdv,
    fis_no: "5573",
    fis_resmi: "/receipts/receipt_2026-10-26_5573.png",
    odeyen: 'Ortak'
  });
}

// 2. 2026-10-26 PENNY (1053) Total 17.40 EUR
const receipt1053 = [
  { urun: "Dana Kıyma (RD-Hackfleisch)", marka: "Penny", kategori: "Et & Tavuk", miktar: 1, birim_fiyat: 5.79, toplam_fiyat: 5.79, kdv: "B (7%)" },
  { urun: "Emmental Peyniri 250g", marka: "Penny", kategori: "Şarküteri & Peynir", miktar: 1, birim_fiyat: 2.29, toplam_fiyat: 2.29, kdv: "B (7%)" },
  { urun: "Yumuşak Beyaz Peynir (Mitakos)", marka: "Mitakos", kategori: "Şarküteri & Peynir", miktar: 1, birim_fiyat: 1.79, toplam_fiyat: 1.79, kdv: "B (7%)" },
  { urun: "Ayran Natur", marka: "Penny", kategori: "İçecek & Süt", miktar: 2, birim_fiyat: 0.89, toplam_fiyat: 1.78, kdv: "B (7%)" },
  { urun: "Havuç (0.158 kg)", marka: "Manav", kategori: "Meyve & Sebze", miktar: 0.158, birim_fiyat: 1.69, toplam_fiyat: 0.27, kdv: "B (7%)" },
  { urun: "Kafes Yumurta 10'lu", marka: "Penny", kategori: "Şarküteri & Yumurta", miktar: 1, birim_fiyat: 4.19, toplam_fiyat: 4.19, kdv: "B (7%)" },
  { urun: "Yeşil Taze Fasulye (Greenland)", marka: "Greenland", kategori: "Konserve & Bakliyat", miktar: 1, birim_fiyat: 1.29, toplam_fiyat: 1.29, kdv: "B (7%)" }
];

for (let it of receipt1053) {
  items.push({
    id: currentId++,
    tarih: "2026-10-26",
    market: "PENNY",
    urun: it.urun,
    marka: it.marka,
    kategori: it.kategori,
    miktar: it.miktar,
    birim_fiyat: it.birim_fiyat,
    toplam_fiyat: it.toplam_fiyat,
    kdv: it.kdv,
    fis_no: "1053",
    fis_resmi: "/receipts/receipt_2026-10-26_1053.png",
    odeyen: 'Ortak'
  });
}

// 3. 2026-10-28 PENNY (7449) Total 16.99 EUR
const receipt7449 = [
  { urun: "Taş Fırın Baget Ekmeği", marka: "Penny", kategori: "Fırın & Ekmek", miktar: 1, birim_fiyat: 1.19, toplam_fiyat: 1.19, kdv: "B (7%)" },
  { urun: "Çengelköy / Mini Salatalık", marka: "Manav", kategori: "Meyve & Sebze", miktar: 2, birim_fiyat: 0.49, toplam_fiyat: 0.98, kdv: "B (7%)" },
  { urun: "Kabak (Zucchini 0.348 kg)", marka: "Manav", kategori: "Meyve & Sebze", miktar: 0.348, birim_fiyat: 1.49, toplam_fiyat: 0.52, kdv: "B (7%)" },
  { urun: "Yunan Yoğurdu (Joghurt Griech.)", marka: "Penny", kategori: "Süt Ürünleri", miktar: 1, birim_fiyat: 2.19, toplam_fiyat: 2.19, kdv: "B (7%)" },
  { urun: "Siyez / Dinkel Spagetti", marka: "Landfreund", kategori: "Kuru Gıda & Makarna", miktar: 1, birim_fiyat: 1.29, toplam_fiyat: 1.29, kdv: "B (7%)" },
  { urun: "Kritharaki Arpa Şehriye", marka: "Penny", kategori: "Kuru Gıda & Makarna", miktar: 1, birim_fiyat: 0.99, toplam_fiyat: 0.99, kdv: "B (7%)" },
  { urun: "Organik Müsli (Naturgut)", marka: "Naturgut", kategori: "Kahvaltılık", miktar: 1, birim_fiyat: 2.65, toplam_fiyat: 2.65, kdv: "B (7%)" },
  { urun: "Organik Keten Tohumu (Bio Leinsamen)", marka: "Penny Bio", kategori: "Kuru Gıda & Tohum", miktar: 1, birim_fiyat: 1.55, toplam_fiyat: 1.55, kdv: "B (7%)" },
  { urun: "Tahin (MK Tahini)", marka: "MK", kategori: "Sos & Kahvaltılık", miktar: 1, birim_fiyat: 2.29, toplam_fiyat: 2.29, kdv: "B (7%)" },
  { urun: "Patates Cipsi", marka: "Penny", kategori: "Atıştırmalık & Cips", miktar: 1, birim_fiyat: 0.99, toplam_fiyat: 0.99, kdv: "B (7%)" },
  { urun: "WC Koku Bloğu (Blik Duft)", marka: "Blik", kategori: "Ev & Temizlik", miktar: 1, birim_fiyat: 0.95, toplam_fiyat: 0.95, kdv: "A (19%)" },
  { urun: "Alışveriş Poşeti", marka: "Penny", kategori: "Diğer", miktar: 1, birim_fiyat: 0.25, toplam_fiyat: 0.25, kdv: "A (19%)" },
  { urun: "Çöp Torbası (Home Ideas Müllb)", marka: "Home Ideas", kategori: "Ev & Temizlik", miktar: 1, birim_fiyat: 1.15, toplam_fiyat: 1.15, kdv: "A (19%)" }
];

for (let it of receipt7449) {
  items.push({
    id: currentId++,
    tarih: "2026-10-28",
    market: "PENNY",
    urun: it.urun,
    marka: it.marka,
    kategori: it.kategori,
    miktar: it.miktar,
    birim_fiyat: it.birim_fiyat,
    toplam_fiyat: it.toplam_fiyat,
    kdv: it.kdv,
    fis_no: "7449",
    fis_resmi: "/receipts/receipt_2026-10-28_7449.png",
    odeyen: 'Ortak'
  });
}

// 4. 2026-10-29 PENNY (7965) Total 27.08 EUR
const receipt7965 = [
  { urun: "Dana Kıyma (RD-Hackfleisch)", marka: "Penny", kategori: "Et & Tavuk", miktar: 1, birim_fiyat: 5.79, toplam_fiyat: 5.79, kdv: "B (7%)" },
  { urun: "Yumuşak Beyaz Peynir (Mitakos)", marka: "Mitakos", kategori: "Şarküteri & Peynir", miktar: 1, birim_fiyat: 1.79, toplam_fiyat: 1.79, kdv: "B (7%)" },
  { urun: "Tereyağı (Kerrygold Butter)", marka: "Kerrygold", kategori: "Süt Ürünleri", miktar: 1, birim_fiyat: 3.29, toplam_fiyat: 3.29, kdv: "B (7%)" },
  { urun: "Yulaf Sütü Barista", marka: "Naturgut", kategori: "İçecek & Süt", miktar: 1, birim_fiyat: 2.55, toplam_fiyat: 2.55, kdv: "A (19%)" },
  { urun: "Dondurulmuş Salamlı Pizza", marka: "Penny", kategori: "Dondurulmuş & Hazır Yemek", miktar: 1, birim_fiyat: 3.99, toplam_fiyat: 3.99, kdv: "B (7%)" },
  { urun: "Durum Buğdayı İrmiği (Hartweizengr.)", marka: "Landfreund", kategori: "Temel Gıda & Un", miktar: 1, birim_fiyat: 0.69, toplam_fiyat: 0.69, kdv: "B (7%)" },
  { urun: "Kakaolu Fındık Kreması 1000g", marka: "Nutella", kategori: "Kahvaltılık & Sürülebilir", miktar: 1, birim_fiyat: 6.99, toplam_fiyat: 6.99, kdv: "B (7%)" },
  { urun: "İtalyan Beyaz Şarap (SOAVE DOC)", marka: "Soave", kategori: "İçecek & Alkol", miktar: 1, birim_fiyat: 1.99, toplam_fiyat: 1.99, kdv: "A (19%)" }
];

for (let it of receipt7965) {
  items.push({
    id: currentId++,
    tarih: "2026-10-29",
    market: "PENNY",
    urun: it.urun,
    marka: it.marka,
    kategori: it.kategori,
    miktar: it.miktar,
    birim_fiyat: it.birim_fiyat,
    toplam_fiyat: it.toplam_fiyat,
    kdv: it.kdv,
    fis_no: "7965",
    fis_resmi: "/receipts/receipt_2026-10-29_7965.png",
    odeyen: 'Ortak'
  });
}

// Sort items by date descending, then id
items.sort((a, b) => b.tarih.localeCompare(a.tarih) || b.id - a.id);

// Write to JSON
const jsonPath = path.join(__dirname, 'data', 'market_data.json');
fs.writeFileSync(jsonPath, JSON.stringify(items, null, 2), 'utf-8');

// Write to CSV
const csvHeaders = ['ID', 'Tarih', 'Market', 'Ürün Adı', 'Marka', 'Kategori', 'Miktar', 'Birim Fiyat (€)', 'Toplam Fiyat (€)', 'KDV Grubu', 'Fiş No', 'Ödeyen'];
const csvRows = items.map(it => [
  it.id,
  it.tarih,
  `"${it.market}"`,
  `"${it.urun.replace(/"/g, '""')}"`,
  `"${it.marka.replace(/"/g, '""')}"`,
  `"${it.kategori.replace(/"/g, '""')}"`,
  it.miktar,
  it.birim_fiyat.toFixed(2),
  it.toplam_fiyat.toFixed(2),
  `"${it.kdv}"`,
  `"${it.fis_no}"`,
  `"${it.odeyen}"`
].join(';'));

const csvContent = '\uFEFF' + [csvHeaders.join(';'), ...csvRows].join('\r\n');
const csvPath = path.join(__dirname, 'data', 'market_data.csv');
fs.writeFileSync(csvPath, csvContent, 'utf-8');

console.log(`Successfully generated database with ${items.length} items!`);
console.log(`Total spend: €${items.reduce((s, x) => s + x.toplam_fiyat, 0).toFixed(2)}`);
