from docx import Document

def read_docx_text(filepath: str) -> str:
    """
    Đọc nội dung text từ file .docx
    """
    doc = Document(filepath)
    paragraphs = [para.text.strip() for para in doc.paragraphs if para.text.strip()]
    return "\n".join(paragraphs)
