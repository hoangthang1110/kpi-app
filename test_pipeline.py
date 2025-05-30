from utils.docx_reader import read_docx_content
from parser.content_analyzer import analyze_content, check_5w1h, calculate_kpi
import os

def test_kpi_pipeline(file_path):
    print(f"🔍 Đang kiểm tra file: {file_path}")

    # Đọc nội dung văn bản
    text = read_docx_content(file_path)
    print("\n📄 Trích xuất nội dung thành công:")
    print(text[:500] + "\n...")  # In 500 ký tự đầu tiên

    # Phân tích nội dung
    content_analysis = analyze_content(text)
    print("\n📊 Phân tích nội dung:")
    print(content_analysis)

    # Kiểm tra 5W1H
    structure_analysis = check_5w1h(text)
    print("\n🧩 Kiểm tra thể thức (5W1H):")
    print(structure_analysis)

    # Tính KPI
    kpi = calculate_kpi(structure_analysis, content_analysis)
    print("\n✅ Kết quả KPI:")
    print(kpi)

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    # Đường dẫn đến các file DOCX mẫu
    test_files = [
        "uploads/01_To trinh So trinh UBND_ok.docx",
        "uploads/03_Xin y kien cac co quan don vi_v01_ok.docx"
        # File thứ 3 là .doc, bạn cần chuyển sang .docx hoặc xử lý riêng
    ]

    for file_path in test_files:
        if os.path.exists(file_path):
            test_kpi_pipeline(file_path)
        else:
            print(f"⚠️ File không tồn tại: {file_path}")
