// =======================================================
// Kumkale Ortaokulu — İlköğretim Kurumları ÖDDK Kiti — ortak davranışlar
// =======================================================

const SCHOOL_KEY = "yaptirimKiti_okulAdi";
const DEFAULT_SCHOOL = "KUMKALE ORTAOKULU MÜDÜRLÜĞÜ";

/* ---------- Okul adı: düzenlenebilir + hatırlanır ---------- */
function updateSchoolEchoes(text) {
  document.querySelectorAll(".okulAdi-echo").forEach((el) => (el.textContent = text));
}
function initSchoolName() {
  const el = document.getElementById("okulAdi");
  if (!el) return;
  const saved = localStorage.getItem(SCHOOL_KEY);
  el.textContent = saved || DEFAULT_SCHOOL;
  updateSchoolEchoes(el.textContent);
  el.addEventListener("input", () => {
    const val = el.textContent.trim() || DEFAULT_SCHOOL;
    localStorage.setItem(SCHOOL_KEY, val);
    updateSchoolEchoes(val);
  });
  el.addEventListener("blur", () => {
    if (!el.textContent.trim()) { el.textContent = DEFAULT_SCHOOL; updateSchoolEchoes(DEFAULT_SCHOOL); }
  });
  el.addEventListener("keydown", (e) => {
    if (e.key === "Enter") { e.preventDefault(); el.blur(); }
  });
}

/* ---------- Textarea'ları otomatik büyüt ---------- */
function autoGrow(el) {
  el.style.height = "auto";
  el.style.height = (el.scrollHeight + 2) + "px";
}
function initAutoGrow() {
  document.querySelectorAll("textarea").forEach((ta) => {
    autoGrow(ta);
    ta.addEventListener("input", () => autoGrow(ta));
    ta.addEventListener("paste", () => setTimeout(() => autoGrow(ta), 0));
  });
  window.addEventListener("beforeprint", () => {
    document.querySelectorAll("textarea").forEach(autoGrow);
  });
}

/* ---------- Alan biçimlendirme: Telefon (kullanıcı nasıl yazarsa yazsın) ---------- */
function onlyDigits(s, maxLen) {
  return s.replace(/\D/g, "").slice(0, maxLen);
}
function formatPhoneDisplay(raw) {
  let d = onlyDigits(raw, 11);
  if (d && d.charAt(0) !== "0") d = ("0" + d).slice(0, 11); // 0 ile başlamıyorsa otomatik eklenir
  let out = d.slice(0, 4);
  if (d.length > 4) out += " - " + d.slice(4, 7);
  if (d.length > 7) out += " " + d.slice(7, 9);
  if (d.length > 9) out += " " + d.slice(9, 11);
  return out;
}
function applyFieldFormatting() {
  document.querySelectorAll('input[type="tel"]').forEach((el) => { el.value = formatPhoneDisplay(el.value); });
}
function initFieldFormatting() {
  document.querySelectorAll('input[type="tel"]').forEach((el) => {
    el.addEventListener("input", () => {
      const capped = onlyDigits(el.value, 11);
      if (el.value !== capped) el.value = capped;
    });
    el.addEventListener("blur", () => { el.value = formatPhoneDisplay(el.value); });
  });
}

/* ---------- Yazdır / PDF Al (baskı öncesi kutuları kesin olarak büyüt) ---------- */
function printForm() {
  applyFieldFormatting();
  document.querySelectorAll("textarea").forEach(autoGrow);
  requestAnimationFrame(() => {
    document.querySelectorAll("textarea").forEach(autoGrow);
    requestAnimationFrame(() => {
      document.querySelectorAll("textarea").forEach(autoGrow);
      setTimeout(() => window.print(), 50);
    });
  });
}

/* ---------- Word'e Kopyala (panoya HTML + düz metin yazar) ----------
   Sayfanın doldurulmuş hâlini, form alanlarının GÜNCEL değerleriyle statik
   metne çevirip panoya kopyalar. Word'ün kendi "HTML'den yapıştır" motoru
   bunu gerçek Word tablosu/paragrafına dönüştürür. Ek kütüphane gerekmez,
   tarayıcının Clipboard API'si kullanılır; hiçbir veri sunucuya gitmez.

   Not: Site bir iframe içine gömülü açıldığında modern Clipboard API bazı
   tarayıcılarda izin vermeyebilir. Bu durumda eski/legacy execCommand("copy")
   yöntemine otomatik geçilir; o da başarısız olursa kullanıcıya siteyi tam
   sayfada açması önerilir.
*/
function formatFieldForCopy(el) {
  if (el.tagName === "SELECT") {
    return el.options[el.selectedIndex] ? el.options[el.selectedIndex].text : "";
  }
  if (el.type === "checkbox" || el.type === "radio") {
    return el.checked ? "☒" : "☐";
  }
  if (el.type === "date") {
    if (!el.value) return "";
    const [y, m, d] = el.value.split("-");
    return `${d}.${m}.${y}`;
  }
  return el.value || "";
}
function legacyCopyHTML(htmlString) {
  const container = document.createElement("div");
  container.style.position = "absolute";
  container.style.left = "0";
  container.style.top = "0";
  container.style.width = "900px";
  container.style.opacity = "0";
  container.style.pointerEvents = "none";
  container.style.zIndex = "-1";
  container.setAttribute("contenteditable", "true");
  container.innerHTML = htmlString;
  document.body.appendChild(container);
  void container.offsetHeight;

  const range = document.createRange();
  range.selectNodeContents(container);
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);

  let ok = false;
  try {
    ok = document.execCommand("copy");
  } catch (e) {
    ok = false;
  }
  selection.removeAllRanges();
  document.body.removeChild(container);
  return ok;
}
async function copyForWord() {
  const btn = document.getElementById("copyWordBtn");
  const pageEl = document.querySelector(".page");
  if (!pageEl) return;

  applyFieldFormatting();

  const originalText = btn.textContent;
  btn.disabled = true;
  btn.textContent = "Hazırlanıyor…";

  const clone = pageEl.cloneNode(true);

  clone.querySelectorAll([".dyn-remove", ".note-close", ".dizi-remove", ".dizi-add-row", ".school-hint"].join(",")).forEach((el) => el.remove());

  const liveFields = pageEl.querySelectorAll("input, textarea, select");
  const cloneFields = clone.querySelectorAll("input, textarea, select");
  liveFields.forEach((liveEl, i) => {
    const cloneEl = cloneFields[i];
    if (!cloneEl) return;
    const span = document.createElement("span");
    span.textContent = formatFieldForCopy(liveEl);
    cloneEl.replaceWith(span);
  });

  clone.querySelectorAll("[contenteditable]").forEach((el) => el.removeAttribute("contenteditable"));

  clone.querySelectorAll("table").forEach((t) => { t.style.borderCollapse = "collapse"; t.style.width = "100%"; });
  clone.querySelectorAll("td, th").forEach((c) => {
    c.style.border = "1px solid #999";
    c.style.padding = "4px 8px";
  });
  clone.querySelectorAll("td.label, th").forEach((c) => {
    c.style.fontWeight = "bold";
    c.style.background = "#f0f0f0";
  });

  const htmlString = `<div>${clone.innerHTML}</div>`;
  const plainString = clone.innerText || clone.textContent || "";
  let success = false;

  if (navigator.clipboard && typeof ClipboardItem !== "undefined") {
    try {
      await navigator.clipboard.write([
        new ClipboardItem({
          "text/html": new Blob([htmlString], { type: "text/html" }),
          "text/plain": new Blob([plainString], { type: "text/plain" }),
        }),
      ]);
      success = true;
    } catch (err) {
      console.warn("Clipboard API başarısız, eski yönteme geçiliyor:", err);
    }
  }

  if (!success) {
    success = legacyCopyHTML(htmlString);
  }

  if (success) {
    btn.textContent = "✅ Kopyalandı!";
    setTimeout(() => { btn.textContent = originalText; btn.disabled = false; }, 2200);
  } else {
    alert(
      "Kopyalama şu an çalışmadı. Bu sayfa bir web sitesine gömülü (iframe) açıldığında bazı tarayıcılar panoya erişimi kısıtlayabilir.\n\n" +
      "Öneri: Sayfayı 'Tam sayfada açmak için tıklayın' bağlantısından doğrudan açıp tekrar deneyin, ya da 'Yazdır / PDF Al' / 'PDF İndir' seçeneklerini kullanın."
    );
    btn.disabled = false;
    btn.textContent = originalText;
  }
}


/* ---------- Kapatılabilir bilgi kutuları ---------- */
function initNoteBoxes() {
  document.querySelectorAll(".note-box").forEach((box) => {
    if (box.querySelector(".note-close")) return;
    const btn = document.createElement("button");
    btn.className = "note-close";
    btn.type = "button";
    btn.innerHTML = "&times;";
    btn.setAttribute("aria-label", "Bu bilgi kutusunu kapat");
    btn.addEventListener("click", () => {
      box.style.maxHeight = box.scrollHeight + "px";
      requestAnimationFrame(() => {
        box.style.transition = "max-height .25s ease, opacity .25s ease, margin .25s ease, padding .25s ease";
        box.style.maxHeight = "0px";
        box.style.opacity = "0";
        box.style.marginTop = "0";
        box.style.marginBottom = "0";
        box.style.paddingTop = "0";
        box.style.paddingBottom = "0";
        box.style.overflow = "hidden";
      });
      setTimeout(() => box.remove(), 260);
    });
    box.appendChild(btn);
  });
}

/* ---------- Dinamik maddelenmiş liste ----------
   HTML iskeleti:
   <div class="dyn-list" data-placeholder="Metni yazınız...">
     <div class="dyn-row">
       <span class="dyn-num"></span>
       <textarea rows="1"></textarea>
       <button type="button" class="dyn-remove">&times;</button>
     </div>
   </div>
*/
function makeDynRow(placeholder) {
  const row = document.createElement("div");
  row.className = "dyn-row";
  row.innerHTML = `
    <span class="dyn-num"></span>
    <textarea rows="1" placeholder="${placeholder || ""}" autocomplete="off"></textarea>
    <button type="button" class="dyn-remove">&times;</button>`;
  return row;
}

function renumberDynList(list) {
  let n = 1;
  list.querySelectorAll(".dyn-row").forEach((row) => {
    const ta = row.querySelector("textarea");
    const num = row.querySelector(".dyn-num");
    const removeBtn = row.querySelector(".dyn-remove");
    const hasText = ta.value.trim().length > 0;
    if (hasText) {
      num.textContent = n + ".";
      num.classList.add("show");
      n++;
    } else {
      num.textContent = "";
      num.classList.remove("show");
    }
    const rowCount = list.querySelectorAll(".dyn-row").length;
    removeBtn.classList.toggle("show", rowCount > 1);
  });
}

function bindDynRow(list, row) {
  const ta = row.querySelector("textarea");
  const removeBtn = row.querySelector(".dyn-remove");

  ta.addEventListener("paste", () => setTimeout(() => autoGrow(ta), 0));
  ta.addEventListener("input", () => {
    autoGrow(ta);
    const rows = Array.from(list.querySelectorAll(".dyn-row"));
    const isLast = rows[rows.length - 1] === row;
    if (isLast && ta.value.trim().length > 0) {
      const placeholder = list.dataset.placeholder || "";
      const newRow = makeDynRow(placeholder);
      list.appendChild(newRow);
      bindDynRow(list, newRow);
    }
    renumberDynList(list);
  });

  removeBtn.addEventListener("click", () => {
    const rows = list.querySelectorAll(".dyn-row");
    if (rows.length <= 1) {
      ta.value = "";
      autoGrow(ta);
      renumberDynList(list);
      return;
    }
    row.remove();
    renumberDynList(list);
  });
}

function initDynLists() {
  document.querySelectorAll(".dyn-list").forEach((list) => {
    if (list.querySelector(".dyn-row")) {
      list.querySelectorAll(".dyn-row").forEach((row) => bindDynRow(list, row));
    } else {
      const row = makeDynRow(list.dataset.placeholder || "");
      list.appendChild(row);
      bindDynRow(list, row);
    }
    renumberDynList(list);
  });
}

/* ---------- Dizi pusulası tablosu (çok sütunlu, satır ekle/sil, toplam sayfa hesabı) ----------
   HTML iskeleti:
   <table class="dizi-table">
     <thead>...</thead>
     <tbody id="diziBody"></tbody>
   </table>
   <button type="button" class="dizi-add-row" data-target="diziBody">+ Satır Ekle</button>
*/
function makeDiziRow() {
  const row = document.createElement("tr");
  row.className = "dizi-row";
  row.innerHTML = `
    <td class="dizi-num"></td>
    <td><input type="date" autocomplete="off"></td>
    <td><input type="text" list="ekTurleri" placeholder="ör. EK-2 Sözlü Uyarma Notu" autocomplete="off"></td>
    <td><input type="number" min="0" class="dizi-sayfa" value="1" autocomplete="off"></td>
    <td><input type="text" placeholder="Açıklama" autocomplete="off"></td>
    <td><button type="button" class="dizi-remove">&times;</button></td>`;
  bindDiziRow(row);
  return row;
}
function updateDiziTotal(tbody) {
  let totalSayfa = 0;
  tbody.querySelectorAll(".dizi-sayfa").forEach((inp) => {
    const v = parseInt(inp.value, 10);
    if (!isNaN(v)) totalSayfa += v;
  });
  const table = tbody.closest("table");
  const sayfaCell = table.querySelector(".dizi-toplam-sayfa");
  const belgeCell = table.querySelector(".dizi-toplam-belge");
  if (sayfaCell) sayfaCell.textContent = totalSayfa;
  if (belgeCell) belgeCell.textContent = tbody.querySelectorAll(".dizi-row").length;
}
function renumberDiziTable(tbody) {
  let n = 1;
  tbody.querySelectorAll(".dizi-row").forEach((row) => {
    row.querySelector(".dizi-num").textContent = n++;
    row.querySelector(".dizi-remove").classList.toggle("show", tbody.querySelectorAll(".dizi-row").length > 1);
  });
  updateDiziTotal(tbody);
}
function bindDiziRow(row) {
  row.querySelector(".dizi-sayfa").addEventListener("input", () => updateDiziTotal(row.closest("tbody")));
  row.querySelector(".dizi-remove").addEventListener("click", () => {
    const tbody = row.closest("tbody");
    if (tbody.querySelectorAll(".dizi-row").length <= 1) {
      row.querySelectorAll("input").forEach((i) => (i.value = i.type === "number" ? "1" : ""));
      renumberDiziTable(tbody);
      return;
    }
    row.remove();
    renumberDiziTable(tbody);
  });
}
function initDiziTables() {
  document.querySelectorAll(".dizi-table tbody").forEach((tbody) => {
    tbody.querySelectorAll(".dizi-row").forEach(bindDiziRow);
    renumberDiziTable(tbody);
  });
  document.querySelectorAll(".dizi-add-row").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tbody = document.getElementById(btn.dataset.target);
      if (!tbody) return;
      const row = makeDiziRow();
      tbody.appendChild(row);
      renumberDiziTable(tbody);
      row.querySelector("input").focus();
    });
  });
}

/* ---------- Formu temizle ---------- */
function clearForm() {
  if (!confirm("Bu formdaki tüm bilgiler silinecek. Emin misiniz?")) return;
  document.querySelectorAll("input").forEach((el) => {
    if (el.type === "checkbox" || el.type === "radio") el.checked = false;
    else el.value = "";
  });
  document.querySelectorAll("select").forEach((el) => (el.selectedIndex = 0));
  document.querySelectorAll(".dyn-list").forEach((list) => {
    list.innerHTML = "";
    const row = makeDynRow(list.dataset.placeholder || "");
    list.appendChild(row);
    bindDynRow(list, row);
  });
  document.querySelectorAll(".dizi-table tbody").forEach((tbody) => {
    tbody.innerHTML = "";
    const row = makeDiziRow();
    tbody.appendChild(row);
    renumberDiziTable(tbody);
  });
  document.querySelectorAll("textarea:not(.dyn-list textarea)").forEach((el) => {
    el.value = "";
    autoGrow(el);
  });
}

/* ---------- Gizlilik: paylaşılan bilgisayarlarda tarayıcı otomatik-doldurma
   önerilerinin önceki kullanıcının verilerini göstermesini engelle ---------- */
function disableAutofill() {
  document.querySelectorAll("input, textarea, select").forEach((el) => {
    if (!el.hasAttribute("autocomplete")) el.setAttribute("autocomplete", "off");
  });
}

/* ---------- Başlat ---------- */
document.addEventListener("DOMContentLoaded", () => {
  disableAutofill();
  initSchoolName();
  initAutoGrow();
  initNoteBoxes();
  initDynLists();
  initFieldFormatting();
  initDiziTables();
});
