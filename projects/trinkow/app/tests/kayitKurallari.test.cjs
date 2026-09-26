const { test } = require('node:test');
const assert = require('node:assert/strict');
const { yukle } = require('./yukle.cjs');
const metinler = yukle('src/content/metinler.ts');
const kurallar = yukle('src/lib/kayitKurallari.ts', { '@/content/metinler': metinler });

const temelParam = {
  eposta: 'a@b.com',
  sifreKuralKarsilandi: true,
  sifre: '12345678',
  sifreTekrar: '12345678',
  onayKosullar: true,
  onayGizlilik: true,
};

test('şifre tekrarı eşleşmiyorken "Hesap oluştur" pasif kalır, eşleşince etkinleşir', () => {
  assert.equal(kurallar.kayitGonderPasifMi({ ...temelParam, sifreTekrar: '87654321' }), true);
  assert.equal(kurallar.kayitGonderPasifMi(temelParam), false);
});

test('boş tekrar alanı hata üretmez, ama eyleme geçmeyi de engeller', () => {
  assert.equal(kurallar.sifreTekrarHatasi('12345678', ''), null);
  assert.equal(kurallar.kayitGonderPasifMi({ ...temelParam, sifreTekrar: '' }), true);
});

test('tekrar dolu ve eşleşmiyorsa hata mesajı basılır', () => {
  assert.equal(kurallar.sifreTekrarHatasi('12345678', '1234567x'), metinler.t['hata.sifre_eslesmiyor']);
  assert.equal(kurallar.sifreTekrarHatasi('12345678', '12345678'), null);
});

test('iki yasal onay işaretlenmemişken eylem pasif kalır', () => {
  assert.equal(kurallar.kayitGonderPasifMi({ ...temelParam, onayKosullar: false, onayGizlilik: true }), true);
  assert.equal(kurallar.kayitGonderPasifMi({ ...temelParam, onayKosullar: true, onayGizlilik: false }), true);
  assert.equal(kurallar.kayitGonderPasifMi({ ...temelParam, onayKosullar: false, onayGizlilik: false }), true);
});

test('onayVerildiMi yalnız iki onay da işaretliyken true döner', () => {
  assert.equal(kurallar.onayVerildiMi(true, true), true);
  assert.equal(kurallar.onayVerildiMi(true, false), false);
  assert.equal(kurallar.onayVerildiMi(false, true), false);
});

// `app/kayit.tsx` render altyapısı yok (bkz. tests/README yorumu); onaysız
// sosyal giriş dokunuşunda iki `Checkbox`ın `error`e geçtiği kaynak
// üzerinden doğrulanır — kaynak metnini değiştiren bir refaktör bu testi kırar.
test('onaysız sosyal giriş dokunuşunda iki Checkbox da error durumuna bağlı kalır', () => {
  const fs = require('node:fs');
  const kaynak = fs.readFileSync(require('node:path').resolve(__dirname, '..', 'app/kayit.tsx'), 'utf8');
  const hataAtamaSayisi = (kaynak.match(/error=\{onayHata\}/g) ?? []).length;
  assert.equal(hataAtamaSayisi, 2);
  assert.match(kaynak, /if \(!onayVerildiMi\(onayKosullar, onayGizlilik\)\)\s*\{\s*setOnayHata\(true\);/);
});
