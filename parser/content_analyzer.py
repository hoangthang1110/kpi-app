from pyvi import ViTokenizer, ViPosTagger


def analyze_content(text):
    # Tách câu đơn giản bằng dấu chấm. Nếu muốn chính xác hơn có thể dùng regex.
    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if s.strip()]

    # POS tagging từng câu
    tokens = []
    for sentence in sentences:
        words, tags = ViPosTagger.postagging(sentence)
        tokens.extend(zip(words, tags))

    # Đếm tần suất loại từ (POS tag)
    pos_counts = {}
    for word, tag in tokens:
        pos_counts[tag] = pos_counts.get(tag, 0) + 1

    # Đánh giá độ phức tạp
    complexity = "high" if len(sentences) > 20 else "low" if len(sentences) < 5 else "medium"

    return {
        "sentence_count": len(sentences),
        "pos_counts": pos_counts,
        "complexity": complexity
    }


def check_5w1h(text):
    keys = ["Who", "What", "When", "Where", "Why", "How"]
    missing = [k for k in keys if k.lower() not in text.lower()]
    return {"missing": missing}


def calculate_kpi(structure_analysis, content_analysis):
    score = 100
    missing = structure_analysis["missing"]
    sentence_count = content_analysis["sentence_count"]
    complexity = content_analysis.get("complexity", "medium")

    if missing:
        score -= len(missing) * 10
    if sentence_count < 5:
        score -= 5

    # Giả định thời gian hoàn thành (có thể cập nhật sau)
    completed_in_minutes = 60

    return {
        "kpi_score": max(score, 0),
        "details": {
            "missing_5w1h": len(missing),
            "sentence_count": sentence_count,
            "pos_counts": content_analysis["pos_counts"],
            "complexity": complexity,
            "completed_in_minutes": completed_in_minutes
        }
    }
