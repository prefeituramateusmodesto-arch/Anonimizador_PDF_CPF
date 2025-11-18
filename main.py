from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import fitz
import re
import os
import uuid
import shutil

app = FastAPI()

# CORS Liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Regex para CPF
cpf_pattern = re.compile(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b')

def anonimizar_pdf(input_path, output_path):
    doc = fitz.open(input_path)

    for page in doc:
        text_instances = page.search_for(cpf_pattern)
        for inst in text_instances:
            page.add_redact_annot(inst, fill=(0, 0, 0))
        page.apply_redactions()

    doc.save(output_path)
    doc.close()


@app.get("/")
def home():
    return HTMLResponse("<h1>API Rodando ✔</h1><p>Use o frontend para enviar PDFs.</p>")


@app.post("/upload")
async def upload(files: list[UploadFile] = File(...)):
    output_files = []

    for file in files:
        file_id = str(uuid.uuid4())
        input_path = f"/tmp/{file_id}_{file.filename}"
        output_path = f"/tmp/ANON_{file.filename}"

        with open(input_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        anonimizar_pdf(input_path, output_path)
        output_files.append(output_path)

    return JSONResponse({"files": output_files})
