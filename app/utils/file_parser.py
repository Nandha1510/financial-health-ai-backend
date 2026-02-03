import pandas as pd
import PyPDF2

def parse_uploaded_file(file):
    filename = file.filename.lower()

    if filename.endswith(".csv"):
        return pd.read_csv(file.file)

    if filename.endswith(".xlsx"):
        return pd.read_excel(file.file)

    if filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file.file)
        text = " ".join(
            page.extract_text() or "" for page in reader.pages
        )
        return {"raw_text": text}

    raise ValueError("Unsupported file format")
