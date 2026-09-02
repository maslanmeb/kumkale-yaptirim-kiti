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
    setTimeout(() => window.print(), 30);
  });
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
    <textarea rows="1" placeholder="${placeholder || ""}"></textarea>
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
    <td><input type="date"></td>
    <td><input type="text" list="ekTurleri" placeholder="ör. EK-2 Sözlü Uyarma Notu"></td>
    <td><input type="number" min="0" class="dizi-sayfa" value="1"></td>
    <td><input type="text" placeholder="Açıklama"></td>
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

/* ---------- Başlat ---------- */
document.addEventListener("DOMContentLoaded", () => {
  initSchoolName();
  initAutoGrow();
  initNoteBoxes();
  initDynLists();
  initFieldFormatting();
  initDiziTables();
});
