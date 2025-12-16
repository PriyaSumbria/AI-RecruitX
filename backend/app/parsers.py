import pdfplumber
import io
from fastapi import UploadFile

async def pdf_to_text(file: UploadFile) -> str:
    """
    Read bytes from UploadFile and extract text using pdfplumber.
    Returns concatenated text of all pages (empty strings tolerated).
    """

    content = await file.read()
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        pages = [p.extract_text().strip() for p in pdf.pages if p.extract_text()]
    return "\n".join(pages)
