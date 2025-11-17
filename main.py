# Projeto: Anonimizador de CPF em PDF (FastAPI + Frontend Render)

Abaixo estão **todos os arquivos necessários** para subir o projeto no **GitHub** e fazer deploy no **Render**.

---

## 📌 1. main.py (Backend FastAPI)

```python
import re
import io
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from PyPDF2 import PdfReader, PdfWriter

app = FastAPI()

# Regex de CPF
CPF_REGEX = r"\b(\d{3}\.\d{3}\.\d{3}-\d{2})\b"

def anonymize_text(text: str) -> str:
    return re.sub(CPF_REGEX, "***.***.***-**", text)

@app.post("/anonimizar")
async def anonimizar_pdf(file: UploadFile):
    reader = PdfReader(file.file)
    writer = PdfWriter()

    for page in reader.pages:
        text = page.extract_text()

        if text:
            new_text = anonymize_text(text)
            page_data = writer.add_blank_page(
                width=page.mediabox.width,
                height=page.mediabox.height
            )
            page_data.insert_text(
                new_text,
                20,
                page.mediabox.height - 40,
                font_size=12,
            )
        else:
            writer.add_page(page)

    output_pdf = io.BytesIO()
    writer.write(output_pdf)
    output_pdf.seek(0)

    return StreamingResponse(
        output_pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=anonimizado.pdf"},
    )
```

---

## 📌 2. requirements.txt

```txt
fastapi
uvicorn[standard]
PyPDF2
python-multipart
```

---

## 📌 3. render.yaml (para deploy automático no Render)

```yaml
services:
  - type: web
    name: anonimizar-cpf
    env: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    autoDeploy: true
```

---

## 📌 4. index.html (Frontend para enviar PDF ao backend)

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Anonymizador de CPF em PDF</title>
</head>
<body>
    <h2>Anonymizar CPF em PDF</h2>

    <input type="file" id="pdfFile" accept="application/pdf">
    <button onclick="uploadPDF()">Enviar</button>

    <p id="status"></p>

    <script>
        async function uploadPDF() {
            const fileInput = document.getElementById("pdfFile");
            if (!fileInput.files.length) {
                alert("Selecione um arquivo PDF!");
                return;
            }

            const formData = new FormData();
            formData.append("file", fileInput.files[0]);

            document.getElementById("status").innerText = "Processando...";

            try {
                const response = await fetch("https://SEU_BACKEND.onrender.com/anonimizar", {
                    method: "POST",
                    body: formData
                });

                if (!response.ok) {
                    document.getElementById("status").innerText = "Erro no processamento.";
                    return;
                }

                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);

                const a = document.createElement("a");
                a.href = url;
                a.download = "pdf_anonimizado.pdf";
                document.body.appendChild(a);
                a.click();

                document.getElementById("status").innerText = "Download pronto!";
            } catch (error) {
                document.getElementById("status").innerText = "Erro ao enviar.";
            }
        }
    </script>
</body>
</html>
```

---

## 📌 5. Estrutura recomendada para o repositório

```
anonimizador-cpf/
│
├── main.py
├── requirements.txt
├── render.yaml
└── frontend/
      └── index.html
```

---

Se quiser, posso gerar também:

* **README.md completo para o GitHub**
* **Versão do backend com OCR (tesseract)**
* **Versão com anonimização visual (riscando o CPF)**
* **Dockerfile** para rodar localmente

Basta pedir! 🙌
