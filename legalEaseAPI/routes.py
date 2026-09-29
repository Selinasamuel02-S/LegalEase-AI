from fastapi import APIRouter
from pydantic import BaseModel
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str

@router.post("/generate")
def generate_doc(req: DocumentRequest):
    gen = GeminiDocumentGenerator()
    result = gen.generate_document(req.document_type, req.parties, req.terms, req.dates)
    return {"document": result, "status": "success"}
