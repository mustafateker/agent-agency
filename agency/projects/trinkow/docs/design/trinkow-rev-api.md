# Trinkow Rev finance API

All routes require existing Bearer auth. Money is integer kuruş, dates YYYY-MM-DD. `bugun` is mandatory on finance routes and identifies the client local day. New settings take effect on `bugun`, never on an arbitrary past date. Errors: HTTP 422 with `detail` for invalid budgets/dates; 404 unknown owned item. Null budget means unknown, not zero.

## Budget

`GET /butce?bugun=2026-09-23&gun=2026-09-23` (gun optional) returns:
```json
{"gun":"2026-09-23","butce": {"yururluk_gunu":"2026-09-23","gelir_kurus":6000000,"sabit_giderler":{"kira":1500000,"fatura":300000,"ulasim":200000,"kredi":0},"hedef_birikim_kurus":1000000,"borc_kurus":0,"limit_modu":"otomatik","manuel_limit_kurus":null,"kategori_limitleri":{"kafe":10000},"gunluk_limit_kurus":100000,"gunluk_gelir_payi_kurus":100000,"dagitilmamis_kurus":90000},"eski_aylik_kategori_limitleri":[]}
```
`PUT /butce?bugun=...` full state replacement; body fields are exactly `gelir_kurus` (nullable), `sabit_giderler` (kira/fatura/ulasim/kredi nonnegative), `hedef_birikim_kurus`, `borc_kurus` (nullable), `limit_modu` (otomatik/manuel), `manuel_limit_kurus` (positive for manuel, null otherwise), `kategori_limitleri` (category code -> nonnegative integer). Returns GET shape. Existing days use their last effective version. Category sum cannot exceed selected daily limit. Manual limit is independent of income. First access preserves legacy daily limit and archives existing MONTHLY categories (not silently converted).

## Routines, favorites, expense metadata

`GET /butce/rutinler?bugun=...&gun=...` -> `{"rutinler":[{"id":"...","ad":"Kahve","kategori":"kafe","gunluk_adet":1,"birim_fiyat_kurus":10000,"aktif":true,"yururluk_gunu":"..."}]}`.
`PUT /butce/rutinler/{id}?bugun=...` client-generated stable UUID id; body `{"ad":"Kahve","kategori":"kafe","gunluk_adet":1,"birim_fiyat_kurus":10000,"aktif":true}` -> same routine object. Setting aktif false archives forward-only.
`PUT /butce/rutinler/{id}/vazgecme?bugun=...` body `{"gun":"2026-09-23","adet":1}` -> `{"rutin_id":"...","gun":"...","adet":1,"tasarruf_kurus":10000}`. Today/past tracked days only, quantity <= expected minus linked purchases; zero removes confirmation. GET monthly includes reconciled amounts after expense changes. Confirmation never creates cash savings.
`GET /butce/sik-kullanilanlar?bugun=...` -> `{"kalemler":[{"id":"...","ad":"Latte","kategori":"kafe","tutar_kurus":10000,"sabitlenmis":true,"kullanim_sayisi":3}]}`. Explicit favorites first, then frequent named products using latest recorded price, max 12.
`PUT /butce/sik-kullanilanlar/{id}` body `{"ad":"Latte","kategori":"kafe","tutar_kurus":10000}` -> favorite with `sabitlenmis:true`. `DELETE /butce/sik-kullanilanlar/{id}` -> 204.
Existing expense POST/PATCH gains optional `rutin_id` (null or ID), `adet` (positive integer default 1), `sabit_gider_kodu` (null/kira/fatura/ulasim/kredi). Existing responses include these fields. Linked mandatory payment consumes monthly reserved expense first; excess counts as discretionary spending. Category alone never determines exclusion. Routine and mandatory linkage are mutually exclusive. Existing expense routes otherwise unchanged.

## Savings

`GET /tasarruf/ay?ay=2026-09&bugun=2026-09-23` returns:
```json
{"ay":"2026-09","takip_baslangic_gunu":"2026-09-23","harcanabilir_kurus":800000,"harcanan_kurus":25000,"toplam_harcama_kurus":25000,"kalan_kurus":775000,"hesaplanan_tasarruf_kurus":0,"kumulatif_tasarruf_kurus":0,"gercek_birikim_kurus":0,"ay_birikim_kurus":0,"hedef_birikim_kurus":1000000,"rutin_tasarruf_kurus":10000,"bilinmeyen_gun_sayisi":22,"tamamlanan_gun_sayisi":0,"kategoriler":[{"kategori":"kafe","harcanan_kurus":25000,"rutin_tasarruf_kurus":10000}],"rutinler":[{"rutin_id":"...","ad":"Kahve","tasarruf_kurus":10000}],"motivasyon":{"tur":"birikim","mesaj":"Küçük adımlar birikimine dönüşebilir.","borc_kurus":0,"borc_yuzde":null}}
```
`harcanabilir` sums daily income allocation for tracked days of entire month; `kalan` subtracts posted spend through today. `hesaplanan_tasarruf` uses only completed days, signed to retain overspend; missing income yields null on income-derived totals. Cumulative includes completed tracked days across months. True savings ledger is independent and never added to budget remainder or routine estimate. Month is calendar month; first month is prorated from tracking start. `harcanan` excludes linked mandatory payments up to reserved amounts; `toplam_harcama` includes all recorded payments. Future installments do not count before their date. Motivation is in-app only, never asserts a debt payment occurred.

`GET /tasarruf/birikimler?ay=2026-09` (optional ay) -> `{"hareketler":[{"id":"...","gun":"2026-09-23","tutar_kurus":50000,"not_metni":"Kenara ayırdım"}],"toplam_kurus":50000}`.
`PUT /tasarruf/birikimler/{id}?bugun=...` UUID generated once per form; body `{"gun":"2026-09-23","tutar_kurus":50000,"not_metni":"Kenara ayırdım"}`. Positive deposit, negative withdrawal, nonzero; total ledger may not become negative. Upsert is retry-safe. `DELETE /tasarruf/birikimler/{id}` -> 204 (reject if removal would make balance negative).

## Compatibility / integration

Mount `app.modules.butce.butce_controller.router` and `app.modules.tasarruf.tasarruf_controller.router` in app/main.py. Account deletion/reset must call `await ButceService(db).hesap_verilerini_sil(user_id)`. Existing monthly category write endpoints reject with 409 directing new clients to /butce; do not interpret old amounts as daily. Existing daily limit write updates versioned budget, existing profile keeps mirrored latest limit. Legacy records survive unchanged.
