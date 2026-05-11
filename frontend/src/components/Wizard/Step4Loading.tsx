import React from "react";
import { useWizard } from "../../hooks/useWizard";
import { Loader2 } from "lucide-react";

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
      <Loader2 className="w-12 h-12 text-blue-600 animate-spin" />
      <div className="text-center space-y-2">
        <p className="text-lg font-semibold text-gray-900">
          {steps[currentLoadingStep]}
        </p>
        <p className="text-sm text-gray-600">
          예상 소요 시간: 10~15초
        </p>
      </div>

      <div className="w-full max-w-xs bg-gray-100 rounded-full h-2">
        <div
          className="bg-blue-600 h-2 rounded-full transition-all duration-500"
          style={{
            width: `${((currentLoadingStep + 1) / steps.length) * 100}%`,
          }}
        />
      </div>
    </div>
  );
}
