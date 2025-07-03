import React, { useState } from "react";

function FileUpload({ onSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      onSuccess();
      alert("✅ Detection complete. Viewer updated.");
    } else {
      alert("❌ Upload failed.");
    }
    setLoading(false);
  };

  return (
    <div className="p-4 bg-gray-100 rounded-xl shadow-md">
      <h2 className="text-lg font-bold mb-2">Upload Floor Plan Image</h2>
      <input
        type="file"
        accept="image/png, image/jpeg"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button
        className="mt-2 px-4 py-1 bg-blue-600 text-white rounded"
        onClick={handleUpload}
        disabled={!file || loading}
      >
        {loading ? "Processing..." : "Upload & Detect"}
      </button>
    </div>
  );
}

export default FileUpload;