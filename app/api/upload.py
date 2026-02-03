from fastapi import APIRouter, UploadFile, HTTPException
from app.utils.file_parser import parse_uploaded_file

router = APIRouter()

@router.post("/")
def upload_financial_file(file: UploadFile):
    try:
        data = parse_uploaded_file(file)
        return {
            "message": "File uploaded successfully",
            "preview": str(data)[:500]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
