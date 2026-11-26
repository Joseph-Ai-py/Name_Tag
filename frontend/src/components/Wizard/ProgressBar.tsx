type StepItem = {
  label: string;
  title: string;
};

type Props = {
  currentStep: 0 | 1 | 2 | 3 | 4 | 5;
  steps: StepItem[];
  stepDetails?: string[];
  onStepChange?: (step: 0 | 1 | 2 | 3 | 4 | 5) => void;
};

export function ProgressBar({ currentStep, steps, stepDetails = [], onStepChange }: Props) {
  return (
    <nav aria-label="보고서 진행 단계" className="w-full space-y-3 rounded-2xl border border-light-border bg-white/80 p-4 shadow-sm dark:border-dark-border dark:bg-dark-bg2/80">
      <div className="flex items-center justify-between gap-2">
        {steps.map((step, index) => {
          const isCurrent = index === currentStep;

          return (
            <div key={step.label} className="flex flex-1 items-center">
              <button
                type="button"
                aria-current={isCurrent ? "step" : undefined}
                aria-label={`${step.label} ${step.title} 단계로 이동`}
                onClick={() => onStepChange?.(index as Props["currentStep"])}
                className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-neon-purple ${
                  isCurrent
                    ? "bg-gradient-neon text-white shadow-glow-cyan"
                    : "border border-light-border bg-light-bg text-light-text/70 hover:border-neon-purple hover:text-neon-purple dark:border-dark-border/50 dark:bg-dark-bg dark:text-dark-text/70 dark:hover:text-neon-cyan"
                }`}
              >
                <span>{step.label}</span>
              </button>

              {index < steps.length - 1 && (
                <div className="mx-2 h-1 flex-1 overflow-hidden rounded-full bg-light-border dark:bg-dark-border/30">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      index < currentStep ? "bg-neon-purple/60 dark:bg-neon-cyan/60" : "bg-light-border dark:bg-dark-border/30"
                    }`}
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-3 gap-2 md:grid-cols-6">
        {steps.map((step, index) => {
          const isCurrent = index === currentStep;

          return (
            <button key={step.label} type="button" onClick={() => onStepChange?.(index as Props["currentStep"])} className={`min-w-0 rounded-lg px-1 py-1 text-center text-xs font-medium transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-neon-purple ${isCurrent ? "text-neon-purple dark:text-neon-cyan" : "text-light-text/60 hover:bg-light-bg dark:text-dark-text/60 dark:hover:bg-dark-bg"}`}>
              <span className="block truncate">{step.title}</span>
              {stepDetails[index] && <span className="mt-0.5 block text-[10px] font-normal text-light-text/50 dark:text-dark-text/50">{stepDetails[index]}</span>}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
