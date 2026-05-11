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
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          어떤 업종 · 서비스인가요?
        </h2>
        <p className="text-gray-600">
          구체적일수록 더 정확한 브랜드를 만들 수 있어요
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            업종/서비스 *
          </label>
          <input
            type="text"
            value={businessType}
            onChange={(e) => setBusinessType(e.target.value)}
            placeholder="예: 20대를 위한 감성 소품 온라인 셀렉샵"
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
          />
          <p className="mt-1 text-xs text-gray-500">
            {businessType.length} / 100글자
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            핵심 키워드 (선택)
          </label>
          <input
            type="text"
            value={keywords}
            onChange={(e) => setKeywords(e.target.value)}
            placeholder="예: 따뜻함, 일상, 발견"
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
          />
          <p className="mt-1 text-xs text-gray-500">
            쉼표로 구분해서 입력해주세요
          </p>
        </div>
      </div>

      <button
        onClick={handleNext}
        disabled={!canProceedStep1}
        className="w-full py-3 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
      >
        다음 →
      </button>
    </div>
  );
}
