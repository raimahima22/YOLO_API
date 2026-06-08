"use client";

type Props = {
  conf: number;
  setConf: (v: number) => void;
  iou: number;
  setIou: (v: number) => void;
};

export default function Controls({
  conf,
  setConf,
  iou,
  setIou,
}: Props) {
  return (
    <div className="bg-white rounded-2xl shadow p-5">
      <h2 className="font-semibold text-lg mb-5">
        Controls
      </h2>

      <div className="mb-6">
        <div className="flex justify-between mb-2">
          <span>Confidence</span>
          <span>{conf.toFixed(2)}</span>
        </div>

        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={conf}
          onChange={(e) => setConf(Number(e.target.value))}
          className="w-full"
        />
      </div>

      <div>
        <div className="flex justify-between mb-2">
          <span>IoU</span>
          <span>{iou.toFixed(2)}</span>
        </div>

        <input
          type="range"
          min="0"
          max="1"
          step="0.01"
          value={iou}
          onChange={(e) => setIou(Number(e.target.value))}
          className="w-full"
        />
      </div>
    </div>
  );
}