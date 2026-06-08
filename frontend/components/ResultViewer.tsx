export default function ResultViewer({ data }: any) {
  if (!data) {
    return (
      <div className="bg-white rounded-2xl shadow p-6">
        No detections yet.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow p-6">
      <h2 className="text-xl font-semibold mb-4">
        Detection Results
      </h2>

      <p className="mb-4">
        Total detections: {data.num_detections}
      </p>

      <div className="space-y-3">
        {data.detections.map((d: any, idx: number) => (
          <div
            key={idx}
            className="border rounded-xl p-4"
          >
            <p>
              <strong>Class:</strong> {d.class}
            </p>

            <p>
              <strong>Confidence:</strong>{" "}
              {d.confidence_percent}
            </p>

            <p>
              <strong>Bounding Box:</strong>{" "}
              {d.bbox.join(", ")}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}