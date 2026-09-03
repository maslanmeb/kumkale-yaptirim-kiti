import re

PAGE_TMPL = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag}</title>
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>

  <div class="toolbar">
    <a class="back" href="../index.html">&larr; Ana Sayfa</a>
    <span class="hint">Alanları doldurun, ardından bir indirme yöntemi seçin.</span>
    <div class="btns">
      <button class="secondary" type="button" onclick="clearForm()">Formu Temizle</button>
      <button class="secondary" type="button" onclick="printForm()">🖨️ Yazdır / PDF Al</button>
      <button type="button" id="pdfDownloadBtn" onclick="downloadPDF()">⬇️ PDF İndir</button>
    </div>
  </div>

  <div class="page">
    <div class="school-line" id="okulAdi" contenteditable="true" spellcheck="false"></div>
    <div class="school-sub">Öğrenci Davranışlarını Değerlendirme Süreci</div>

    <div class="ek-tag">EK-{no}</div>
    <h1>{title}</h1>
    <div class="dayanak">Dayanak: {dayanak}</div>

{body}

    <div class="foot">
      <span>Öğrenci Davranışları Yaptırım Süreci &ndash; Ek Belge</span>
      <span>EK-{no}</span>
    </div>
  </div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script src="../assets/app.js"></script>
</body>
</html>
"""

def page(no, title, dayanak, body):
    return PAGE_TMPL.format(
        title_tag=f"EK-{no} {title}",
        no=str(no).zfill(2) if False else no,
        title=title,
        dayanak=dayanak,
        body=body
    )

def meta_table(rows):
    """rows: list of (label, field_html)"""
    trs = "\n".join(
        f'      <tr><td class="label">{label}</td><td>{field}</td></tr>'
        for label, field in rows
    )
    return f'    <table class="meta">\n{trs}\n    </table>'

def text_field(id_, placeholder=""):
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    return f'<input type="text" id="{id_}"{ph}>'

def date_field(id_):
    return f'<input type="date" id="{id_}">'

def echo_field(suffix=" MÜDÜRLÜĞÜNE"):
    return f'<span class="okulAdi-echo"></span>{suffix}'

def section_title(text, sub=None):
    s = f'    <div class="section-title">{text}</div>\n'
    if sub:
        s += f'    <div class="section-sub">{sub}</div>\n'
    return s

def textarea(id_, placeholder="", rows=3):
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    return f'    <textarea id="{id_}" rows="{rows}"{ph}></textarea>\n'

def para(text, cls="para"):
    return f'    <div class="{cls}">{text}</div>\n'

def note_box(title, text):
    return f'''    <div class="note-box">
      <div class="note-title">{title}</div>
      <div class="note-text">{text}</div>
    </div>
'''

def dyn_list(placeholder="Metni yazınız..."):
    return f'    <div class="dyn-list" data-placeholder="{placeholder}"></div>\n'

def radio_group(name, options, id_prefix, layout="block"):
    """options: list of (value, label)"""
    rows = []
    for i, (val, label) in enumerate(options):
        rid = f"{id_prefix}_{i}"
        rows.append(f'      <div class="radio-row"><input type="radio" name="{name}" id="{rid}" value="{val}"><label for="{rid}">{label}</label></div>')
    return f'    <div class="check-group">\n' + "\n".join(rows) + "\n    </div>\n"

def checkbox_group(items, id_prefix):
    """items: list of (id_suffix, label) or (id_suffix, label, extra_text_input_id)"""
    rows = []
    for i, item in enumerate(items):
        if len(item) == 2:
            suf, label = item
            cid = f"{id_prefix}_{suf}"
            rows.append(f'      <div class="check-row"><input type="checkbox" id="{cid}"><label for="{cid}">{label}</label></div>')
        else:
            suf, label, extra_id = item
            cid = f"{id_prefix}_{suf}"
            rows.append(f'      <div class="check-row inline-extra"><input type="checkbox" id="{cid}"><label for="{cid}">{label}</label><input type="text" id="{extra_id}" placeholder="belirtiniz"></div>')
    return f'    <div class="check-group">\n' + "\n".join(rows) + "\n    </div>\n"

def signature_block(labels):
    tds = "\n".join(
        f'''        <td>
          <div class="imza-box"></div>
          <input class="imza-name" type="text" placeholder="Ad Soyad">
          <div class="imza-label">{lbl}</div>
        </td>'''
        for lbl in labels
    )
    return f'''    <table class="imza">
      <tr>
{tds}
      </tr>
    </table>
'''

def member_table(rows, extra_col=None):
    """rows: list of role labels; produces Üye | Adı Soyadı | (extra) table"""
    header_extra = f'<td class="label" style="width:20%">{extra_col}</td>' if extra_col else ""
    trs = []
    for i, role in enumerate(rows):
        extra_td = f'<td>{date_field(f"uye{i}_extra")}</td>' if extra_col else ""
        trs.append(f'      <tr><td class="label" style="width:34%">{role}</td><td>{text_field(f"uye{i}_ad")}</td>{extra_td}</tr>')
    header = f'      <tr><td class="label" style="width:34%">Üye</td><td class="label">Adı Soyadı</td>{header_extra}</tr>\n' if False else ""
    return '    <table class="meta">\n' + "\n".join(trs) + '\n    </table>\n'
