# -*- coding: utf-8 -*-
"""E-10 — Bugün (Pano). Mood: sakin ve tek odakli.
Ust yari neredeyse bos: tek buyuk sayi + tek cubuk. Liste alt yarida."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *

SET = iconbtn("settings", "Ayarları aç")


def hero(etiket, sayi, sayi_renk, alt, bar, kip="Takip", sayi_cls="t-display"):
    return (div("col px20",
                div("row between",
                    T("t-label", "c-ink2", etiket)
                    + div("chip chip-sel shrink0", T("t-label", "c-acc", kip)))
                + sp(4)
                + f'<span class="{sayi_cls} {sayi_renk}">{sayi}</span>'
                + sp(24)
                + bar
                + sp(12)
                + f'<span class="t-caption c-ink2">{alt}</span>'))


def liste_baslik(sag_metin="Tümünü gör"):
    return (div("row between px20",
                T("t-label", "c-ink2", "Bugünkü kayıtlar")
                + T("t-label", "c-acc", sag_metin))
            + sp(12) + div("divider"))


def footer(btn):
    return div("col px20", btn, "padding-top:12px;padding-bottom:12px")


def govde(inner, aktif="bugun"):
    return div("scroll", inner)


PLUS = ic("plus", 24, "#FFFDF8", 1.75)


def btn_ekle(durum="default"):
    cls = {"default": "btn-p", "pressed": "btn-p btn-p-press",
           "disabled": "btn-p btn-p-dis"}[durum]
    renk = "c-ink2" if durum == "disabled" else "c-page"
    ikon = ic("plus", 24, "#5C574C" if durum == "disabled" else "#FFFDF8", 1.75)
    return div(cls, ikon + wsp(8) + T("t-bodys", renk, "Harcama ekle"), "align-self:stretch")


ROWS_180 = (spendrow("Kafe", "Kart · 08.40", "95 ₺") + div("divider-56")
            + spendrow("Ulaşım", "Kart · 09.05", "35 ₺") + div("divider-56")
            + spendrow("Market", "Nakit · 13.20", "50 ₺") + div("divider"))

bloklar = []

# ---------------------------------------------------------------- 1. dolu
bloklar.append(item(
    "E-10", "Bugün · dolu (limit altı)",
    "Günlük limit 300 ₺, harcanan 180 ₺. Çubuk %60 dolu, renk accent. "
    "Eşik çizgisi sağ uçta.",
    govde(header("Bugün", SET) + sp(32)
          + hero("bugün kalan", "120 ₺", "c-ink",
                 "Bugün 180 ₺. Limitinin 120 ₺ altındasın.", limitbar(180, 300))
          + sp(32) + liste_baslik() + ROWS_180)
    + footer(btn_ekle()) + tabbar("bugun")))

# ---------------------------------------------------------------- 2. %0 / bos
bloklar.append(item(
    "E-10", "Bugün · boş (ilk gün, %0)",
    "Çubuk boş oluk + eşik çizgisi. Kahraman sayı = günlük limit. "
    "EmptyState kullanıcıyı ilk kayda çağırır.",
    govde(header("Bugün", SET) + sp(32)
          + hero("bugün kalan", "300 ₺", "c-ink",
                 "Bugün henüz bir şey yazmadın.", limitbar(0, 300))
          + sp(48)
          + div("col px20 mid-x",
                tally() + sp(24)
                + T("t-h2", "c-ink", "Bugün boş") + sp(8)
                + '<span class="t-body c-ink2 mid">Bugün henüz bir şey yazmadın.'
                  ' İlk kahve iyi bir başlangıç.</span>'))
    + footer(btn_ekle()) + tabbar("bugun")))

# ---------------------------------------------------------------- 3. %100
bloklar.append(item(
    "E-10", "Bugün · limit doldu (%100)",
    "Çubuk tam dolu, eşik çizgisi sağ uçta. Renk DÖNMEZ, ikon değişmez, "
    "titremez. Kahraman sayı 0 ₺.",
    govde(header("Bugün", SET) + sp(32)
          + hero("bugün kalan", "0 ₺", "c-ink",
                 "Günlük limitin doldu. Bugün 300 ₺.", limitbar(300, 300))
          + sp(32) + liste_baslik()
          + spendrow("Kafe", "Kart · 08.40", "95 ₺") + div("divider-56")
          + spendrow("Ulaşım", "Kart · 09.05", "35 ₺") + div("divider-56")
          + spendrow("Market", "Nakit · 13.20", "50 ₺") + div("divider-56")
          + spendrow("Restoran", "Kart · 19.50", "120 ₺") + div("divider"))
    + footer(btn_ekle()) + tabbar("bugun")))

# ---------------------------------------------------------------- 4. tasma
bloklar.append(item(
    "E-10", "Bugün · limit dışı (%120)",
    "Eşiğin sağında ayrı Kiremit segment. Kırmızı yok, ünlem yok, uyarı "
    "ikonu yok. Sayı eksi ile değil 'limit dışı' etiketiyle verilir.",
    govde(header("Bugün", SET) + sp(32)
          + hero("bugün kalan", "60 ₺", "c-edge",
                 "Limitin 60 ₺ üzerindesin.", limitbar(360, 300))
          + div("col px20", sp(4) + T("t-label", "c-edge", "limit dışı"))
          + sp(24) + liste_baslik()
          + spendrow("Kafe", "Kart · 08.40", "95 ₺") + div("divider-56")
          + spendrow("Ulaşım", "Kart · 09.05", "35 ₺") + div("divider-56")
          + spendrow("Market", "Nakit · 13.20", "50 ₺") + div("divider-56")
          + spendrow("Restoran", "Kart · 19.50", "180 ₺", "overflow") + div("divider"))
    + footer(btn_ekle()) + tabbar("bugun")))

# ---------------------------------------------------------------- 5. limitsiz
bloklar.append(item(
    "E-10", "Bugün · günlük limit tanımsız",
    "Limit yoksa çubuk ÇİZİLMEZ (yanlış bir doluluk uydurmak yerine). "
    "Kahraman sayı bugünün toplamı olur.",
    govde(header("Bugün", SET) + sp(32)
          + div("col px20",
                T("t-label", "c-ink2", "bugün harcanan") + sp(4)
                + T("t-display", "c-ink", "180 ₺") + sp(12)
                + T("t-caption", "c-ink2", "Günlük limit tanımlı değil."))
          + sp(32)
          + div("col px20",
                div("card",
                    T("t-h2", "c-ink", "Günlük limit tanımlı değil") + sp(8)
                    + T("t-body", "c-ink2", "Bir limit olmadan kalan gösterilemez.")
                    + sp(24) + btn_s("Limit belirle")))
          + sp(24) + liste_baslik() + ROWS_180)
    + footer(btn_ekle()) + tabbar("bugun")))

# ---------------------------------------------------------------- 6. skeleton
bloklar.append(item(
    "E-10", "Bugün · yükleniyor (≥150ms)",
    "Skeleton yalnızca okuma 150ms'yi aşarsa çizilir. Parıldama (shimmer) "
    "YOK — animasyon yasağı. Oluk çizilir, dolgu çizilmez.",
    govde(header("Bugün", SET) + sp(32)
          + div("col px20",
                skeleton("96px", 18, 8)
                + skeleton("168px", 48, 24)
                + limitbar(0, 300, "skeleton")
                + sp(12) + skeleton("232px", 18, 0))
          + sp(32) + liste_baslik()
          + div("col px20",
                sp(16) + skeleton("100%", 24, 12) + skeleton("70%", 24, 12)
                + skeleton("85%", 24, 12) + skeleton("60%", 24, 0)))
    + footer(btn_ekle("disabled")) + tabbar("bugun")))

# ---------------------------------------------------------------- 7. hata
bloklar.append(item(
    "E-10", "Bugün · okuma hatası",
    "ErrorState: h2 + body + secondary 'Yeniden dene'. Teknik kod "
    "gösterilmez, 'Ayrıntıyı gör' altında saklanır. Kırmızı kullanılmaz.",
    govde(header("Bugün", SET) + sp(64)
          + div("col px20 mid-x",
                tally() + sp(24)
                + T("t-h2", "c-ink", "Kayıtlar açılamadı") + sp(8)
                + '<span class="t-body c-ink2 mid">Veriler bu cihazda tutuluyor'
                  ' ve şu an okunamadı.</span>'
                + sp(24) + btn_s("Yeniden dene", "default", "align-self:stretch")
                + sp(8) + btn_g("Ayrıntıyı gör", "default", "c-ink2",
                                "align-self:center"))
          ) + tabbar("bugun")))

# ---------------------------------------------------------------- 8. limit sorgu
bloklar.append(item(
    "E-10", "Bugün · limit kurulumu sorgusu (imza akışı)",
    "Ayda 5+ aşımdan sonra bir kez çıkar. Suç kullanıcıya değil kuruluma "
    "atılır. Toast değil Card; modal ASLA değil.",
    govde(header("Bugün", SET) + sp(32)
          + hero("bugün kalan", "60 ₺", "c-edge",
                 "Limitin 60 ₺ üzerindesin.", limitbar(360, 300))
          + div("col px20", sp(4) + T("t-label", "c-edge", "limit dışı"))
          + sp(24)
          + div("col px20",
                div("card",
                    div("row between",
                        T("t-h2", "c-ink", "Bu ay 6. limit aşımı")
                        + iconbtn("x", "Kartı kapat"))
                    + sp(8)
                    + T("t-body", "c-ink2", "Limit gerçekçi mi. Birlikte bakalım.")
                    + sp(24)
                    + btn_s("Limiti gözden geçir")))
          + sp(24) + liste_baslik()
          + spendrow("Restoran", "Kart · 19.50", "180 ₺", "overflow") + div("divider"))
    + footer(btn_ekle()) + tabbar("bugun")))

# ---------------------------------------------------------------- 9. profilleme
bloklar.append(item(
    "E-10", "Bugün · ProfilingPrompt görünür (2. gün)",
    "Günde en fazla 1 soru, toplam 3. 'Şimdi değil' ile 14 gün geri gelmez. "
    "Pano akışını kesmez, listenin üstünde durur.",
    govde(header("Bugün", SET) + sp(32)
          + hero("bugün kalan", "120 ₺", "c-ink",
                 "Bugün 180 ₺. Limitinin 120 ₺ altındasın.", limitbar(180, 300))
          + sp(24)
          + div("col px20",
                div("card",
                    T("t-h2", "c-ink", "Aylık gelirin hangi aralıkta") + sp(8)
                    + T("t-caption", "c-ink3", "Cevabın cihazda kalır.")
                    + sp(16)
                    + div("row wrap",
                          chip("30.000 ₺ altı") + chip("30.000-60.000 ₺")
                          + chip("60.000 ₺ üzeri") + chip("Söylemek istemiyorum"))
                    + div("row", btn_g("Şimdi değil", "default", "c-ink2",
                                       "align-self:flex-start;padding-left:0;padding-right:0"))))
          + sp(16) + liste_baslik() + ROWS_180)
    + footer(btn_ekle()) + tabbar("bugun")))

# ---------------------------------------------------------------- 10. toast + basili
bloklar.append(item(
    "E-10", "Bugün · kayıt sonrası Toast + basılı durumlar",
    "Toast 4 sn. Sol 3pt şerit Kiremit = limit dışı. Sekme ve satır "
    "'pressed' halleri burada: hover yok, tek geri bildirim bu.",
    govde(header("Bugün", SET) + sp(32)
          + hero("bugün kalan", "60 ₺", "c-edge",
                 "Limitin 60 ₺ üzerindesin.", limitbar(360, 300))
          + div("col px20", sp(4) + T("t-label", "c-edge", "limit dışı"))
          + sp(24) + liste_baslik()
          + spendrow("Kafe", "Kart · 08.40", "95 ₺") + div("divider-56")
          + spendrow("Ulaşım", "Kart · 09.05", "35 ₺", "pressed") + div("divider-56")
          + spendrow("Restoran", "Kart · 19.50", "180 ₺", "overflow") + div("divider"))
    + div("col px20", toast("180 ₺ kaydedildi · 60 ₺ limit dışı", "edge", "Geri al"),
          "padding-bottom:12px")
    + footer(btn_ekle("pressed")) + tabbar("bugun", "kayitlar")))

# ---------------------------------------------------------------- 11. uzun icerik
bloklar.append(item(
    "E-10", "Bugün · uzun tutar ve uzun metin taşma testi",
    "Kuruşlu en uzun literal (1.250.000,50 ₺) hem kahraman sayıda hem liste "
    "tutarında sınanır: tutar kırpılmaz, sütun genişler; kategori/not satırı "
    "kırpılır. Kahraman sayı 9 haneyi aşarsa 44pt → 28pt tek kademe düşer.",
    govde(header("Bugün", SET) + sp(32)
          + hero("bugün kalan", "1.250.000,50 ₺", "c-ink",
                 "Bugün 12.480 ₺. Limitinin 1.250.000,50 ₺ altındasın.",
                 limitbar(12480, 1262480), sayi_cls="t-h1")
          + sp(32) + liste_baslik()
          + spendrow("Kira ve ev", "Kart · 10.05 · Akşam yemeği, iki kişi, "
                     "arkadaşımla ödeme sonradan bölündü", "1.250.000,50 ₺")
          + div("divider-56")
          + spendrow("Abonelik", "Kart · 11.00 · 12/12 taksit", "1.041 ₺",
                     taksit=True)
          + div("divider-56")
          + spendrow("Alışkanlıklar", "Nakit · 12.30", "12.480 ₺") + div("divider"))
    + footer(btn_ekle()) + tabbar("bugun")))

# ---------------------------------------------------------------- 12. odak halleri
def _chip(metin, cls="chip", renk="c-ink2"):
    return div(cls + " shrink0", T("t-label", renk, metin))


ODAK = div("g-item", div("col",
    div("g-note",
        T("t-h2", "c-ink", "Odak (focus) hâlleri") + sp(8)
        + T("t-caption", "c-ink2",
            "tokens.md §6: 2pt Petrol #14484C dış halka, elemandan 2pt boşlukla, "
            "halkanın yarıçapı = elemanın yarıçapı + 2. Kaldırılmaz.")
        + sp(8)
        + T("t-caption", "c-ink2",
            "RN'de hover yoktur; odak halkası yalnız harici klavye, Switch Control "
            "ve TalkBack/VoiceOver gezinmesinde görünür — dokunmatik girişte çıkmaz.")
        + sp(24)
        + T("t-label", "c-ink2", "Button primary · focused (radius 12 → halka 14)")
        + sp(8) + div("focusring", btn_ekle())
        + sp(24)
        + T("t-label", "c-ink2", "Chip · focused (radius 16 → halka 18)")
        + sp(8)
        + div("row",
              div("focusring-pill", _chip("Kafe", "chip chip-sel", "c-acc"))
              + wsp(12) + div("focusring-pill", _chip("Market"))
              + wsp(12) + div("focusring-pill", _chip("Ulaşım")))
        + sp(8)
        + T("t-caption", "c-ink3", "Odak ile seçili aynı şey değildir: 'Kafe' seçili + odaklı, 'Market' yalnız odaklı.")
        + sp(24)
        + T("t-label", "c-ink2", "TabItem · focused (radius 12 → halka 14)")
        + sp(8) + tabbar("bugun", odak="kayitlar")
        + sp(8)
        + T("t-caption", "c-ink3",
            "TabItem içerik kutusu 48pt: 48 + 2pt boşluk + 2pt kenarlık = 56, yani tam "
            "bar yüksekliği. Halka bar içinde kalır, kırpma bağımlılığı yok; dokunma "
            "hedefi 48pt (≥44)."),
        "width:390px")))
bloklar.append(ODAK)

bloklar.append(note("Bu ekranda bilinçli kararlar", [
    "Çubuk doluluğa göre renk DEĞİŞTİRMEZ — dört doluluk hâli yan yana bunu kanıtlıyor.",
    "Taşma ayrı segment: eşiğin solu Petrol, sağı Kiremit. Ölçek yeniden hesaplanır, çubuk genişliği sabit kalır.",
    "Kırmızı (#8E2F20) bu ekranda hiç geçmez — yalnızca silme onayına ayrılmıştır.",
    "Ayarlar sağ üstte: sol üst köşe iOS geri kaydırmasıyla çakışır.",
    "'Harcama ekle' klavye/sekme üstünde sabit; ekranda tek birincil buton.",
    "Kategori ikonları daire zemine alınmaz, renk taşımaz — ayrım ikon + isimle.",
    "Safe area: üstte 48pt Dynamic Island şeridi, altta 32pt home indicator şeridi işaretli.",
    "Odak halkası ayrı bir şeritte toplandı: her karede tekrar çizmek yerine Button/Chip/TabItem için tek referans verildi.",
]))

page("E-10 · Bugün (Pano)",
     "Ürünün kalbi. 11 durum: dolu · %0 · %100 · limit dışı · limitsiz · "
     "yükleniyor · hata · limit sorgusu · profilleme · toast + basılı · taşma testi "
     "· artı odak (focus) hâlleri şeridi.",
     bloklar, "01-bugun.html")
