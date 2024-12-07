document.addEventListener("DOMContentLoaded", () => {
    const ogrenciForm = document.getElementById("ogrenci-form");
    const ogrenciTableBody = document.querySelector("#ogrenci-table tbody");
    const ogretmenForm = document.getElementById("ogretmen-form");
    const ogretmenTableBody = document.querySelector("#ogretmen-table tbody");
    const dersProgramiForm = document.getElementById("ders-programi-form");
    const dersProgramiTableBody = document.querySelector("#ders-programi-table tbody");
    const ogretmenSelect = document.getElementById("ogretmen-select");

    async function loadOgretmenSelect() {
        const res = await fetch("/ogretmenler");
        if (res.ok) {
            const ogretmenler = await res.json();
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
        const formData = new FormData(ogrenciForm);
        const data = Object.fromEntries(formData.entries());
        const res = await fetch("/ogrenciler/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (res.ok) {
            await loadOgrenciler();
            ogrenciForm.reset();
        } else {
            const error = await res.json();
            console.error("Hata:", error);
            alert("Öğrenci eklenemedi!");
        }
    });

    // Öğrencileri Listele
    async function loadOgrenciler() {
        const res = await fetch("/ogrenciler/");
        if (res.ok) {
            const ogrenciler = await res.json();
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
            const res = await fetch(`/ogrenciler/${id}`, { method: "DELETE" });
            if (res.ok) {
                await loadOgrenciler();
            } else {
                alert("Öğrenci silinemedi!");
            }
        }
    });

    // Öğretmen Ekle
    ogretmenForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(ogretmenForm);
        const data = Object.fromEntries(formData.entries());
        const res = await fetch("/ogretmenler/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (res.ok) {
            await loadOgretmenler();
            await loadOgretmenSelect();
            ogretmenForm.reset();
        } else {
            alert("Öğretmen eklenemedi!");
        }
    });

    // Öğretmenleri Listele
    async function loadOgretmenler() {
        const res = await fetch("/ogretmenler/");
        if (res.ok) {
            const ogretmenler = await res.json();
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
        const formData = new FormData(dersProgramiForm);
        const data = Object.fromEntries(formData.entries());
        const res = await fetch("/dersprogrami/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (res.ok) {
            await loadDersProgrami();
            dersProgramiForm.reset();
        } else {
            alert("Ders programı eklenemedi!");
        }
    });

    async function loadDersProgrami() {
        const res = await fetch("/dersprogrami/");
        if (res.ok) {
            const dersler = await res.json();
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

    // Sayfa yüklendiğinde verileri getir
    (async function init() {
        await loadOgrenciler();
        await loadOgretmenler();
        await loadOgretmenSelect();
        await loadDersProgrami();
    })();
});
