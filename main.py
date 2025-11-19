from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF
import io
import re
import os

app = Flask(__name__)

CPF_REGEX = r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"

def anonymize_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page in doc:
        text_instances = page.search_for(re.compile(CPF_REGEX))
        for inst in text_instances:
            page.add_redact_annot(inst, fill=(0, 0, 0))
        page.apply_redactions()

    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return output


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "files" not in request.files:
        return {"error": "Nenhum arquivo enviado"}, 400

    files = request.files.getlist("files")
    processed_files = []

    for file in files:
        pdf_content = file.read()
        anonymized = anonymize_pdf(pdf_content)

        processed_files.append(
            (file.filename.replace(".pdf", "_anon.pdf"), anonymized)
        )

    if len(processed_files) == 1:
        # Se for só 1 arquivo, retornar o PDF direto
        filename, pdf_data = processed_files[0]
        return send_file(pdf_data, download_name=filename, as_attachment=True)

    # Se vários → gerar ZIP
    import zipfile
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as z:
        for filename, pdf_data in processed_files:
            z.writestr(filename, pdf_data.getvalue())

    zip_buffer.seek(0)
    return send_file(zip_buffer, download_name="arquivos_anonimizados.zip", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
