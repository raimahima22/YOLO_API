"use client";

import { useState } from "react";

export default function UploadBox({
  conf,
  iou,
  onResult,
}: any) {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState("");
  const [loading, setLoading] = useState(false);

  const upload = async () => {
    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/predict?conf=${conf}&iou=${iou}`,
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await res.json();

    onResult(data);

    setLoading(false);
  };

  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <h2 className="font-semibold text-lg mb-4">
        Upload Image
      </h2>

      <input
        type="file"
        accept="image/*"
        onChange={(e) => {
          const selected = e.target.files?.[0];

          if (!selected) return;

          setFile(selected);
          setPreview(URL.createObjectURL(selected));
        }}
      />

      {preview && (
        <img
          src={preview}
          alt="preview"
          className="mt-4 rounded-xl border max-h-96"
        />
      )}

      <button
        onClick={upload}
        disabled={!file || loading}
        className="mt-4 w-full bg-black text-white py-3 rounded-xl"
      >
        {loading ? "Running Detection..." : "Run Detection"}
      </button>
    </div>
  );
}