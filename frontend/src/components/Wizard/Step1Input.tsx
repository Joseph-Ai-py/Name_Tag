import React from "react";
import { useWizard } from "../../hooks/useWizard";

export function Step1Input() {
  const {
    businessType,
    keywords,
    setBusinessType,
    setKeywords,
    setStep,
    canProceedStep1,
  } = useWizard();

  const handleNext = () => {
    if (canProceedStep1) {
      setStep(2);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-bold text-light-text dark:text-dark-text mb-3">
          어떤 업종 · 서비스인가요?
        </h2>
        <p className="text-light-text/70 dark:text-dark-text/70 text-base">
          구체적일수록 더 정확한 브랜드를 만들 수 있어요
        </p>
      </div>

      <div className="space-y-5 floating-card p-6">
        <div>
          <label className="block text-sm font-semibold text-light-text dark:text-dark-text mb-3">
            업종/서비스 <span className="text-neon-magenta">*</span>
          </label>
          <input
            type="text"
            value={businessType}
            onChange={(e) => setBusinessType(e.target.value)}
            placeholder="예: 20대를 위한 감성 소품 온라인 셀렉샵"
            className="input-field"
          />
          <p className="mt-2 text-xs text-light-text/50 dark:text-dark-text/50">
            {businessType.length} / 100글자
          </p>
        </div>

        <div>
          <label className="block text-sm font-semibold text-light-text dark:text-dark-text mb-3">
            핵심 키워드 <span className="text-neon-green">(선택)</span>
          </label>
          <input
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="예: 따뜻함, 일상, 발견"
            className="input-field"
          />
          <p className="mt-2 text-xs text-light-text/50 dark:text-dark-text/50">
            쉼표로 구분해서 입력해주세요
          </p>
        </div>
      </div>

      <button
        onClick={handleNext}
        disabled={!canProceedStep1}
        className={`w-full btn-primary ${
          !canProceedStep1 ? "opacity-50 cursor-not-allowed" : ""
        }`}
      >
        다음으로 (Step 2/5) →
      </button>
    </div>
  );
}
