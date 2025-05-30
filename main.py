from fastapi import FastAPI, File, UploadFile, HTTPException
from utils.docx_reader import read_docx_content
from parser.content_analyzer import analyze_content, check_5w1h, calculate_kpi
from db.database import SessionLocal, Document
import os
import shutil
from routers import kpi
from fastapi import FastAPI

app = FastAPI()
app.include_router(kpi.router)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.get("/")
def read_root():
    return {"message": "Hello KPI App"}
@app.post("/analyze-docx/")
async def analyze_docx(file: UploadFile = File(...)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file .docx")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        text = read_docx_content(file_path)
        content_analysis = analyze_content(text)
        structure_analysis = check_5w1h(text)
        kpi_result = calculate_kpi(structure_analysis, content_analysis)

        db = SessionLocal()
        doc = Document(
            filename=file.filename,
            uploader="Tên cán bộ",  # TODO: Thay bằng user thực sau
            word_count=len(text.split()),
            kpi_score=kpi_result["kpi_score"],
            missing_5w1h=kpi_result["details"]["missing_5w1h"],
            sentence_count=kpi_result["details"]["sentence_count"],
            pos_counts_json=kpi_result["details"]["pos_counts"],
            complexity=kpi_result["details"].get("complexity", "medium"),
            completed_in_minutes=kpi_result["details"].get("completed_in_minutes", 0)
        )
        db.add(doc)
        db.commit()
        db.close()

        return {
            "filename": file.filename,
            "word_count": len(text.split()),
            "structure_analysis": structure_analysis,
            "content_analysis": content_analysis,
            "kpi": kpi_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
