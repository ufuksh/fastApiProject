document.addEventListener("DOMContentLoaded", () => {
    const BASE_URL = "http://35.158.119.153:8000";

    // Form ve tablo elementlerini seçme
    const ogrenciForm = document.getElementById("ogrenci-form");
    const ogrenciTableBody = document.querySelector("#ogrenci-table tbody");
    const ogretmenForm = document.getElementById("ogretmen-form");
    const ogretmenTableBody = document.querySelector("#ogretmen-table tbody");
    const dersProgramiForm = document.getElementById("ders-programi-form");
    const dersProgramiTableBody = document.querySelector("#ders-programi-table tbody");
    const ogretmenSelect = document.getElementById("ogretmen-select");
    const feedbackMessage = document.getElementById("feedback-message"); // Geri bildirim mesajı için

    /**
     * API'den veri çekmek ve hataları yönetmek için yardımcı fonksiyon
     * @param {string} url - API endpoint'i
     * @param {object} options - Fetch seçenekleri
     * @returns {object|null} - API yanıtı veya null
     */
    async function fetchAndHandle(url, options = {}) {
        try {
            const res = await fetch(BASE_URL + url, options);
            if (!res.ok) {
                const error = await res.json();
                console.error(`Hata: ${error.detail || "Bilinmeyen bir hata oluştu."}`);
                showFeedback(error.detail || "Bir hata oluştu.", "error");
                return null;
            }
            return await res.json();
        } catch (err) {
            console.error("Sunucuya bağlanırken hata oluştu:", err);
            showFeedback("Sunucuya bağlanırken hata oluştu.", "error");
            return null;
        }
    }

    /**
     * Geri bildirim mesajını gösterir
     * @param {string} message - Mesaj içeriği
     * @param {string} type - Mesaj türü ('success' veya 'error')
     */
    function showFeedback(message, type) {
        if (feedbackMessage) {
            feedbackMessage.textContent = message;
            feedbackMessage.className = `feedback-message ${type}`;
            feedbackMessage.style.display = "block";
            setTimeout(() => {
                feedbackMessage.style.display = "none";
            }, 5000);
        }
    }

    /**
     * Öğretmen select alanını doldurur
     */
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

    /**
     * Tabloya satır ekler
     * @param {HTMLElement} tableBody - Tablo gövdesi
     * @param {object} data - Eklenecek veri
     * @param {string} type - Veri tipi ('ogrenci', 'ogretmen', 'ders-programi')
     */
    function addRow(tableBody, data, type) {
        const row = document.createElement("tr");
        let işlemButonu = "";

        switch(type) {
            case 'ogrenci':
                işlemButonu = `<button data-id="${data.id}" class="btn btn-delete delete-ogrenci"><i class="fas fa-trash-alt"></i> Sil</button>`;
                row.innerHTML = `
                    <td>${data.id}</td>
                    <td>${data.ad}</td>
                    <td>${data.soyad}</td>
                    <td>${data.ogrenci_numarasi}</td>
                    <td>${data.sinif}</td>
                    <td>${data.iletisim}</td>
                    <td>${işlemButonu}</td>
                `;
                break;
            case 'ogretmen':
                işlemButonu = `<button data-id="${data.id}" class="btn btn-delete delete-ogretmen"><i class="fas fa-trash-alt"></i> Sil</button>`;
                row.innerHTML = `
                    <td>${data.id}</td>
                    <td>${data.ad}</td>
                    <td>${data.soyad}</td>
                    <td>${data.brans}</td>
                    <td>${data.email}</td>
                    <td>${işlemButonu}</td>
                `;
                break;
            case 'ders-programi':
                işlemButonu = `<button data-id="${data.id}" class="btn btn-delete delete-ders-programi"><i class="fas fa-trash-alt"></i> Sil</button>`;
                row.innerHTML = `
                    <td>${data.id}</td>
                    <td>${data.sinif}</td>
                    <td>${data.ders}</td>
                    <td>${data.saat}</td>
                    <td>${data.ogretmen_id}</td>
                    <td>${işlemButonu}</td>
                `;
                break;
            default:
                break;
        }

        tableBody.appendChild(row);
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
            addRow(ogrenciTableBody, result, 'ogrenci');
            ogrenciForm.reset();
            showFeedback("Öğrenci başarıyla eklendi.", "success");
        }
    });

    // Öğrencileri Listele
    async function loadOgrenciler() {
        const ogrenciler = await fetchAndHandle("/ogrenciler/");
        if (ogrenciler) {
            ogrenciTableBody.innerHTML = "";
            ogrenciler.forEach(o => addRow(ogrenciTableBody, o, 'ogrenci'));
        }
    }

    // Öğrenci Sil
    ogrenciTableBody.addEventListener("click", async (e) => {
        if (e.target.closest(".delete-ogrenci")) {
            const id = e.target.closest("button").dataset.id;
            if (confirm("Bu öğrenciyi silmek istediğinizden emin misiniz?")) {
                const result = await fetchAndHandle(`/ogrenciler/${id}`, { method: "DELETE" });
                if (result) {
                    e.target.closest("tr").remove();
                    showFeedback("Öğrenci başarıyla silindi.", "success");
                }
            }
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
            addRow(ogretmenTableBody, result, 'ogretmen');
            await loadOgretmenSelect();
            ogretmenForm.reset();
            showFeedback("Öğretmen başarıyla eklendi.", "success");
        }
    });

    // Öğretmenleri Listele
    async function loadOgretmenler() {
        const ogretmenler = await fetchAndHandle("/ogretmenler/");
        if (ogretmenler) {
            ogretmenTableBody.innerHTML = "";
            ogretmenler.forEach(o => addRow(ogretmenTableBody, o, 'ogretmen'));
        }
    }

    // Öğretmen Sil
    ogretmenTableBody.addEventListener("click", async (e) => {
        if (e.target.closest(".delete-ogretmen")) {
            const id = e.target.closest("button").dataset.id;
            if (confirm("Bu öğretmeni silmek istediğinizden emin misiniz?")) {
                const result = await fetchAndHandle(`/ogretmenler/${id}`, { method: "DELETE" });
                if (result) {
                    e.target.closest("tr").remove();
                    await loadOgretmenSelect();
                    showFeedback("Öğretmen başarıyla silindi.", "success");
                }
            }
        }
    });

    // Ders Programı Ekle
    dersProgramiForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const data = Object.fromEntries(new FormData(dersProgramiForm).entries());
        const result = await fetchAndHandle("/dersprogrami/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (result) {
            addRow(dersProgramiTableBody, result, 'ders-programi');
            dersProgramiForm.reset();
            showFeedback("Ders programı başarıyla eklendi.", "success");
        }
    });

    // Ders Programını Listele
    async function loadDersProgrami() {
        const dersler = await fetchAndHandle("/dersprogrami/");
        if (dersler) {
            dersProgramiTableBody.innerHTML = "";
            dersler.forEach(d => addRow(dersProgramiTableBody, d, 'ders-programi'));
        }
    }

    // Ders Programı Sil
    dersProgramiTableBody.addEventListener("click", async (e) => {
        if (e.target.closest(".delete-ders-programi")) {
            const id = e.target.closest("button").dataset.id;
            if (confirm("Bu ders programını silmek istediğinizden emin misiniz?")) {
                const result = await fetchAndHandle(`/dersprogrami/${id}`, { method: "DELETE" });
                if (result) {
                    e.target.closest("tr").remove();
                    showFeedback("Ders programı başarıyla silindi.", "success");
                }
            }
        }
    });

    // Başlangıçta tüm verileri yükle
    (async function init() {
        await loadOgrenciler();
        await loadOgretmenler();
        await loadOgretmenSelect();
        await loadDersProgrami();
    })();
});
