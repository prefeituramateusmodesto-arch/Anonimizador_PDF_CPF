from fastapi import FastAPI, UploadFile, File
import re
import fitz  # PyMuPDF

app = FastAPI()

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

        if text != anonymized_text:
            page.insert_text((50, 50), anonymized_text)

    output_bytes = pdf_doc.tobytes()
    return {"message": "PDF processado com sucesso!"}
