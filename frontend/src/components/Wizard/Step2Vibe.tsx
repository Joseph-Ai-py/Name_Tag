import React from "react";
import { useWizard } from "../../hooks/useWizard";

const VIBES = [
  "따뜻한",
  "차가운",
  "모던한",
  "클래식한",
  "자연친화적",
  "럭셔리한",
  "미니멀한",
  "활기찬",
  "유머러스한",
  "진지한",
  "감성적인",
  "신뢰감있는",
  "트렌디한",
  "레트로한",
];

export function Step2Vibe() {
  const {
    selectedVibes,
    toggleVibe,
    setStep,
    canProceedStep2,
  } = useWizard();

  const handleBack = () => setStep(1);
  const handleNext = () => {
    if (canProceedStep2) {
      setStep(3);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          브랜드 감성을 선택해주세요
        </h2>
        <p className="text-gray-600">최대 4개까지 선택 가능합니다</p>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
        {VIBES.map((vibe) => (
          <button
            key={vibe}
            onClick={() => toggleVibe(vibe)}
            className={`px-4 py-3 rounded-lg font-medium transition ${
              selectedVibes.includes(vibe)
                ? "bg-blue-600 text-white ring-2 ring-blue-400"
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            {vibe}
          </button>
        ))}
      </div>

      <p className="text-sm text-gray-600">
        선택됨: {selectedVibes.length} / 4
      </p>

      <div className="flex gap-3">
        <button
          onClick={handleBack}
          className="flex-1 py-3 px-4 bg-gray-200 text-gray-900 font-semibold rounded-lg hover:bg-gray-300 transition"
        >
          ← 이전
        </button>
        <button
          onClick={handleNext}
          disabled={!canProceedStep2}
          className="flex-1 py-3 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
        >
          다음 →
        </button>
      </div>
    </div>
  );
}
