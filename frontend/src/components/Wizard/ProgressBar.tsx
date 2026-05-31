import { Check } from "lucide-react";

type StepItem = {
  label: string;
  title: string;
};

type Props = {
  currentStep: 0 | 1 | 2 | 3 | 4 | 5;
  steps: StepItem[];
};

export function ProgressBar({ currentStep, steps }: Props) {
  return (
    <div className="w-full space-y-4">
      <div className="flex items-center justify-between gap-2">
        {steps.map((step, index) => {
          const isCompleted = index < currentStep;
          const isCurrent = index === currentStep;

          return (
            <div key={step.label} className="flex flex-1 items-center">
              <div
                className={`flex h-12 w-12 items-center justify-center rounded-full text-sm font-semibold transition-all ${
                  isCompleted
                    ? "bg-gradient-neon text-white shadow-glow"
                    : isCurrent
                      ? "bg-gradient-neon text-white shadow-glow-cyan animate-pulse"
                      : "border border-light-border bg-light-bg text-light-text/50 dark:border-dark-border/50 dark:bg-dark-bg2 dark:text-dark-text/50"
                }`}
              >
                {isCompleted ? <Check className="h-6 w-6" /> : <span>{step.label}</span>}
              </div>

              {index < steps.length - 1 && (
                <div className="mx-2 h-1 flex-1 overflow-hidden rounded-full bg-light-border dark:bg-dark-border/30">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      isCompleted ? "bg-gradient-neon" : "bg-light-border dark:bg-dark-border/30"
                    }`}
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="flex items-center justify-between gap-2">
        {steps.map((step, index) => {
          const isActive = index <= currentStep;

          return (
            <div key={step.label} className={`flex-1 text-center text-xs font-medium ${isActive ? "text-neon-purple dark:text-neon-cyan" : "text-light-text/50 dark:text-dark-text/50"}`}>
              {step.title}
            </div>
          );
        })}
      </div>
    </div>
  );
}