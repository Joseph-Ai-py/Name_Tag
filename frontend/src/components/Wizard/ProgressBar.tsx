import React from "react";
import { Check } from "lucide-react";

interface ProgressBarProps {
  currentStep: 1 | 2 | 3 | 4 | 5;
}

const STEPS = ["업종 입력", "감성 선택", "타겟 고객", "생성 중", "결과"];

export function ProgressBar({ currentStep }: ProgressBarProps) {
  return (
    <div className="w-full">
      <div className="flex items-center justify-between gap-2">
        {STEPS.map((label, index) => {
          const stepNumber = index + 1;
          const isCompleted = stepNumber < currentStep;
          const isCurrent = stepNumber === currentStep;

          return (
            <React.Fragment key={stepNumber}>
              {/* Step Circle */}
              <div
                className={`flex items-center justify-center w-12 h-12 rounded-full font-semibold transition-all ${
                  isCompleted
                    ? "bg-gradient-neon text-white shadow-glow"
                    : isCurrent
                      ? "bg-gradient-neon text-white shadow-glow-cyan animate-pulse-glow"
                      : "bg-light-border dark:bg-dark-border/50 text-light-text/50 dark:text-dark-text/50"
                }`}
              >
                {isCompleted ? (
                  <Check className="w-6 h-6" />
                ) : (
                  <span>{stepNumber}</span>
                )}
              </div>

              {/* Step Line */}
              {index < STEPS.length - 1 && (
                <div className="flex-1 h-1 mx-2 overflow-hidden rounded-full">
                  <div
                    className={`h-full transition-all duration-500 ${
                      isCompleted
                        ? "bg-gradient-neon"
                        : "bg-light-border dark:bg-dark-border/30"
                    }`}
                  />
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Step Labels */}
      <div className="flex items-center justify-between gap-2 mt-4">
        {STEPS.map((label, index) => {
          const stepNumber = index + 1;
          const isCompleted = stepNumber < currentStep;
          const isCurrent = stepNumber === currentStep;

          return (
            <div
              key={stepNumber}
              className={`text-xs font-medium text-center flex-1 transition-colors ${
                isCompleted || isCurrent
                  ? "text-neon-purple dark:text-neon-cyan"
                  : "text-light-text/50 dark:text-dark-text/50"
              }`}
            >
              {label}
            </div>
          );
        })}
      </div>
    </div>
  );
}
