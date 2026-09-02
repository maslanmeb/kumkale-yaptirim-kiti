# -*- coding: utf-8 -*-
from gen_web_common import *
import os

OUT = "/home/claude/kumkale-site/ek"
os.makedirs(OUT, exist_ok=True)

def write(no, title, dayanak, body):
    html = page(no, title, dayanak, body)
    fname = f"ek-{str(no).zfill(2)}.html"
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname)

# ================= EK-1 =================
body = []
body.append(para(
    'Bu kurul, ders yılı başındaki ilk öğretmenler kurulu toplantısında oluşturulur ve yeni kurul '
    'oluşana kadar görevine devam eder.', cls="section-sub"))
body.append(meta_table([
    ("Eğitim ve Öğretim Yılı", text_field("egitimYili", "ör. 2026-2027")),
]))

body.append(section_title("A) Kurul Başkanı", "Müdürün görevlendirdiği müdür yardımcısı — Md.57/2-a"))
body.append(meta_table([
    ("Adı Soyadı", text_field("baskanAd")),
    ("Görevlendirme Tarihi", date_field("baskanTarih")),
]))

body.append(section_title("B) Öğretmen Üyeler", "Öğretmenler Kurulunda gizli oyla seçilir — Md.57/2-b"))
rows_html = []
labels = ["Asıl Üye 1", "Asıl Üye 2", "Asıl Üye 3", "Yedek Üye 1", "Yedek Üye 2", "Yedek Üye 3"]
header = '''    <table class="meta">
      <tr><td class="label" style="width:26%"></td><td class="label" style="width:38%">Adı Soyadı</td><td class="label" style="width:18%">Branşı</td><td class="label">Aldığı Oy</td></tr>
'''
trs = []
for i, lbl in enumerate(labels):
    trs.append(f'      <tr><td class="label">{lbl}</td><td>{text_field(f"ogrUye{i}_ad")}</td><td>{text_field(f"ogrUye{i}_brans")}</td><td>{text_field(f"ogrUye{i}_oy")}</td></tr>')
body.append(header + "\n".join(trs) + "\n    </table>\n")

body.append(section_title("C) Veli Üyesi", "Okul-Aile Birliğince kendi üyeleri arasından seçilir — Md.57/2-c"))
body.append(meta_table([
    ("Adı Soyadı", text_field("veliUyeAd")),
    ("Okul-Aile Birliğindeki Görevi", text_field("veliUyeGorev")),
]))

body.append(note_box(
    "Not",
    "Kurulun görevi yeni kurul oluşana kadar devam eder (Md.57/6). Rehber Öğretmen / Psikolojik "
    "Danışman kadrosu bulunmadığında kurul toplantılarına bu görevlinin katılımı aranmaz; ihtiyaç "
    "hâlinde kurul, RAM ile yazışma yoluyla görüş alabilir."
))
body.append(signature_block(["Öğretmenler Kurulu Kâtibi", "Kurul Başkanı", "Okul Müdürü (Onay)"]))

write(1, "ÖĞRENCİ DAVRANIŞLARINI DEĞERLENDİRME KURULU OLUŞTURMA TUTANAĞI", "Md.57", "\n".join(body))

# ================= EK-2 =================
body = []
body.append(meta_table([
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("Tarih", date_field("tarih")),
    ("Görüşmeyi Yapan Öğretmen", text_field("ogretmenAd")),
]))
body.append(section_title("Gözlenen Davranış", "Md.55/a listesinden ilgili madde belirtilerek"))
body.append(textarea("davranis", "Gözlenen davranışı yazınız...", rows=3))
body.append(para(
    "Görüşmede öğrenciden beklenen olumlu davranış açıklandı ve davranışın devamı hâlinde "
    "uygulanabilecek yaptırımlar (sözleşme imzalama, veli görüşmesi, kurula sevk) hakkında bilgi verildi."
))
body.append(section_title("Bu, öğrencinin bu eğitim-öğretim yılındaki kaçıncı sözlü uyarısıdır?"))
body.append(meta_table([("Sıra No", text_field("siraNo", "ör. 1"))]))
body.append(signature_block(["Öğrenci", "Görüşmeyi Yapan Öğretmen"]))

write(2, "SÖZLÜ UYARMA GÖRÜŞME NOTU", "Md.54/3-a — Uyarma sürecinin 1. aşaması", "\n".join(body))

# ================= EK-3 =================
body = []
body.append(meta_table([
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("Tarih", date_field("tarih")),
]))
body.append(section_title("Sözlü Uyarıya Konu Olan ve Sürdürülen Davranış"))
body.append(textarea("davranis", "Davranışı buraya yazınız...", rows=3))
body.append(para(
    "Ben, aşağıda kimliği belirtilen öğrenci, yukarıda belirtilen olumsuz davranışımı sürdürmeyeceğimi; "
    "okul kurallarına uyacağımı ve öğretmenim ile aşağıda birlikte belirlediğimiz olumlu davranışları "
    "göstermeye çalışacağımı kabul ve taahhüt ederim. Bu davranışı sürdürmem hâlinde velimin okula davet "
    "edileceğini ve gerekirse Öğrenci Davranışlarını Değerlendirme Kuruluna sevk edilebileceğimi biliyorum."
))
body.append(section_title("Birlikte Belirlenen Olumlu Davranış Hedefleri"))
body.append(dyn_list("Bir hedef yazınız..."))
body.append(signature_block(["Öğrenci", "Görüşmeyi Yapan Öğretmen", "Öğrenci Velisi (bilgilendirilmiştir)"]))

write(3, "ÖĞRENCİ SÖZLEŞMESİ", "Md.54/3-b — Uyarma sürecinin 2. aşaması (Yönetmelik EK-9 karşılığı)", "\n".join(body))

# ================= EK-4 =================
body = []
body.append(meta_table([
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("Görüşme Tarihi", date_field("gorusmeTarihi")),
    ("Veliye Davet Şekli ve Tarihi", text_field("davetSekli", "ör. telefonla, 12.09.2026")),
    ("Görüşmeye Katılan Okul Yöneticisi", text_field("yoneticiAd")),
    ("Görüşmeye Katılan Öğretmen(ler)", text_field("ogretmenAd")),
]))
body.append(note_box(
    "Rehber Öğretmen / Psikolojik Danışman katılımı",
    "Md.54/3-c uyarınca Rehber Öğretmen / Psikolojik Danışman &ldquo;varsa&rdquo; görüşmeye katılır. "
    "Kadro bulunmadığında bu alan boş bırakılabilir; görüşme okul yöneticisi ve öğretmen ile de yürütülebilir."
))
body.append(section_title("Öğrencinin Sürdürdüğü Olumsuz Davranış ve Daha Önce Uygulanan Aşamalar"))
body.append(textarea("davranisGecmis", "", rows=3))
body.append(section_title("Veliye Bildirilen Hususlar"))
body.append(para("Öğrencinin olumsuz davranışları ve davranış sürerse uygulanabilecek yaptırımlar (kınama, okul değiştirme dâhil) veliye sözlü olarak bildirilmiştir."))
body.append(section_title("Velinin Görüş ve Beyanı"))
body.append(textarea("veliGorus", "", rows=3))
body.append(section_title("Veli Toplantıya Geldi mi?"))
body.append(radio_group("veliGeldi", [("geldi", "Geldi"), ("gelmedi", "Gelmedi (bu tutanak tek başına düzenlenmiştir)")], "veliGeldi"))
body.append(signature_block(["Okul Yöneticisi", "Öğretmen", "Öğrenci Velisi"]))

write(4, "VELİ GÖRÜŞME TUTANAĞI", "Md.54/3-c — Uyarma sürecinin 3. aşaması", "\n".join(body))

# ================= EK-5 =================
body = []
body.append(meta_table([
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("Raporu Hazırlayan Öğretmen", text_field("ogretmenAd")),
    ("Tarih", date_field("tarih")),
]))
body.append(section_title("Sevk Gerekçesi"))
body.append(radio_group("sevkGerekce", [
    ("a", "Md.55/a — 3 aşamalı uyarma süreci tükendi, davranış sürüyor"),
    ("b", "Md.55/b — Doğrudan kınama gerektiren davranış"),
    ("c", "Md.55/c — Doğrudan okul değiştirme gerektiren davranış"),
], "sevkGerekce"))
body.append(section_title("Olayın / Davranışın Ayrıntılı Anlatımı", "Tarih, yer, tanıklar dâhil"))
body.append(textarea("olayAnlatim", "", rows=5))
body.append(section_title("Ekte Kurula Sunulan Belgeler"))
body.append(checkbox_group([
    ("ek2", "EK-2 Sözlü Uyarma Notu (varsa)"),
    ("ek3", "EK-3 Öğrenci Sözleşmesi (varsa)"),
    ("ek4", "EK-4 Veli Görüşme Tutanağı (varsa)"),
    ("diger", "Diğer kanıtlar / tanık beyanları / fotoğraf-belge:", "digerBelge"),
], "belge"))
body.append(section_title("Öğrencinin Bu Eğitim-Öğretim Yılındaki Önceki Yaptırım Geçmişi"))
body.append(radio_group("gecmis", [("yok", "Yok (ilk olay)"), ("var", "Var — aşağıda açıklayınız")], "gecmis"))
body.append(textarea("gecmisAciklama", "Varsa açıklayınız...", rows=2))
body.append(signature_block(["Raporu Hazırlayan Öğretmen", "Okul Müdürü (Kurula havale)"]))

write(5, "ÖĞRETMEN RAPORU VE KURULA SEVK FORMU", "Md.54/3-c (son cümle) ve Md.58/f", "\n".join(body))

# ================= EK-6 =================
body = []
body.append(meta_table([
    ("Toplantı Tarihi", date_field("toplantiTarihi")),
    ("Toplantı Saati", '<input type="time" id="toplantiSaati">'),
    ("Toplantı Yeri", text_field("toplantiYeri")),
    ("Çağrıyı Yapan (Kurul Başkanı)", text_field("cagriYapan")),
]))
body.append(section_title("Gündem", "Görüşülecek öğrenci/dosya ve ilgili EK-5 sevk tarihi"))
body.append(dyn_list("ör. Ahmet Y. — sınıfta kavga (EK-5 sevk tarihi: 14.09.2026)"))
body.append(section_title("Toplantıya Çağrılan Üyeler ve Tebliğ Tarihleri"))
labels = ["Kurul Başkanı", "Öğretmen Üye 1", "Öğretmen Üye 2", "Öğretmen Üye 3", "Veli Üyesi"]
trs = "\n".join(f'      <tr><td class="label" style="width:40%">{l}</td><td>{date_field(f"uyeTebligTarih{i}")}</td></tr>' for i, l in enumerate(labels))
body.append(f'    <table class="meta">\n{trs}\n    </table>\n')
body.append(note_box(
    "Katılım kuralı",
    "Şikâyetçi, zarar gören veya olumsuz davranışta bulunanla ikinci dereceye kadar akrabalığı olan "
    "üyeler bu toplantıya katılamaz (Md.59/2). Üyeler kabul edilebilir bir özrü olmadıkça katılmaktan "
    "kaçınamaz."
))
body.append(signature_block(["Kurul Başkanı"]))

write(6, "KURUL TOPLANTI ÇAĞRISI VE GÜNDEMİ", "Md.59/1", "\n".join(body))

# ================= EK-7 =================
body = []
body.append(meta_table([
    ("İfadesi Alınan Kişi", text_field("kisiAd")),
    ("Sıfatı", text_field("sifat", "ör. öğrenci, tanık")),
    ("Tarih", date_field("tarih")),
    ("Saat", '<input type="time" id="saat">'),
    ("İfadeyi Alan Kurul Başkanı", text_field("baskanAd")),
    ("Eşlik Eden Öğretmen", text_field("ogretmenAd")),
]))
body.append(para(
    "Rehber Öğretmen / Psikolojik Danışman normu bulunmadığında, Md.60/1 uyarınca ifade alma işlemine "
    "bir öğretmen eşlik eder.", cls="section-sub"
))
body.append(section_title("İfade Metni"))
body.append(textarea("ifadeMetni", "", rows=6))
body.append(section_title("Çağrıldığı Hâlde Gelmeme / İfade Vermeme Durumu"))
body.append(radio_group("cagriDurumu", [
    ("uyuldu", "Çağrıya uyuldu, ifade verildi"),
    ("uyulmadi", "Çağrıya uyulmadı (tutanakla tespit edilmiştir)"),
], "cagriDurumu"))
body.append(signature_block(["İfadesi Alınan Kişi", "Eşlik Eden Öğretmen", "Kurul Başkanı"]))

write(7, "İFADE ALMA TUTANAĞI", "Md.60/1-2", "\n".join(body))

# ================= EK-8 =================
body = []
body.append(meta_table([
    ("Karar No / Tarih", date_field("kararTarihi")),
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("Bu, öğrencinin bu davranışa ilişkin kaçıncı yaptırımı?", text_field("kacinciYaptirim", "ör. 1.")),
]))
body.append(section_title("İncelenen Davranış ve Dayanılan Yönetmelik Maddesi"))
body.append(f'    <table class="meta"><tr><td class="label" style="width:18%">Md.55 /</td><td>{text_field("maddeBendi", "a / b / c ...")}</td></tr></table>\n')
body.append(textarea("davranisAciklama", "Davranışı kısaca açıklayınız...", rows=2))
body.append(section_title("Yaptırım Takdirinde Değerlendirilen Hususlar", "Md.56/1"))
body.append(checkbox_group([
    ("nitelik", "Davranışın niteliği ve gerçekleştiği şartlar"),
    ("genel", "Öğrencinin genel durumu"),
    ("yascins", "Yaş / cinsiyet"),
    ("ders", "Derslerdeki ilgi ve başarı"),
    ("sosyal", "Sosyal / kültürel katılım"),
    ("gecmis", "Bu yıl içindeki önceki yaptırım geçmişi"),
], "husus"))
body.append(section_title("Kurul Kararı"))
body.append(radio_group("kararTuru", [
    ("uyarma", "Uyarma"), ("kinama", "Kınama"), ("okulDegistirme", "Okul Değiştirme"), ("yok", "Yaptırım gerekmiyor")
], "kararTuru"))
body.append(section_title("Kararın Gerekçesi (özet)"))
body.append(textarea("gerekce", "", rows=2))
body.append(meta_table([("Oylama Sonucu", text_field("oylamaSonucu", "ör. 4 kabul, 1 çekimser"))]))
body.append(section_title("Katılan Üyeler, Görüş ve İmzalar"))
labels = ["Kurul Başkanı", "Öğretmen Üye 1", "Öğretmen Üye 2", "Öğretmen Üye 3", "Veli Üyesi"]
trs = []
for i, l in enumerate(labels):
    trs.append(f'      <tr><td class="label" style="width:26%">{l}</td><td>{text_field(f"uyeGorus{i}", "görüş")}</td><td>{text_field(f"uyeImza{i}", "ad soyad / imza")}</td></tr>')
body.append('    <table class="meta">\n' + "\n".join(trs) + "\n    </table>\n")
body.append(section_title("Karara Katılmayan Üye(ler) Varsa Gerekçesi", "Md.60/3"))
body.append(textarea("katilmayanGerekce", "", rows=2))
body.append(section_title("Okul Müdürünün Onayı"))
body.append(radio_group("mudurOnay", [
    ("uygun", "Uygun bulundu, onaylandı"),
    ("uygunDegil", "Uygun bulunmadı, itirazla birlikte kurula iade edildi (Md.60/4)")
], "mudurOnay"))
body.append(signature_block(["Kurul Başkanı", "Okul Müdürü"]))

write(8, "ÖĞRENCİ DAVRANIŞLARINI DEĞERLENDİRME KURULU KARAR TUTANAĞI", "Md.60/3 (Yönetmelik EK-10 karşılığı)", "\n".join(body))

# ================= EK-9 =================
body = []
body.append(meta_table([
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("Karar Tarihi / No (EK-8)", text_field("kararNo")),
]))
body.append(section_title("Uygulanan Yaptırım"))
body.append(radio_group("yaptirim", [("uyarma", "Uyarma"), ("kinama", "Kınama"), ("okulDegistirme", "Okul Değiştirme")], "yaptirim"))
body.append(meta_table([
    ("Tebliğ Tarihi", date_field("tebligTarihi")),
    ("Tebliğ Şekli", '<select class="field" id="tebligSekli"><option value="">Seçiniz...</option><option>Elden</option><option>Telefonla</option><option>Posta (Tebligat Kanunu)</option><option>Bilgi ve iletişim araçlarıyla / SMS</option></select>'),
]))
body.append(para(
    "Yukarıda kimliği belirtilen öğrenci hakkında Öğrenci Davranışlarını Değerlendirme Kurulunca alınan "
    "ve okul müdürünce onaylanan karar tarafıma tebliğ edilmiştir. Karara karşı tebliğ tarihinden "
    "itibaren 5 (beş) iş günü içinde okul müdürlüğüne yazılı olarak itiraz edebileceğim konusunda "
    "bilgilendirildim (Md.56/11)."
))
body.append(section_title("Kararın Özeti"))
body.append(textarea("kararOzeti", "", rows=3))
body.append(note_box(
    "Veli çağrıya gelmezse (okul değiştirme kararı için)",
    "Md.62/2 uyarınca veli, karar tebliğ edilmek üzere okula çağrılır. Çağrıya uyulmazsa 7201 sayılı "
    "Tebligat Kanununa göre tebligat yapılır ve tebellüğ belgesi dosyada saklanır."
))
body.append(signature_block(["Okul Müdürü", "Öğrenci Velisi (veya Tebligat Kanununa göre tebliğ)"]))

write(9, "YAPTIRIM KARARININ VELİYE TEBLİĞ FORMU", "Md.62/1 (uyarma/kınama) — Md.62/2 (okul değiştirme)", "\n".join(body))

# ================= EK-10 =================
body = []
body.append(meta_table([
    ("İlçe Millî Eğitim Müdürlüğüne", text_field("ilceAd", "ör. Çanakkale / Merkez İlçe Millî Eğitim Müdürlüğüne")),
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("Okul Kurulu Karar Tarihi / No", text_field("kararNo")),
    ("Gönderme Tarihi", date_field("gondermeTarihi")),
]))
body.append(para(
    "İlgi: Okulumuz Öğrenci Davranışlarını Değerlendirme Kurulunun yukarıda tarih ve sayısı belirtilen "
    "kararı ile okul değiştirme yaptırımı uygulanmasına karar verilen öğrenciye ait dosya, Md.61 uyarınca "
    "onay için ekte gönderilmiştir."
))
body.append(section_title("Dosya Ekinde Gönderilen Belgeler", "Md.61/2"))
body.append(checkbox_group([
    ("ifade", "Yazılı ifadeler / savunma (EK-7)"),
    ("mahkeme", "Varsa mahkeme kararı ve soruşturmayla ilgili diğer belgeler"),
    ("kararOrnegi", "Öğrenci Davranışlarını Değerlendirme Kurulu Karar Örneği onaylı sureti (EK-8)"),
    ("itiraz", "İtiraz edilmişse itiraza ilişkin belgeler (EK-11)"),
    ("tebellug", "Kararların bildirildiğine ilişkin tebellüğ belgesi (EK-9)"),
    ("rapor", "Öğretmen Raporu / Kurula Sevk Formu (EK-5)"),
    ("diger", "Diğer:", "digerBelge"),
], "belge"))
body.append(note_box(
    "Hatırlatma",
    "İlçe kurulu, dosyanın kendisine bildirilmesinden itibaren en geç 5 iş günü içinde toplanır; karar "
    "verme süresi en geç 15 gündür (Md.64/3). İlçe kurulu ayrıca öğrencinin naklen gidebileceği okulu da "
    "belirler (Md.64/2-b)."
))
body.append(signature_block(["Okul Müdürü"]))

write(10, "İLÇE ÖĞRENCİ DAVRANIŞLARINI DEĞERLENDİRME KURULUNA GÖNDERME ÜST YAZISI VE DOSYA LİSTESİ",
      "Md.61/1-2 — yalnızca Okul Değiştirme kararlarında kullanılır", "\n".join(body))

# ================= EK-11 =================
body = []
body.append(f'    <div class="para" style="text-align:center; font-weight:bold; text-transform:uppercase;">{echo_field(" MÜDÜRLÜĞÜNE")}</div>\n')
body.append(meta_table([
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("İtiraz Edilen Kararın Tarihi / No", text_field("kararNo")),
    ("Kararın Tebliğ Tarihi", date_field("tebligTarihi")),
]))
body.append(para(
    "Yukarıda kimliği belirtilen velisi bulunduğum öğrenci hakkında verilen ve tarafıma tebliğ edilen "
    "karara aşağıda belirttiğim gerekçelerle itiraz ediyorum. İtirazımın incelenerek 5580 sayılı mevzuat "
    "ve Yönetmeliğin ilgili hükümleri çerçevesinde değerlendirilmesini arz ederim."
))
body.append(section_title("İtiraz Gerekçe(ler)i"))
body.append(dyn_list("Bir gerekçe yazınız..."))
body.append(meta_table([
    ("Dilekçe Tarihi", date_field("dilekceTarihi")),
    ("Velinin Adı Soyadı", text_field("veliAd")),
    ("Telefon / İletişim", '<input type="tel" id="iletisim" placeholder="0532 - 123 45 67">'),
]))
body.append(note_box(
    "Okul yönetimi için hatırlatma",
    "İtiraz işlemleri sonuçlanıncaya kadar yaptırım uygulanmaz (Md.56/12). Okul değiştirme kararına "
    "yapılan itirazlarda dilekçe, ilgili belgelerle birlikte en geç 5 iş günü içinde ilçe kuruluna "
    "gönderilir (Md.60/4, Md.61/2-c)."
))

write(11, "VELİ İTİRAZ DİLEKÇESİ ÖRNEĞİ", "Md.56/11-12 — Tebliğ tarihinden itibaren 5 iş günü içinde kullanılır", "\n".join(body))

# ================= EK-12 =================
body = []
body.append(meta_table([
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("Kaldırılması İstenen Yaptırım (Karar Tarihi/No)", text_field("kararNo")),
    ("Değerlendirme Toplantısı Tarihi", date_field("toplantiTarihi")),
]))
body.append(para(
    "Kurul, öğrencinin yaptırıma neden olan davranışı bir daha tekrarlamadığını ve olumlu davranışlar "
    "sergilediğini gözlemiş olup, aşağıdaki kararı almıştır."
))
body.append(section_title("Gözlemlere Dayalı Değerlendirme"))
body.append(textarea("degerlendirme", "", rows=4))
body.append(section_title("Kurul Kararı"))
body.append(radio_group("kaldirmaKarari", [
    ("kaldirildi", "Yaptırım dosyadan kaldırılmıştır"),
    ("kaldirilmadi", "Yaptırım kaldırılmamıştır (gerekçe belirtiniz)")
], "kaldirmaKarari"))
body.append(textarea("kaldirmamaGerekce", "Kaldırılmadıysa gerekçesini yazınız...", rows=2))
body.append(note_box("Süre", "Kaldırma kararı, en geç 5 iş günü içinde öğrencinin e-Okul sistemindeki dosyasından çıkarılır (Md.62/3)."))
body.append(section_title("Katılan Üyeler, Görüş ve İmzalar"))
labels = ["Kurul Başkanı", "Öğretmen Üye 1", "Öğretmen Üye 2", "Öğretmen Üye 3", "Veli Üyesi"]
trs = []
for i, l in enumerate(labels):
    trs.append(f'      <tr><td class="label" style="width:26%">{l}</td><td>{text_field(f"uyeGorus{i}", "görüş")}</td><td>{text_field(f"uyeImza{i}", "ad soyad / imza")}</td></tr>')
body.append('    <table class="meta">\n' + "\n".join(trs) + "\n    </table>\n")
body.append(signature_block(["Kurul Başkanı", "Okul Müdürü (Onay)"]))

write(12, "YAPTIRIMIN DOSYADAN KALDIRILMASI KARAR FORMU", "Md.62/3", "\n".join(body))

# ================= EK-13 =================
body = []
body.append(meta_table([
    ("Öğrencinin Adı Soyadı", text_field("ogrenciAd")),
    ("Sınıf / Şube", text_field("sinifSube")),
    ("Dosya Konusu", text_field("dosyaKonusu", "ör. Öğrenci Davranışlarını Değerlendirme Süreci Dosyası")),
    ("Dosyayı Düzenleyen", text_field("duzenleyen", "Kurul Başkanı")),
]))
body.append(section_title(
    "Dosya İçeriği — Dizi Pusulası",
    "Dosyaya konulan her belge için bir satır doldurun. Sıra numarası otomatik verilir; toplam belge ve "
    "sayfa sayısı aşağıda kendiliğinden hesaplanır."
))
body.append(note_box(
    "Neden gerekli?",
    "18/10/2019 tarihli ve 30922 sayılı Resmî Gazete'de yayımlanan Devlet Arşiv Hizmetleri Hakkında "
    "Yönetmelik ve Yönetmeliğin Md.75/5'i uyarınca, dosyalarda bulunan belgeler sıra numarası verilerek "
    "dizi pusulasına bağlanır; böylece dosyanın eksiksizliği ve belge sırası her zaman denetlenebilir "
    "hâlde tutulur."
))
body.append(note_box(
    "Dosyada Hangi Ekler Bulunmalı? (örnek liste)",
    '<strong>Zorunlu ekler</strong> — her dosyada mutlaka bulunmalı:'
    '<ul style="margin:4px 0 8px 18px; padding:0;">'
    '<li><a href="ek-05.html">EK-5</a> Öğretmen Raporu / Kurula Sevk Formu</li>'
    '<li><a href="ek-06.html">EK-6</a> Kurul Toplantı Çağrısı ve Gündemi</li>'
    '<li><a href="ek-07.html">EK-7</a> İfade Alma Tutanağı</li>'
    '<li><a href="ek-08.html">EK-8</a> Kurul Karar Tutanağı</li>'
    '<li><a href="ek-09.html">EK-9</a> Kararın Veliye Tebliğ Formu</li>'
    '</ul>'
    '<strong>Duruma göre zorunlu</strong> — ilgili durum oluştuysa mutlaka eklenmeli:'
    '<ul style="margin:4px 0 8px 18px; padding:0;">'
    '<li><a href="ek-02.html">EK-2</a>, <a href="ek-03.html">EK-3</a>, <a href="ek-04.html">EK-4</a> — uyarma süreci uygulandıysa</li>'
    '<li><a href="ek-10.html">EK-10</a> — karar okul değiştirme ise</li>'
    '<li><a href="ek-11.html">EK-11</a> — veli itiraz ettiyse</li>'
    '<li><a href="ek-12.html">EK-12</a> — yaptırım sonradan kaldırıldıysa</li>'
    '</ul>'
    '<strong>Tavsiye edilen ekler</strong> — yönetmelikte doğrudan istenmez, iyi uygulama için önerilir:'
    '<ul style="margin:4px 0 0 18px; padding:0;">'
    '<li>Olaya ilişkin kanıt, tanık beyanı, fotoğraf veya kamera görüntüsü dökümü (varsa)</li>'
    '<li>Öğrencinin önceki yıllara ait yaptırım kayıtlarının özeti</li>'
    '<li>Rehberlik/RAM yönlendirme yazışmaları (varsa)</li>'
    '<li>Veliyle yapılan ek yazışmalar (SMS, e-posta çıktısı vb.)</li>'
    '</ul>'
))
body.append('''    <datalist id="ekTurleri">
      <option value="EK-1 Kurul Oluşturma Tutanağı">
      <option value="EK-2 Sözlü Uyarma Görüşme Notu">
      <option value="EK-3 Öğrenci Sözleşmesi">
      <option value="EK-4 Veli Görüşme Tutanağı">
      <option value="EK-5 Öğretmen Raporu / Kurula Sevk Formu">
      <option value="EK-6 Kurul Toplantı Çağrısı ve Gündemi">
      <option value="EK-7 İfade Alma Tutanağı">
      <option value="EK-8 Kurul Karar Tutanağı">
      <option value="EK-9 Kararın Veliye Tebliğ Formu">
      <option value="EK-10 İlçe Kuruluna Gönderme Üst Yazısı">
      <option value="EK-11 Veli İtiraz Dilekçesi">
      <option value="EK-12 Yaptırımın Dosyadan Kaldırılması Karar Formu">
      <option value="Diğer (özgün belge)">
    </datalist>
    <table class="dizi-table">
      <thead>
        <tr>
          <th style="width:6%">Sıra</th>
          <th style="width:13%">Belge Tarihi</th>
          <th style="width:32%">Belge Türü / Adı</th>
          <th style="width:9%">Sayfa Sayısı</th>
          <th style="width:28%">Açıklama</th>
          <th style="width:12%"></th>
        </tr>
      </thead>
      <tbody id="diziBody"></tbody>
      <tfoot>
        <tr>
          <td colspan="2" style="text-align:right;">TOPLAM</td>
          <td><span class="dizi-toplam-belge">1</span> belge</td>
          <td><span class="dizi-toplam-sayfa">1</span> sayfa</td>
          <td colspan="2"></td>
        </tr>
      </tfoot>
    </table>
    <button type="button" class="dizi-add-row" data-target="diziBody">+ Satır Ekle</button>
''')
body.append(signature_block(["Düzenleyen (Kurul Başkanı)", "Kontrol Eden (Okul Müdürü)"]))

write(13, "DOSYA DİZİ PUSULASI", "Md.75/5 — Devlet Arşiv Hizmetleri Hakkında Yönetmelik", "\n".join(body))

print("ALL DONE")
