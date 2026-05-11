import React from "react";
import { useWizard } from "../../hooks/useWizard";
import { useGenerate } from "../../hooks/useGenerate";
import { Zap } from "lucide-react";

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
        <h2 className="text-3xl font-bold text-light-text dark:text-dark-text mb-3">
          주요 타겟 고객은 누구인가요?
        </h2>
        <p className="text-light-text/70 dark:text-dark-text/70 text-base">
          나이, 직업, 라이프스타일 등을 자유롭게 설명해주세요
        </p>
      </div>

      {error && (
        <div className="p-4 bg-neon-magenta/10 border border-neon-magenta/30 rounded-xl">
          <p className="text-sm text-neon-magenta font-medium">{error}</p>
        </div>
      )}

      <div className="floating-card p-6">
        <label className="block text-sm font-semibold text-light-text dark:text-dark-text mb-3">
          타겟 고객 설명 <span className="text-neon-magenta">*</span>
        </label>
        <textarea
          value={target}
          onChange={(e) => setTarget(e.target.value)}
          placeholder="예: 30대 직장 여성, 소소한 취미생활을 즐기고 자신만의 공간을 꾸미는 것에 관심 있는 분들"
          rows={6}
          className="input-field resize-none"
        />
        <p className="mt-2 text-xs text-light-text/50 dark:text-dark-text/50">
          {target.length} / 500글자
        </p>
      </div>

      <div className="flex gap-3">
        <button
          onClick={handleBack}
          className="flex-1 btn-secondary"
          disabled={generateMutation.isPending}
        >
          ← 이전
        </button>
        <button
          onClick={handleGenerate}
          disabled={!canProceedStep3 || generateMutation.isPending}
          className={`flex-1 btn-primary flex items-center justify-center gap-2 ${
            !canProceedStep3 || generateMutation.isPending
              ? "opacity-50 cursor-not-allowed"
              : ""
          }`}
        >
          <Zap size={18} />
          {generateMutation.isPending ? "생성 중..." : "브랜드 생성"}
        </button>
      </div>
    </div>
  );
}
