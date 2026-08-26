# Yaptırım Süreçleri Uygulama Kiti

Ortaokul/imam-hatip ortaokulu öğrenci davranışları için uyarma – kınama – okul değiştirme
süreçlerini yöneten, tarayıcıda doldurulabilir ve doğrudan PDF olarak kaydedilebilir statik
web sitesi. MEB Okul Öncesi Eğitim ve İlköğretim Kurumları Yönetmeliği Md.54-65 esas alınmıştır.

## Yapı

```
index.html          → Ana sayfa: tıklanabilir akış şeması + tüm belgelere erişim
kilavuz.html         → Uygulama kılavuzunun okunabilir web sürümü
ek/ek-01.html … ek-12.html → Doldurulabilir 12 form (A4, yazdır/PDF al)
assets/style.css     → Ortak stil
assets/app.js        → Ortak davranışlar (otomatik büyüyen kutular, dinamik listeler,
                        kapatılabilir bilgi kutuları, okul adı hatırlama)
assets/akis_semasi_interactive.svg → Kaynak şema (index.html içine gömülü kopyası kullanılır)
netlify.toml         → Netlify yayın ayarları
```

## Yayın

Bu depo Netlify'a bağlandığında `netlify.toml` içindeki ayarlarla otomatik yayınlanır.
Kök dizin doğrudan statik site olarak servis edilir, build adımı gerekmez.

## Geliştirme notları

- Tüm formlar istemci tarafında (JavaScript) çalışır; hiçbir veri sunucuya gönderilmez.
- Okul adı `localStorage` üzerinde saklanır ve tüm sayfalarda hatırlanır.
- 12 formun HTML'i `gen_web_forms.py` + `gen_web_common.py` ile üretilmiştir; içerik
  değişikliği gerektiğinde bu betikler güncellenip yeniden çalıştırılabilir.
- Akış şeması `build_flow_web.py` ile üretilir (Python + cairosvg gerektirir).
