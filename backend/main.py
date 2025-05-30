@app.post("/analyze-docx/")
async def analyze_docx(file: UploadFile = File(...)):
    filepath = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = read_docx_text(filepath)
    
    # 🔍 Phân tích nội dung & thể thức
    content_analysis = analyze_content(text)
    structure_analysis = check_5w1h(text)

    # ✅ Tính KPI
    kpi_result = calculate_kpi(structure_analysis, content_analysis)

    # 💾 Lưu vào PostgreSQL
    db = SessionLocal()
    doc = Document(
        filename=file.filename,
        uploader="Tên cán bộ",  # TODO: thay bằng thông tin từ đăng nhập khi làm auth
        word_count=len(text.split()),
        kpi_score=kpi_result["kpi_score"],
        missing_5w1h=kpi_result["details"]["missing_5w1h"],
        sentence_count=kpi_result["details"]["sentence_count"],
        pos_counts_json=kpi_result["details"]["pos_counts"]
    )
    db.add(doc)
    db.commit()
    db.close()

    # 📦 Trả kết quả cho frontend
    return {
        "filename": file.filename,
        "word_count": len(text.split()),
        "structure_analysis": structure_analysis,
        "content_analysis": content_analysis,
        "kpi": kpi_result
    }
