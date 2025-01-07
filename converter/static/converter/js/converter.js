const form = document.getElementById("upload-form");
const convertButton = document.getElementById("convert-button");
const downloadButton = document.getElementById("download-button");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    // Réinitialise le bouton "Télécharger" s'il est visible
    if (downloadButton.classList.contains("visible")) {
        downloadButton.classList.remove("increase");
        setTimeout(() => {
            downloadButton.classList.remove("visible");
            setTimeout(() => {
                convertButton.classList.remove("shrink"); 
            }, 10);
        }, 500);
    }

    // Agrandit le bouton "Convertir"
    convertButton.disabled = true;
    convertButton.textContent = "Conversion...";

    try {
        const response = await fetch(uploadUrl, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        });

        const data = await response.json();

        if (data.status === "success") {
            convertButton.classList.add("shrink");
            setTimeout(() => {
                downloadButton.dataset.downloadUrl = data.download_url; // Associe l'URL
                downloadButton.classList.add("visible"); // Affiche le bouton
                setTimeout(() => {
                    downloadButton.classList.add("increase"); // Déclenche l'animation d'agrandissement
                }, 10);
            }, 500);
            convertButton.textContent = "Convertir"; // Restaure le texte
        } else {
            alert(`Erreur : ${data.message}`);
            convertButton.textContent = "Convertir";
            convertButton.classList.remove("shrink");
        }
    } catch (error) {
        console.error("Erreur pendant la conversion :", error);
        convertButton.classList.remove("shrink");
    } finally {
        convertButton.disabled = false;
    }
});

// Gestion du clic sur le bouton de téléchargement
downloadButton.addEventListener("click", () => {
    const url = downloadButton.dataset.downloadUrl;

    if (url) {
        const anchor = document.createElement("a");
        anchor.href = url;
        anchor.download = ""; // Nom du fichier (optionnel)
        document.body.appendChild(anchor);
        anchor.click();
        document.body.removeChild(anchor);
    } else {
        alert("Aucune URL de téléchargement n'est disponible !");
    }
});
