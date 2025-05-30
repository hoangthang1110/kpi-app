import React, { useState } from "react";
import axios from "axios";

function UploadForm() {
  const [file, setFile] = useState(null);
  const [report, setReport] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://localhost:8000/upload/", formData);
    setReport(res.data.analysis);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold">Tải lên văn bản hành chính</h2>
      <input type="file" accept=".docx" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} className="bg-blue-500 text-white px-4 py-2 rounded mt-2">Phân tích</button>

      {report && (
        <div className="mt-4 bg-gray-100 p-4 rounded">
          <h3 className="text-lg font-semibold">Kết quả phân tích:</h3>
          <ul className="list-disc ml-5">
            {report.loi.length === 0 ? (
              <li className="text-green-600">Văn bản đúng thể thức!</li>
            ) : (
              report.loi.map((item, idx) => <li key={idx}>{item}</li>)
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

export default UploadForm;
