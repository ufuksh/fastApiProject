// Sayfa yüklenince bir mesaj göster
document.addEventListener("DOMContentLoaded", function () {
    console.log("Sayfa başarıyla yüklendi!");
});

// Form gönderme işlemi
function submitForm(event) {
    event.preventDefault(); // Formun yenilenmesini engelle

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);

    console.log("Form verisi gönderiliyor:", data);

    // Formu API'ye gönder
    fetch(event.target.action, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error("Bir hata oluştu!");
        }
        return response.json();
    })
    .then((result) => {
        console.log("Başarılı:", result);
        alert("Form başarıyla gönderildi!");
    })
    .catch((error) => {
        console.error("Hata:", error);
        alert("Bir hata oluştu. Lütfen tekrar deneyin.");
    });
}

// Formlara submit işlemi ekle
document.querySelectorAll("form").forEach((form) => {
    form.addEventListener("submit", submitForm);
});
