"""File parsing service for PDF, DOCX, and text files."""
import io
import re
from typing import Optional
from fastapi import UploadFile, HTTPException

import PyPDF2
import docx


def clean_text(text: str) -> str:
    """Clean and normalize text by removing extra whitespace."""
    return re.sub(r"\s+", " ", text).strip()


def extract_text_from_file(file: UploadFile) -> str:
    """
    Extract text from uploaded file (PDF, DOCX, or TXT).
    
    Args:
        file: FastAPI UploadFile object
        
    Returns:
        Extracted text content
        
    Raises:
        HTTPException: If file type is unsupported or parsing fails
    """
    filename = file.filename or ""
    file_ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""
    
    # Read file content
    try:
        content = file.file.read()
        file.file.seek(0)  # Reset for potential re-read
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    
    # Validate file size (16MB max)
    max_size = 16 * 1024 * 1024  # 16MB
    if len(content) > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds 16MB limit")
    
    # Parse based on file type
    try:
        if file_ext == "pdf":
            return extract_text_from_pdf(io.BytesIO(content))
        elif file_ext == "docx":
            return extract_text_from_docx(io.BytesIO(content))
        elif file_ext == "txt":
            return extract_text_from_txt(content)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}. Supported: pdf, docx, txt"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")


def extract_text_from_pdf(file_obj: io.BytesIO) -> str:
    """Extract text from PDF file."""
    try:
        reader = PyPDF2.PdfReader(file_obj)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return " ".join(text_parts)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF parsing error: {str(e)}")


def extract_text_from_docx(file_obj: io.BytesIO) -> str:
    """Extract text from DOCX file."""
    try:
        doc = docx.Document(file_obj)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DOCX parsing error: {str(e)}")


def extract_text_from_txt(content: bytes) -> str:
    """Extract text from TXT file."""
    try:
        # Try UTF-8 first, fallback to latin-1
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("latin-1")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Text file parsing error: {str(e)}")

