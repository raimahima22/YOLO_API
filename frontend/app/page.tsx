"use client";

import { useState } from "react";
import Controls from "@/components/Controls";
import UploadBox from "@/components/UploadBox";
import ResultViewer from "@/components/ResultViewer";

export default function Home() {
  const [result, setResult] = useState(null);

  const [conf, setConf] = useState(0.25);
  const [iou, setIou] = useState(0.45);

  return (
    <main className="min-h-screen bg-slate-100">
      <div className="max-w-6xl mx-auto p-8">
        <div className="mb-10 text-center">
          <h1 className="text-5xl font-bold">
            YOLO Table Detector
          </h1>

          <p className="text-gray-600 mt-3">
            Detect tables, column headers and row headers
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <Controls
            conf={conf}
            setConf={setConf}
            iou={iou}
            setIou={setIou}
          />

          <div className="md:col-span-2">
            <UploadBox
              conf={conf}
              iou={iou}
              onResult={setResult}
            />
          </div>
        </div>

        <div className="mt-8">
          <ResultViewer data={result} />
        </div>
      </div>
    </main>
  );
}