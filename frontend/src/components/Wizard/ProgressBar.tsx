import React from "react";
import { ChevronRight, Check } from "lucide-react";

interface ProgressBarProps {
  currentStep: 1 | 2 | 3 | 4 | 5;
}

const STEPS = ["업종 입력", "감성 선택", "타겟 고객", "생성 중", "결과"];

export function ProgressBar({ currentStep }: ProgressBarProps) {
  return (
    <div className="flex items-center justify-between gap-2">
      {STEPS.map((label, index) => {
        const stepNumber = index + 1;
        const isCompleted = stepNumber < currentStep;
        const isCurrent = stepNumber === currentStep;

        return (
          <React.Fragment key={stepNumber}>
            <div
              className={`flex items-center justify-center w-10 h-10 rounded-full font-semibold transition-colors ${
                isCompleted
                  ? "bg-green-100 text-green-700"
                  : isCurrent
                    ? "bg-blue-100 text-blue-700"
                    : "bg-gray-100 text-gray-500"
              }`}
            >
              {isCompleted ? (
                <Check className="w-6 h-6" />
              ) : (
                stepNumber
              )}
            </div>
            {index < STEPS.length - 1 && (
              <div
                className={`flex-1 h-1 mx-2 transition-colors ${
                  isCompleted ? "bg-green-100" : "bg-gray-100"
                }`}
              />
            )}
          </React.Fragment>
        );
      })}
    </div>
  );
}
