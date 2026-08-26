import textwrap

W, H = 1240, 1780
svg_parts = []

NAVY = "#1F3864"
GRAY = "#595959"
LIGHT_GRAY = "#EDEDED"
AMBER_FILL, AMBER_STROKE, AMBER_TEXT = "#FDEBD0", "#D68910", "#7E4E0B"
CORAL_FILL, CORAL_STROKE, CORAL_TEXT = "#FDE3D8", "#C0562A", "#7A3013"
RED_FILL, RED_STROKE, RED_TEXT = "#FADBD8", "#C0392B", "#78241C"
GREEN_FILL, GREEN_STROKE, GREEN_TEXT = "#D5F0DD", "#1E8449", "#145A32"
BLUE_FILL, BLUE_STROKE, BLUE_TEXT = "#D6E4F0", "#2E5C8A", "#1B3A57"
GRAY_FILL, GRAY_STROKE, GRAY_TEXT = "#ECECEC", "#7F8C8D", "#4D5656"
WHITE = "#FFFFFF"

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def box(x, y, w, h, lines, fill, stroke, textcolor, bold_first=True, fs=15.5, rx=10, sw=1.6, align="middle"):
    cx = x + w / 2
    n = len(lines)
    line_h = fs + 5
    start_y = y + h/2 - (n-1)*line_h/2 + fs*0.32
    tx = cx if align == "middle" else x + 14
    anchor = "middle" if align == "middle" else "start"
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>']
    for i, ln in enumerate(lines):
        w_font = "700" if (bold_first and i == 0) else "400"
        fs_line = fs if (bold_first and i == 0) else fs - 1.5
        yy = start_y + i*line_h
        parts.append(f'<text x="{tx}" y="{yy}" text-anchor="{anchor}" font-family="Calibri, Arial, sans-serif" font-size="{fs_line}" font-weight="{w_font}" fill="{textcolor}">{esc(ln)}</text>')
    return "\n".join(parts)

def diamond(cx, cy, w, h, lines, fill=GRAY_FILL, stroke=GRAY_STROKE, textcolor=GRAY_TEXT, fs=13.5):
    pts = f"{cx},{cy-h/2} {cx+w/2},{cy} {cx},{cy+h/2} {cx-w/2},{cy}"
    n = len(lines)
    line_h = fs + 4
    start_y = cy - (n-1)*line_h/2 + fs*0.32
    parts = [f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>']
    for i, ln in enumerate(lines):
        yy = start_y + i*line_h
        parts.append(f'<text x="{cx}" y="{yy}" text-anchor="middle" font-family="Calibri, Arial, sans-serif" font-size="{fs}" font-weight="600" fill="{textcolor}">{esc(ln)}</text>')
    return "\n".join(parts)

def arrow(x1, y1, x2, y2, color=GRAY, sw=1.8, dash=None, label=None, lx=None, ly=None, fs=12.5, label_anchor="middle"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    parts = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}"{d} marker-end="url(#arrow)"/>']
    if label:
        lx = lx if lx is not None else (x1+x2)/2
        ly = ly if ly is not None else (y1+y2)/2 - 6
        parts.append(f'<rect x="{lx-2}" y="{ly-fs}" width="1" height="1" fill="none"/>')
        parts.append(f'<text x="{lx}" y="{ly}" text-anchor="{label_anchor}" font-family="Calibri, Arial, sans-serif" font-size="{fs}" font-weight="600" fill="{color}">{esc(label)}</text>')
    return "\n".join(parts)

def elbow(points, color=GRAY, sw=1.8, dash=None, label=None, lx=None, ly=None, fs=12.5):
    pts = " ".join(f"{x},{y}" for x,y in points[:-1])
    d = f' stroke-dasharray="{dash}"' if dash else ""
    path_pts = " L ".join(f"{x} {y}" for x,y in points)
    parts = [f'<path d="M {path_pts}" fill="none" stroke="{color}" stroke-width="{sw}"{d} marker-end="url(#arrow)"/>']
    if label:
        parts.append(f'<text x="{lx}" y="{ly}" text-anchor="middle" font-family="Calibri, Arial, sans-serif" font-size="{fs}" font-weight="600" fill="{color}">{esc(label)}</text>')
    return "\n".join(parts)

def hlink(href, svg_fragment, title=None):
    t = f'<title>{esc(title)}</title>' if title else ""
    return f'<a href="{href}" class="hotspot">{t}{svg_fragment}</a>'

def note(x, y, w, h, title, text_lines, fill="#FFF6D9", stroke="#BF8F00", textcolor="#7F6000"):
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>',
             f'<rect x="{x}" y="{y}" width="6" height="{h}" fill="{stroke}"/>']
    ty = y + 22
    parts.append(f'<text x="{x+18}" y="{ty}" font-family="Calibri, Arial, sans-serif" font-size="13.5" font-weight="700" fill="{textcolor}">{esc(title)}</text>')
    line_h = 17
    for i, ln in enumerate(text_lines):
        yy = ty + 22 + i*line_h
        parts.append(f'<text x="{x+18}" y="{yy}" font-family="Calibri, Arial, sans-serif" font-size="12.5" fill="{textcolor}">{esc(ln)}</text>')
    return "\n".join(parts)

def wraptext(s, width=34):
    return textwrap.wrap(s, width)

parts = []

parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{WHITE}"/>')
parts.append(f'''<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9Z" fill="{GRAY}"/></marker>
<marker id="arrowNavy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9Z" fill="{NAVY}"/></marker></defs>''')
parts.append('''<style>
  a.hotspot { cursor: pointer; }
  a.hotspot rect { transition: filter .12s ease, stroke-width .12s ease; }
  a.hotspot:hover rect { filter: brightness(0.94); stroke-width: 3; }
  a.hotspot:focus rect { outline: 2px solid #2b6cb0; }
</style>''')

# ---- Header ----
parts.append(f'<rect x="0" y="0" width="{W}" height="86" fill="{NAVY}"/>')
parts.append(f'<text x="{W/2}" y="36" text-anchor="middle" font-family="Calibri, Arial, sans-serif" font-size="24" font-weight="700" fill="white">İLKÖĞRETİM KURUMLARI ÖDDK SÜRECİ — TEK SAYFA AKIŞ ŞEMASI</text>')
parts.append(f'<text x="{W/2}" y="62" text-anchor="middle" font-family="Calibri, Arial, sans-serif" font-size="13.5" fill="#CFDAE8">Dayanak: MEB Okul Öncesi Eğitim ve İlköğretim Kurumları Yönetmeliği, Md. 54-65  •  Her kutuya tıklayarak ilgili belgeye gidebilirsiniz</text>')

# ---- Start ----
start_x, start_y, start_w, start_h = W/2-170, 110, 340, 56
parts.append(box(start_x, start_y, start_w, start_h, ["Olumsuz davranış gözlemlendi"], NAVY, NAVY, WHITE, fs=16))

# ---- First decision diamond ----
d1_cx, d1_cy = W/2, 232
parts.append(arrow(W/2, start_y+start_h, d1_cx, d1_cy-58, color=GRAY))
parts.append(diamond(d1_cx, d1_cy, 300, 108, ["Davranış Md.55'te", "hangi grupta?"], fs=14.5))

# ---- Three category boxes ----
col_y = 400
colA_x, colB_x, colC_x = 175, W/2, 1065
box_w = 300

parts.append(box(colA_x-box_w/2, col_y, box_w, 62, ["a) Uyarma davranışı", "(Md.55/a)"], AMBER_FILL, AMBER_STROKE, AMBER_TEXT, fs=15))
parts.append(box(colB_x-box_w/2, col_y, box_w, 62, ["b) Kınama davranışı", "(Md.55/b)"], CORAL_FILL, CORAL_STROKE, CORAL_TEXT, fs=15))
parts.append(box(colC_x-box_w/2, col_y, box_w, 62, ["c) Okul değiştirme davranışı", "(Md.55/c)"], RED_FILL, RED_STROKE, RED_TEXT, fs=15))

parts.append(elbow([(d1_cx-150, d1_cy), (colA_x, d1_cy), (colA_x, col_y)], color=AMBER_STROKE))
parts.append(arrow(d1_cx, d1_cy+54, colB_x, col_y, color=CORAL_STROKE))
parts.append(elbow([(d1_cx+150, d1_cy), (colC_x, d1_cy), (colC_x, col_y)], color=RED_STROKE))

# ---- Uyarma escalation ladder (left column) ----
step_w = 300
y1 = col_y + 62 + 40
parts.append(arrow(colA_x, col_y+62, colA_x, y1, color=AMBER_STROKE))
parts.append(hlink("ek/ek-02.html", box(colA_x-step_w/2, y1, step_w, 58, ["1) Sözlü Uyarma", "EK-2"], WHITE, AMBER_STROKE, AMBER_TEXT, fs=15), "EK-2: Sözlü Uyarma Görüşme Notu"))

dy1 = y1 + 58 + 56
parts.append(arrow(colA_x, y1+58, colA_x, dy1-39, color=AMBER_STROKE))
parts.append(diamond(colA_x, dy1, 170, 78, ["Davranış", "sürüyor mu?"], fill=AMBER_FILL, stroke=AMBER_STROKE, textcolor=AMBER_TEXT, fs=13))

y2 = dy1 + 42 + 40
parts.append(arrow(colA_x, dy1+39, colA_x, y2, color=AMBER_STROKE, label="Evet", lx=colA_x+34, ly=(dy1+39+y2)/2))
parts.append(hlink("ek/ek-03.html", box(colA_x-step_w/2, y2, step_w, 58, ["2) Öğrenci Sözleşmesi", "EK-3"], WHITE, AMBER_STROKE, AMBER_TEXT, fs=15), "EK-3: Öğrenci Sözleşmesi"))

dy2 = y2 + 58 + 56
parts.append(arrow(colA_x, y2+58, colA_x, dy2-39, color=AMBER_STROKE))
parts.append(diamond(colA_x, dy2, 170, 78, ["Davranış", "sürüyor mu?"], fill=AMBER_FILL, stroke=AMBER_STROKE, textcolor=AMBER_TEXT, fs=13))

y3 = dy2 + 42 + 40
parts.append(arrow(colA_x, dy2+39, colA_x, y3, color=AMBER_STROKE, label="Evet", lx=colA_x+34, ly=(dy2+39+y3)/2))
parts.append(hlink("ek/ek-04.html", box(colA_x-step_w/2, y3, step_w, 58, ["3) Veli Görüşmesi", "EK-4"], WHITE, AMBER_STROKE, AMBER_TEXT, fs=15), "EK-4: Veli Görüşme Tutanağı"))

dy3 = y3 + 58 + 56
parts.append(arrow(colA_x, y3+58, colA_x, dy3-39, color=AMBER_STROKE))
parts.append(diamond(colA_x, dy3, 170, 78, ["Davranış", "sürüyor mu?"], fill=AMBER_FILL, stroke=AMBER_STROKE, textcolor=AMBER_TEXT, fs=13))

# "Hayır" exits -> small terminator pill to the right of each diamond
def hayir_pill(dcy):
    px = colA_x + 85 + 12
    pw = 182
    ph = 46
    parts.append(arrow(colA_x+85, dcy, px, dcy, color=GRAY, sw=1.6))
    parts.append(box(px, dcy-ph/2, pw, ph, ["Hayır:", "kayda geçirilir, biter"], LIGHT_GRAY, GRAY, GRAY_TEXT, bold_first=True, fs=12))

hayir_pill(dy1)
hayir_pill(dy2)
hayir_pill(dy3)

# ---- Merge point: Kurula Sevk ----
merge_cx, merge_y = W/2, dy3 + 42 + 70
parts.append(hlink("ek/ek-05.html", box(merge_cx-190, merge_y, 380, 62, ["Öğretmen Raporu / Kurula Sevk", "EK-5"], NAVY, NAVY, WHITE, fs=16), "EK-5: Öğretmen Raporu / Kurula Sevk Formu"))

parts.append(elbow([(colA_x, dy3+39), (colA_x, merge_y+31), (merge_cx-190, merge_y+31)], color=AMBER_STROKE, label="Evet", lx=colA_x-40, ly=dy3+39+40))
parts.append(arrow(colB_x, col_y+62, merge_cx, merge_y, color=CORAL_STROKE))
parts.append(elbow([(colC_x, col_y+62), (colC_x, merge_y+31), (merge_cx+190, merge_y+31)], color=RED_STROKE))

# ---- Kurul process chain ----
cy = merge_y + 62 + 46
parts.append(arrow(merge_cx, merge_y+62, merge_cx, cy, color=NAVY))
parts.append(hlink("ek/ek-06.html", box(merge_cx-190, cy, 380, 56, ["Kurul Toplantı Çağrısı ve Gündemi — EK-6", "(en geç 5 iş günü içinde çağrılır)"], BLUE_FILL, BLUE_STROKE, BLUE_TEXT, fs=14), "EK-6: Kurul Toplantı Çağrısı ve Gündemi"))

cy2 = cy + 56 + 44
parts.append(arrow(merge_cx, cy+56, merge_cx, cy2, color=BLUE_STROKE))
parts.append(hlink("ek/ek-07.html", box(merge_cx-190, cy2, 380, 56, ["İfade Alma Tutanağı — EK-7", "(öğrenci ve tanıklar)"], BLUE_FILL, BLUE_STROKE, BLUE_TEXT, fs=14), "EK-7: İfade Alma Tutanağı"))

cy3 = cy2 + 56 + 44
parts.append(arrow(merge_cx, cy2+56, merge_cx, cy3, color=BLUE_STROKE))
parts.append(hlink("ek/ek-08.html", box(merge_cx-190, cy3, 380, 56, ["Kurul Karar Tutanağı — EK-8", "(en geç 5 iş günü içinde karara bağlanır)"], BLUE_FILL, BLUE_STROKE, BLUE_TEXT, fs=14), "EK-8: Kurul Karar Tutanağı"))

# ---- Karar türü decision ----
d2_cy = cy3 + 56 + 66
parts.append(arrow(merge_cx, cy3+56, merge_cx, d2_cy-56, color=BLUE_STROKE))
parts.append(diamond(merge_cx, d2_cy, 260, 108, ["Karar türü?"], fs=15))

# ---- Left branch: Uyarma/Kınama ----
lb_x = merge_cx - 330
by1 = d2_cy + 54 + 44
parts.append(elbow([(merge_cx-130, d2_cy), (lb_x, d2_cy), (lb_x, by1)], color=CORAL_STROKE, label="Uyarma / Kınama", lx=merge_cx-260, ly=d2_cy-14))
parts.append(box(lb_x-155, by1, 310, 56, ["Okul Müdürünün Onayı"], CORAL_FILL, CORAL_STROKE, CORAL_TEXT, fs=14.5))

by2 = by1 + 56 + 40
parts.append(arrow(lb_x, by1+56, lb_x, by2, color=CORAL_STROKE))
parts.append(hlink("ek/ek-09.html", box(lb_x-155, by2, 310, 56, ["Veliye Tebliğ — EK-9"], CORAL_FILL, CORAL_STROKE, CORAL_TEXT, fs=14.5), "EK-9: Kararın Veliye Tebliğ Formu"))

by3 = by2 + 56 + 40
parts.append(arrow(lb_x, by2+56, lb_x, by3, color=CORAL_STROKE))
parts.append(box(lb_x-155, by3, 310, 50, ["e-Okul sistemine işlenir"], CORAL_FILL, CORAL_STROKE, CORAL_TEXT, fs=14))

# ---- Right branch: Okul Değiştirme ----
rb_x = merge_cx + 330
ry1 = d2_cy + 54 + 44
parts.append(elbow([(merge_cx+130, d2_cy), (rb_x, d2_cy), (rb_x, ry1)], color=RED_STROKE, label="Okul Değiştirme", lx=merge_cx+270, ly=d2_cy-14))
parts.append(hlink("ek/ek-10.html", box(rb_x-155, ry1, 310, 62, ["İlçe Kuruluna Gönderme — EK-10", "(en geç 5 iş günü)"], RED_FILL, RED_STROKE, RED_TEXT, fs=13.5), "EK-10: İlçe Kuruluna Gönderme Üst Yazısı"))

ry2 = ry1 + 62 + 40
parts.append(arrow(rb_x, ry1+62, rb_x, ry2, color=RED_STROKE))
parts.append(box(rb_x-155, ry2, 310, 62, ["İlçe Kurulu Kararı", "(≤5 iş günü toplanır, ≤15 gün karar)"], RED_FILL, RED_STROKE, RED_TEXT, fs=13.5))

ry3 = ry2 + 62 + 40
parts.append(arrow(rb_x, ry2+62, rb_x, ry3, color=RED_STROKE))
parts.append(hlink("ek/ek-09.html", box(rb_x-155, ry3, 310, 56, ["Veliye Tebliğ — EK-9"], RED_FILL, RED_STROKE, RED_TEXT, fs=14.5), "EK-9: Kararın Veliye Tebliğ Formu"))

ry4 = ry3 + 56 + 40
parts.append(arrow(rb_x, ry3+56, rb_x, ry4, color=RED_STROKE))
parts.append(box(rb_x-155, ry4, 310, 50, ["e-Okul sistemine işlenir"], RED_FILL, RED_STROKE, RED_TEXT, fs=14))

# ---- Merge both branches into itiraz decision ----
final_y = max(by3+50, ry4+50) + 70
parts.append(elbow([(lb_x, by3+50), (lb_x, final_y-54), (merge_cx, final_y-54)], color=GRAY))
parts.append(elbow([(rb_x, ry4+50), (rb_x, final_y-54), (merge_cx, final_y-54)], color=GRAY))
parts.append(diamond(merge_cx, final_y, 300, 108, ["Veli itiraz etti mi?", "(tebliğden itibaren 5 iş günü)"], fs=13.5))

# Evet -> itiraz box
itr_x = merge_cx + 330
itr_y = final_y - 30
parts.append(elbow([(merge_cx+150, final_y), (itr_x, final_y), (itr_x, itr_y+30)], color=GRAY_STROKE, label="Evet", lx=merge_cx+150, ly=final_y-12))
parts.append(hlink("ek/ek-11.html", box(itr_x-160, itr_y, 320, 62, ["İtiraz Dilekçesi — EK-11", "(itiraz sonuçlanana dek yaptırım uygulanmaz)"], GRAY_FILL, GRAY_STROKE, GRAY_TEXT, fs=13), "EK-11: Veli İtiraz Dilekçesi Örneği"))

# Hayır -> tamamlandı
done_y = final_y + 54 + 46
parts.append(arrow(merge_cx, final_y+54, merge_cx, done_y, color=GREEN_STROKE, label="Hayır", lx=merge_cx+40, ly=(final_y+54+done_y)/2))
parts.append(box(merge_cx-170, done_y, 340, 58, ["SÜREÇ TAMAMLANDI"], GREEN_FILL, GREEN_STROKE, GREEN_TEXT, fs=16))

# ---- Side notes ----
note1_y = 232 - 54
parts.append(note(870, 170, 320, 108, "Tekrar kuralı (Md.56/5)",
    ["Aynı eğitim-öğretim yılı içinde davranış", "tekrarlanırsa bir üst yaptırım uygulanır:", "Uyarma → Kınama → Okul Değiştirme."]))

note2_y = done_y - 10
parts.append(note(150, done_y-14, 340, 92, "Düzelme hâlinde (Md.62/3)",
    ["Öğrenci davranışını tekrarlamaz ve olumlu", "davranış sergilerse, dönem sonu kurul", "toplantısında EK-12 ile yaptırım kaldırılabilir."]))

parts.append(note(merge_cx-150, by1+6, 300, 106, "Nakil gidilecek okul yoksa (Md.56/7)",
    ["Yerleşim biriminde nakledilebileceği", "başka ortaokul yoksa, yaptırım bir alt", "derece olan KINAMA olarak uygulanır."]))

# ---- Legend ----
leg_y = max(done_y + 58, itr_y + 62) + 70
parts.append(f'<line x1="60" y1="{leg_y-18}" x2="{W-60}" y2="{leg_y-18}" stroke="{LIGHT_GRAY}" stroke-width="1.5"/>')
legend_items = [
    (AMBER_FILL, AMBER_STROKE, "Uyarma süreci"),
    (CORAL_FILL, CORAL_STROKE, "Kınama"),
    (RED_FILL, RED_STROKE, "Okul değiştirme"),
    (BLUE_FILL, BLUE_STROKE, "Ortak kurul adımları"),
    (GREEN_FILL, GREEN_STROKE, "Süreç sonu"),
    (GRAY_FILL, GRAY_STROKE, "Nötr / itiraz"),
]
lx = 70
for fill, stroke, label in legend_items:
    parts.append(f'<rect x="{lx}" y="{leg_y}" width="22" height="16" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1.3"/>')
    parts.append(f'<text x="{lx+30}" y="{leg_y+13}" font-family="Calibri, Arial, sans-serif" font-size="13" fill="{GRAY}">{esc(label)}</text>')
    lx += 30 + 15*len(label) + 34

footer_y = leg_y + 40
parts.append(f'<text x="{W/2}" y="{footer_y}" text-anchor="middle" font-family="Calibri, Arial, sans-serif" font-size="11.5" fill="#9AA0A6">Millî Eğitim Bakanlığı Okul Öncesi Eğitim ve İlköğretim Kurumları Yönetmeliği Md.54-65 esas alınarak hazırlanmıştır — yalnızca ortaokul/imam-hatip ortaokulu kademesi içindir.</text>')

# compute actual content bottom to size viewbox precisely
content_bottom = footer_y + 30

bg_rect = f'<rect x="0" y="0" width="{W}" height="{content_bottom}" fill="{WHITE}"/>'
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{content_bottom}" viewBox="0 0 {W} {content_bottom}">\n' + bg_rect + "\n" + "\n".join(parts[1:]) + "\n</svg>"

with open("/home/claude/kumkale-site/assets/akis_semasi_interactive.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("content_bottom", content_bottom)
print("done")
