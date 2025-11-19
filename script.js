document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const files = document.getElementById("fileInput").files;
    if (files.length === 0) {
        alert("Selecione ao menos 1 PDF!");
        return;
    }

    const formData = new FormData();
    for (let f of files) {
        formData.append("files", f);
    }

    document.getElementById("status").innerHTML = "Processando... Aguarde.";

    const response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    if (!response.ok) {
        document.getElementById("status").innerHTML = "Erro ao processar!";
        return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "resultado.zip"; 
    a.click();

    document.getElementById("status").innerHTML = "Arquivo(s) prontos para download!";
});
