from underthesea import pos_tag, sent_tokenize
import re

def analyze_content(text: str):
    """
    Phân tích nội dung văn bản bằng underthesea:
    - Tách câu
    - Gán nhãn từ loại (POS)
    - Thống kê số loại từ
    """
    # 1. Tách câu
    sentences = sent_tokenize(text)

    # 2. POS tagging từng câu
    pos_results = [pos_tag(sentence) for sentence in sentences]

    # 3. Đếm số lượng từng loại từ (POS)
    pos_counts = {}
    for tagged in pos_results:
        for word, tag in tagged:
            pos_counts[tag] = pos_counts.get(tag, 0) + 1

    return {
        "sentence_count": len(sentences),
        "pos_counts": pos_counts,
        "example_tagged": pos_results[:3]  # ví dụ 3 câu đầu
    }


def check_5w1h(text: str):
    """
    Kiểm tra các yếu tố 5W1H trong nội dung:
    - Who: Ai
    - What: Làm gì
    - When: Khi nào
    - Where: Ở đâu
    - Why: Tại sao
    - How: Như thế nào
    """
    who = bool(re.search(r"Sở|Công ty|Ban|Phòng|UBND|ông|bà|đồng chí", text, re.IGNORECASE))
    what = bool(re.search(r"ban hành|thực hiện|xây dựng|báo cáo|phê duyệt|trình|gửi", text, re.IGNORECASE))
    when = bool(re.search(r"ngày\s+\d{1,2}\s+tháng\s+\d{1,2}", text))
    where = bool(re.search(r"Hà Nội|TP\.? HCM|Đà Nẵng|tại\s+\w+", text))
    why = bool(re.search(r"nhằm|để|vì|do|mục đích", text, re.IGNORECASE))
    how = bool(re.search(r"bằng cách|thông qua|qua việc", text, re.IGNORECASE))

    result = {
        "Who": who,
        "What": what,
        "When": when,
        "Where": where,
        "Why": why,
        "How": how,
    }

    missing = [k for k, v in result.items() if not v]

    return {
        "5W1H": result,
        "missing": missing
    }
