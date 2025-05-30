from docx import Document
import re

def check_docx_format(filepath):
    doc = Document(filepath)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip() != ""]

    result = {
        "quoc_hieu": False,
        "tieu_ngu": False,
        "so_hieu": False,
        "ngay_thang": False,
        "tieu_de": False,
        "nguoi_ky": False,
        "loi": []
    }

    for para in paragraphs:
        if "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" in para.upper():
            result["quoc_hieu"] = True
        if "Độc lập - Tự do - Hạnh phúc" in para:
            result["tieu_ngu"] = True
        if re.search(r"Số:\s*\d+/.+", para):
            result["so_hieu"] = True
        if re.search(r"ngày\s+\d+\s+tháng\s+\d+\s+năm\s+\d+", para.lower()):
            result["ngay_thang"] = True
        if para.isupper() and len(para.split()) >= 3:
            result["tieu_de"] = True
        if re.search(r"Ký tên|Trưởng phòng|Giám đốc|KT\. Giám đốc", para):
            result["nguoi_ky"] = True

    for key, value in result.items():
        if value is False:
            result["loi"].append(f"Thiếu hoặc sai mục: {key.replace('_', ' ').title()}")

    return result
