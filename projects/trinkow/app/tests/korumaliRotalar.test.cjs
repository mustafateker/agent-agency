const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');
const assert = require('node:assert/strict');

// Kapanış QA bulgusu: `app/birikimler.tsx` mevcut ve `tasarruflar`'dan
// `router.push` ile hedefleniyor, ama `Stack.Protected guard={durum ===
// 'acik'}` grubunda listeli değildi. Dosya tabanlı yönlendirme derlediği
// için `tsc` bunu yakalamaz — kaynak metni üzerinden kilitliyoruz.

test("'birikimler' oturum-açık korumalı ekran grubunda listeli", () => {
  const kaynak = fs.readFileSync(path.resolve(__dirname, '..', 'app/_layout.tsx'), 'utf8');
  const acikGrubu = kaynak.slice(kaynak.indexOf("guard={durum === 'acik'}"), kaynak.indexOf('</Stack.Protected>', kaynak.indexOf("guard={durum === 'acik'}")));
  assert.match(acikGrubu, /<Stack\.Screen name="birikimler" \/>/);
  // Kardeş ekranların hâlâ orada olduğunu da doğrula (regresyon güvenliği).
  for (const kardes of ['tasarruflar', 'profil', 'rutinler', 'favoriler', 'butce', 'ozet', 'limitler', 'kayitlar', 'seri', 'taksitler']) {
    assert.match(acikGrubu, new RegExp(`<Stack\\.Screen name="${kardes}" `));
  }
});
