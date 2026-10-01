# ai-ajans

Trinkow operasyonu tek repoda, birbirinden bağımsız üç çalışma alanında yönetilir:

```text
ai-ajans/
├── backend/    # FastAPI + MongoDB servisi
├── mobile/     # React Native / Expo uygulaması
├── agency/     # ajanlar, operasyon kuralları, dokümanlar ve durum kayıtları
├── dev.py      # yerel servisleri birlikte başlatır
└── README.md
```

Her alan kendi bağımlılıklarına, README'sine ve çalıştırma komutlarına sahiptir.
Mobil uygulama backend'i yalnızca HTTP API üzerinden kullanır; ajans sistemi iki
uygulamanın kaynak kodundan ayrı tutulur.

## Hızlı başlangıç

Tüm yerel geliştirme ortamını başlatmak için:

```bash
cd mobile
npm run dev
```

Tek tek çalıştırmak için:

- Mobil: `cd mobile && npm start`
- Backend: `cd backend && .venv/bin/python -m uvicorn app.main:app --reload`
- Ajans: `cd agency && claude`

Ayrıntılı kurulum: [mobile/README.md](mobile/README.md),
[backend/README.md](backend/README.md) ve [agency/README.md](agency/README.md).
