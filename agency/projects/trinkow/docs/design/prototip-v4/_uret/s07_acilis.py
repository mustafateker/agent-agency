# -*- coding: utf-8 -*-
"""E-00 · Açılış (splash) — sistem yüzeyi.
tokens.md §10: zemin `bg`, ortada wordmark 26pt `text`, "w" sağında topuz
`primary`. Animasyon YOK. Ekranda başka hiçbir şey yoktur — yükleniyor
göstergesi, sürüm numarası, slogan, telif satırı hiçbiri konmaz.

Monogram (T + topuz) splash'ta değil uygulama ikonundadır; sayfanın
ikinci birimi onu gösterir ve o birim RN'e kodlanmaz (kabuk bölgesi).
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from lib import device, page

OUT = pathlib.Path(__file__).parent.parent / "07-acilis.html"

# ---- wordmark: Poppins SemiBold 26pt (t-h1) + 8pt topuz, "w"nin sağında ----
WORDMARK = '''          <div class="esnek kolon orta" style="justify-content:center">
            <div class="satir" style="align-items:flex-start">
              <div class="t-h1">Trinkow</div>
              <div class="w4"></div>
              <div class="kolon">
                <div class="h8"></div>
                <div class="nokta" style="background-color:var(--primary)"></div>
              </div>
            </div>
          </div>'''

# ---- monogram (varliklar.md: 100×100 ızgara, T + topuz, keskin köşe) ----
def monogram(renk="#FFFFFF", topuz="#FFFFFF", boy=104):
    return f'''<svg width="{boy}" height="{boy}" viewBox="0 0 100 100" role="img" aria-label="Trinkow monogramı">
          <rect x="18" y="21" width="54" height="15" fill="{renk}"/>
          <rect x="37.5" y="21" width="15" height="58" fill="{renk}"/>
          <circle cx="78" cy="26.5" r="9" fill="{topuz}"/>
        </svg>'''


def ikon_kutusu(boy, radius):
    return (f'<div style="width:{boy}px;height:{boy}px;border-radius:{radius}px;'
            f'background-image:linear-gradient(180deg,#3B82F6 0%,#2F68C5 100%);'
            f'display:flex;align-items:center;justify-content:center;'
            f'box-shadow:0 16px 32px -8px rgba(28,57,142,0.22),0 4px 8px -2px rgba(28,57,142,0.12)">'
            f'{monogram(boy=int(boy * 0.58))}</div>')


MARKA_BIRIM = f'''    <div class="sahne-birim">
      <div class="baslik-etiket">MONOGRAM <span>· uygulama ikonu · RN'e kodlanmaz</span></div>
      <div style="width:414px;display:flex;flex-direction:column;align-items:center;
                  background:rgba(255,255,255,0.62);border-radius:32px;padding:32px 24px">
        <div style="display:flex;flex-direction:row;align-items:flex-end;gap:24px">
          {ikon_kutusu(160, 36)}
          {ikon_kutusu(88, 20)}
          {ikon_kutusu(48, 11)}
        </div>
        <div style="height:32px"></div>
        <div style="display:flex;flex-direction:row;align-items:center;gap:32px">
          <div style="width:104px;height:104px;background:#FFFFFF;border-radius:24px;
                      display:flex;align-items:center;justify-content:center;
                      box-shadow:0 8px 16px -4px rgba(28,57,142,0.16)">
            {monogram("#1C398E", "#3B82F6", 64)}
          </div>
          <div style="width:104px;height:104px;background:#1C398E;border-radius:24px;
                      display:flex;align-items:center;justify-content:center">
            {monogram("#FFFFFF", "#FFFFFF", 64)}
          </div>
        </div>
      </div>
      <div class="not-kutu">
        <b>Monogram:</b> 100×100 ızgara, T cap-height 58, taban çizgisi y=79, kol x 18→72,
        kol üstü y=21; topuz çap 18, merkez (78, 26.5). Köşeler <b>keskin</b>
        (<code>varliklar.md</code>) — clay'in yumuşaklığına karşı markanın sert imzası.
        <br /><br />
        <b>İzinli üç kullanım:</b> tek renk <code>text</code> (açık zemin) · tek renk
        <code>#FFFFFF</code> (koyu zemin) · iki renk (T <code>#FFFFFF</code> + topuz
        <code>#3B82F6</code>). Uygulama ikonunda zemin <code>grad.action</code>,
        saydamlık yoktur, köşe yuvarlatması <b>çizilmez</b> — platform maskeler.
        Gölge, kontur, esnetme, döndürme yasak.
      </div>
    </div>
'''

units = "".join([
    device("AÇILIŞ", "E-00 · varsayılan", WORDMARK, note=
           "<b>Ekranda üç şey var:</b> zemin, kelime markası, topuz. Yükleniyor göstergesi, slogan, "
           "sürüm numarası, telif satırı <b>yoktur</b> — bu ekran okunmaz, sadece görülür. "
           "<b>Süre:</b> hedef ≤ 600ms (veritabanı açılışı). Bu sürede animasyon <b>çalıştırılmaz</b>; "
           "yarım kalan bir hareket, hareketsizlikten daha ucuz görünür. 600ms'yi aşarsa ekran aynı kalır, "
           "3sn üst sınırında E-10'a geçilir ve veri <b>iskeletle</b> beklenir — kullanıcı splash'ta hapis kalmaz. "
           "İlk açılışta sonraki ekran E-01 (onboarding), sonrakilerde E-10.<br /><br />"
           "<b>Topuz nerede:</b> \"Trinkow\"un son harfi \"w\"nin sağında, 8pt <code>primary</code> daire, "
           "x-height hizasında. Bu, kahraman göstergedeki topuzun ta kendisidir — marka işareti ile ürünün "
           "ana nesnesi aynı şeydir. Logo kilidinin iç geometrisi (4pt boşluk) düzen ritmi değil "
           "<b>marka ölçüsüdür</b> (tokens §10)."),
    MARKA_BIRIM,
])

OUT.write_text(page(
    "Trinkow · Açılış — prototip v4",
    "E-00 · Açılış (splash)",
    "Sistem yüzeyi · animasyonsuz · 390×844 · claymorphism",
    units), encoding="utf-8")
print("yazıldı:", OUT)
