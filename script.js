const API_URL = "https://anonimizador-pdf-cpf.onrender.com/anonymize_pdf/";

async function sendPDF() {
    const fileInput = document.getElementById('pdfFile');
    const status = document.getElementById('status');

    if (!fileInput.files.length) {
        status.textContent = "Por favor, selecione um PDF.";
        status.style.color = "red";
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    status.textContent = "Processando... aguarde.";
    status.style.color = "black";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Erro ao processar o PDF.");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "PDF_Anonimizado.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();

        status.textContent = "PDF anonimizado com sucesso!";
        status.style.color = "green";

    } catch (error) {
        status.textContent = "Erro no servidor. Tente novamente.";
        status.style.color = "red";
    }
}
