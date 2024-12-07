document.addEventListener("DOMContentLoaded", () => {
    const ogrenciForm = document.getElementById("ogrenci-form");
    const ogrenciTableBody = document.querySelector("#ogrenci-table tbody");
    const ogretmenForm = document.getElementById("ogretmen-form");
    const ogretmenTableBody = document.querySelector("#ogretmen-table tbody");
    const dersProgramiForm = document.getElementById("ders-programi-form");
    const dersProgramiTableBody = document.querySelector("#ders-programi-table tbody");
    const ogretmenSelect = document.getElementById("ogretmen-select");

    async function fetchAndHandle(url, options = {}) {
        try {
            const res = await fetch(url, options);
            if (!res.ok) {
                const error = await res.json();
                console.error(`Hata: ${error.detail || "Bilinmeyen bir hata oluştu."}`);
                alert(error.detail || "Bir hata oluştu.");
            }
            return res.ok ? res.json() : null;
        } catch (err) {
            console.error("Sunucuya bağlanırken hata oluştu:", err);
            alert("Sunucuya bağlanırken hata oluştu.");
            return null;
        }
    }

    async function loadOgretmenSelect() {
        const ogretmenler = await fetchAndHandle("/ogretmenler/");
        if (ogretmenler) {
            ogretmenSelect.innerHTML = `<option value="">Öğretmen Seçin</option>`;
            ogretmenler.forEach(o => {
                const option = document.createElement("option");
                option.value = o.id;
                option.textContent = `${o.ad} ${o.soyad}`;
                ogretmenSelect.appendChild(option);
            });
        }
    }

    // Öğrenci Ekle
    ogrenciForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(ogrenciForm).entries());
        const result = await fetchAndHandle("/ogrenciler/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (result) {
            await loadOgrenciler();
            ogrenciForm.reset();
        }
    });

    // Öğrencileri Listele
    async function loadOgrenciler() {
        const ogrenciler = await fetchAndHandle("/ogrenciler/");
        if (ogrenciler) {
            ogrenciTableBody.innerHTML = "";
            ogrenciler.forEach(o => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${o.id.slice(0, 8)}</td>
                    <td>${o.ad}</td>
                    <td>${o.soyad}</td>
                    <td>${o.ogrenci_numarasi}</td>
                    <td>${o.sinif}</td>
                    <td>${o.iletisim}</td>
                    <td><button data-id="${o.id}" class="delete-ogrenci">Sil</button></td>
                `;
                ogrenciTableBody.appendChild(row);
            });
        }
    }

    // Öğrenci Sil
    ogrenciTableBody.addEventListener("click", async (e) => {
        if (e.target.classList.contains("delete-ogrenci")) {
            const id = e.target.dataset.id;
            const result = await fetchAndHandle(`/ogrenciler/${id}`, { method: "DELETE" });
            if (result) await loadOgrenciler();
        }
    });

    // Öğretmen Ekle
    ogretmenForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(ogretmenForm).entries());
        const result = await fetchAndHandle("/ogretmenler/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (result) {
            await loadOgretmenler();
            await loadOgretmenSelect();
            ogretmenForm.reset();
        }
    });

    // Öğretmenleri Listele
    async function loadOgretmenler() {
        const ogretmenler = await fetchAndHandle("/ogretmenler/");
        if (ogretmenler) {
            ogretmenTableBody.innerHTML = "";
            ogretmenler.forEach(o => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${o.id.slice(0, 8)}</td>
                    <td>${o.ad}</td>
                    <td>${o.soyad}</td>
                    <td>${o.brans}</td>
                    <td>${o.iletisim}</td>
                    <td><button data-id="${o.id}" class="delete-ogretmen">Sil</button></td>
                `;
                ogretmenTableBody.appendChild(row);
            });
        }
    }

    // Ders Programı İşlemleri
    dersProgramiForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(dersProgramiForm).entries());
        const result = await fetchAndHandle("/dersprogrami/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (result) {
            await loadDersProgrami();
            dersProgramiForm.reset();
        }
    });

    async function loadDersProgrami() {
        const dersler = await fetchAndHandle("/dersprogrami/");
        if (dersler) {
            dersProgramiTableBody.innerHTML = "";
            dersler.forEach(d => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${d.id.slice(0, 8)}</td>
                    <td>${d.sinif}</td>
                    <td>${d.ders}</td>
                    <td>${d.saat}</td>
                    <td>${d.ogretmen_id.slice(0, 8)}</td>
                    <td><button data-id="${d.id}" class="delete-ders-programi">Sil</button></td>
                `;
                dersProgramiTableBody.appendChild(row);
            });
        }
    }

    // Ders Programı Sil
    dersProgramiTableBody.addEventListener("click", async (e) => {
        if (e.target.classList.contains("delete-ders-programi")) {
            const id = e.target.dataset.id;
            const result = await fetchAndHandle(`/dersprogrami/${id}`, { method: "DELETE" });
            if (result) await loadDersProgrami();
        }
    });

    // Sayfa yüklendiğinde verileri getir
    (async function init() {
        await loadOgrenciler();
        await loadOgretmenler();
        await loadOgretmenSelect();
        await loadDersProgrami();
    })();
});
