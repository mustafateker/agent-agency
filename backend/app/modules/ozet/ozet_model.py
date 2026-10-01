"""
`ozet` modülünün KENDİ Mongo koleksiyonu YOKTUR.

Bu modül yalnız OKUR: `harcama` ve `kullanici` modüllerinin servis
arayüzlerini (`HarcamaService` / `KullaniciService`) çağırıp pano/özet/
kategori dağılımı/seri gibi TÜRETİLMİŞ görünümler üretir (K-076 — BE-5).
Kendi belgesini yazmadığı için burada bir Mongo şeması YOK; dosya yalnız
diğer modüllerle aynı dört-dosya iskeletini (controller/service/dto/model)
korumak için var (bkz. backend/README.md Kural 1).

Hesaplanan görünümlerin Python veri sınıfları (`GunlukPano`, `OzetGorunumu`,
`KategoriDetayGorunumu`, `SeriGorunumu` ...) `ozet_service.py` içinde
tanımlıdır — onlar Mongo belgesi değil, saf hesap sonucudur.
"""
from __future__ import annotations
