from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import re
import fitz  # PyMuPDF
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

# Liberar CORS para seu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CPF_REGEX = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'


def anonymize_cpf(text: str) -> str:
    return re.sub(CPF_REGEX, "***.***.***-**", text)


@app.post("/anonymize_pdf/")
async def anonymize_pdf(file: UploadFile = File(...)):
    pdf_bytes = await file.read()
    pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page in pdf_doc:
        text = page.get_text()
        anonymized_text = anonymize_cpf(text)

        # Se houve CPF substituído, insere o texto modificado por cima
        if text != anonymized_text:
            page.insert_text((50, 50), anonymized_text)

    output_bytes = pdf_doc.tobytes()
    pdf_doc.close()

    # retorna PDF para download
    return StreamingResponse(
        BytesIO(output_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=anonimizado.pdf"}
    )
