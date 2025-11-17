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
