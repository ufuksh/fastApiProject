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
        const res = await fetch("/ogrenciler", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (res.ok) {
            await loadOgrenciler();
            ogrenciForm.reset();
        }
    });

    // Öğrencileri Listele
    async function loadOgrenciler() {
        const res = await fetch("/ogrenciler");
        if (res.ok) {
            const ogrenciler = await res.json();
            ogrenciTableBody.innerHTML = "";
            ogrenciler.forEach(o => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${o.id}</td>
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
        if(e.target.classList.contains("delete-ogrenci")){
            const id = e.target.dataset.id;
            const res = await fetch(`/ogrenciler/${id}`, { method: "DELETE" });
            if(res.ok){
                await loadOgrenciler();
            }
        }
    });

    // Öğretmen Ekle
    ogretmenForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(ogretmenForm);
        const data = Object.fromEntries(formData.entries());
        const res = await fetch("/ogretmenler", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (res.ok) {
            await loadOgretmenler();
            await loadOgretmenSelect();
            ogretmenForm.reset();
        }
    });

    // Öğretmenleri Listele
    async function loadOgretmenler() {
        const res = await fetch("/ogretmenler");
        if (res.ok) {
            const ogretmenler = await res.json();
            ogretmenTableBody.innerHTML = "";
            ogretmenler.forEach(o => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${o.id}</td>
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

    // Öğretmen Sil
    ogretmenTableBody.addEventListener("click", async (e) => {
        if(e.target.classList.contains("delete-ogretmen")){
            const id = e.target.dataset.id;
            const res = await fetch(`/ogretmenler/${id}`, { method: "DELETE" });
            if(res.ok){
                await loadOgretmenler();
                await loadOgretmenSelect();
            }
        }
    });

    // Ders Programı Ekle
    dersProgramiForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(dersProgramiForm);
        const data = Object.fromEntries(formData.entries());
        const res = await fetch("/dersprogrami", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if(res.ok){
            await loadDersProgrami();
            dersProgramiForm.reset();
        }
    });

    // Ders Programı Listele
    async function loadDersProgrami() {
        const res = await fetch("/dersprogrami");
        if (res.ok) {
            const dersler = await res.json();
            dersProgramiTableBody.innerHTML = "";
            dersler.forEach(d => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${d.id}</td>
                    <td>${d.sinif}</td>
                    <td>${d.ders}</td>
                    <td>${d.saat}</td>
                    <td>${d.ogretmen_id}</td>
                    <td><button data-id="${d.id}" class="delete-ders-programi">Sil</button></td>
                `;
                dersProgramiTableBody.appendChild(row);
            });
        }
    }

    // Ders Programı Sil
    dersProgramiTableBody.addEventListener("click", async (e) => {
        if(e.target.classList.contains("delete-ders-programi")){
            const id = e.target.dataset.id;
            const res = await fetch(`/dersprogrami/${id}`, { method: "DELETE" });
            if(res.ok){
                await loadDersProgrami();
            }
        }
    });

    // Sayfa yüklendiğinde verileri getir
    (async function init(){
        await loadOgrenciler();
        await loadOgretmenler();
        await loadOgretmenSelect();
        await loadDersProgrami();
    })();
});
