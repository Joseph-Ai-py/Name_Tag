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
        <h2 className="text-3xl font-bold text-light-text dark:text-dark-text mb-3">
          브랜드 감성을 선택해주세요
        </h2>
        <p className="text-light-text/70 dark:text-dark-text/70 text-base">
          최대 4개까지 선택 가능합니다
        </p>
      </div>

      <div className="floating-card p-6">
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
          {VIBES.map((vibe) => (
            <button
              key={vibe}
              onClick={() => toggleVibe(vibe)}
              className={`px-4 py-3 rounded-xl font-medium transition-all ${
                selectedVibes.includes(vibe)
                  ? "bg-gradient-neon text-white shadow-glow-cyan"
                  : "bg-light-border dark:bg-dark-border/50 text-light-text dark:text-dark-text hover:bg-light-border/80 dark:hover:bg-dark-border"
              }`}
            >
              {vibe}
            </button>
          ))}
        </div>

        <p className="mt-6 text-sm text-light-text/60 dark:text-dark-text/60 font-medium">
          선택됨: <span className="text-neon-purple dark:text-neon-cyan">{selectedVibes.length}</span> / 4
        </p>
      </div>

      <div className="flex gap-3">
        <button
          onClick={handleBack}
          className="flex-1 btn-secondary"
        >
          ← 이전
        </button>
        <button
          onClick={handleNext}
          disabled={!canProceedStep2}
          className={`flex-1 btn-primary ${
            !canProceedStep2 ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          다음으로 (Step 3/5) →
        </button>
      </div>
    </div>
  );
}
