import React from "react";
import { useWizard } from "../../hooks/useWizard";
import { Sparkles } from "lucide-react";

export function Step4Loading() {
  const { currentStep } = useWizard();

  const steps = [
    "업종 · 키워드 분석 중",
    "브랜드 네임 도출 중",
    "스토리텔링 작성 중",
    "서체 · 캐릭터 설계 중",
  ];

  const [currentLoadingStep, setCurrentLoadingStep] = React.useState(0);

  React.useEffect(() => {
    const interval = setInterval(() => {
      setCurrentLoadingStep((prev) => (prev + 1) % steps.length);
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center justify-center py-20 space-y-8">
      {/* Animated Spinner */}
      <div className="relative w-16 h-16">
        <div className="spinner" />
        <div className="absolute inset-0 flex items-center justify-center">
          <Sparkles size={24} className="text-neon-cyan animate-pulse" />
        </div>
      </div>

      {/* Loading Info */}
      <div className="text-center space-y-3">
        <p className="text-lg font-semibold bg-gradient-neon bg-clip-text text-transparent animate-pulse">
          {steps[currentLoadingStep]}
        </p>
        <p className="text-sm text-light-text/60 dark:text-dark-text/60">
          예상 소요 시간: 10~15초
        </p>
      </div>

      {/* Progress Bar */}
      <div className="w-full max-w-xs progress-bar">
        <div
          className="progress-fill"
          style={{
            width: `${((currentLoadingStep + 1) / steps.length) * 100}%`,
          }}
        />
      </div>

      {/* Step Indicators */}
      <div className="flex gap-2 mt-4">
        {steps.map((_, index) => (
          <div
            key={index}
            className={`h-1 rounded-full transition-all ${
              index <= currentLoadingStep
                ? "bg-gradient-neon w-8"
                : "bg-light-border dark:bg-dark-border w-2"
            }`}
          />
        ))}
      </div>
    </div>
  );
}
