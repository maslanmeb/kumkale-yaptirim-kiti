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

/* ---------- Yazdır / PDF Al (baskı öncesi kutuları kesin olarak büyüt) ---------- */
function printForm() {
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
});
