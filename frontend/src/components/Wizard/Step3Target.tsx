import React from "react";
import { useWizard } from "../../hooks/useWizard";
import { useGenerate } from "../../hooks/useGenerate";

export function Step3Target() {
  const {
    target,
    setTarget,
    setStep,
    error,
    canProceedStep3,
    businessType,
    selectedVibes,
    keywords,
  } = useWizard();

  const generateMutation = useGenerate();

  const handleBack = () => setStep(2);

  const handleGenerate = async () => {
    if (canProceedStep3) {
      generateMutation.mutate({
        business_type: businessType,
        vibes: selectedVibes,
        target: target,
        keywords: keywords,
      });
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          주요 타겟 고객은 누구인가요?
        </h2>
        <p className="text-gray-600">
          나이, 직업, 라이프스타일 등을 자유롭게 설명해주세요
        </p>
      </div>

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          타겟 고객 설명 *
        </label>
        <textarea
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          placeholder="예: 30대 직장 여성, 소소한 취미생활을 즐기고 자신만의 공간을 꾸미는 것에 관심 있는 분들"
          rows={6}
          className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition resize-none"
        />
        <p className="mt-1 text-xs text-gray-500">
          {target.length} / 500글자
        </p>
      </div>

      <div className="flex gap-3">
        <button
          onClick={handleBack}
          className="flex-1 py-3 px-4 bg-gray-200 text-gray-900 font-semibold rounded-lg hover:bg-gray-300 transition disabled:opacity-50"
          disabled={generateMutation.isPending}
        >
          ← 이전
        </button>
        <button
          onClick={handleGenerate}
          disabled={!canProceedStep3 || generateMutation.isPending}
          className="flex-1 py-3 px-4 bg-violet-600 text-white font-semibold rounded-lg hover:bg-violet-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
        >
          {generateMutation.isPending ? "생성 중..." : "✦ 브랜드 생성"}
        </button>
      </div>
    </div>
  );
}
