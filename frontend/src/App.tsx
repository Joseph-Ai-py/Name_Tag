import { useMemo } from "react";
import { Sparkles } from "lucide-react";
import { SectionA } from "./pages/SectionA";
import { SectionB } from "./pages/SectionB";
import { SectionC } from "./pages/SectionC";
import { SectionDE } from "./pages/SectionDE";
import { SectionO } from "./pages/SectionO";
import { Preview } from "./pages/Preview";
import { RightSidebar } from "./components/RightSidebar";
import { useBrandStore } from "./store/brandStore";

const stepLabels = ["O", "A", "B", "C", "DE", "Preview"] as const;

function App() {
  const currentStep = useBrandStore((state) => state.currentStep);
  const setCurrentStep = useBrandStore((state) => state.setCurrentStep);
  const reset = useBrandStore((state) => state.reset);

  const steps = useMemo(
    () => [
      { label: "O", title: "브랜드 초안" },
      { label: "A", title: "철학/스토리" },
      { label: "B", title: "타겟/여정" },
      { label: "C", title: "비주얼" },
      { label: "DE", title: "로고/캐릭터" },
      { label: "Preview", title: "PDF 미리보기" },
    ],
    [],
  );

  const content = (() => {
    switch (currentStep) {
      case 0:
        return <SectionO />;
      case 1:
        return <SectionA />;
      case 2:
        return <SectionB />;
      case 3:
        return <SectionC />;
      case 4:
        return <SectionDE />;
      default:
        return <Preview />;
    }
  })();

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(251,191,36,0.16),_transparent_34%),radial-gradient(circle_at_top_right,_rgba(15,118,110,0.12),_transparent_28%),linear-gradient(180deg,#fffdf7_0%,#faf7f0_100%)] text-stone-900">
      <header className="sticky top-0 z-20 border-b border-stone-200/80 bg-white/75 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 md:px-6">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.35em] text-stone-500">NameTag</p>
            <h1 className="mt-1 text-lg font-black tracking-tight md:text-2xl">섹션형 브랜드 가이드 생성기</h1>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={reset}
              className="rounded-full border border-stone-200 bg-white px-4 py-2 text-sm font-medium text-stone-700 transition hover:border-stone-300 hover:bg-stone-50"
            >
              초기화
            </button>
            <div className="hidden items-center gap-2 rounded-full border border-stone-200 bg-white px-4 py-2 text-sm text-stone-600 md:flex">
              <Sparkles size={16} className="text-amber-600" />
              프롬프트 기반 단계 진행
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto grid max-w-[1600px] gap-6 px-4 py-6 lg:grid-cols-[260px_1fr_320px] md:grid-cols-[260px_1fr] md:px-6 md:py-8">
        <aside className="rounded-3xl border border-stone-200 bg-white/80 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.07)] backdrop-blur">
          <div className="mb-5">
            <p className="text-xs font-semibold uppercase tracking-[0.35em] text-stone-500">Workflow</p>
            <h2 className="mt-2 text-xl font-black">진행 단계</h2>
          </div>
          <div className="space-y-3">
            {steps.map((step, index) => (
              <button
                key={step.label}
                type="button"
                onClick={() => setCurrentStep(index as 0 | 1 | 2 | 3 | 4 | 5)}
                className={`flex w-full items-center gap-3 rounded-2xl border px-3 py-3 text-left transition ${
                  currentStep === index
                    ? "border-amber-500 bg-amber-50 shadow-sm"
                    : "border-stone-200 bg-white hover:bg-stone-50"
                }`}
              >
                <div
                  className={`flex h-9 min-w-9 items-center justify-center rounded-full border px-3 text-sm font-semibold transition-all ${
                    currentStep === index
                      ? "border-amber-500 bg-amber-500 text-white shadow-sm"
                      : "border-stone-200 bg-white text-stone-500"
                  }`}
                >
                  {step.label}
                </div>
                <div>
                  <p className="text-sm font-semibold text-stone-900">{step.title}</p>
                  <p className="text-xs text-stone-500">{index === currentStep ? "진행 중" : "대기"}</p>
                </div>
              </button>
            ))}
          </div>

          <div className="mt-6 rounded-2xl bg-stone-50 p-4 text-sm leading-6 text-stone-600">
            <p className="font-semibold text-stone-900">운영 메모</p>
            <p className="mt-2">O부터 DE까지 순서대로 진행하면 브랜드 정보, 인터뷰 응답, 이미지, PDF가 차례로 누적됩니다.</p>
          </div>
        </aside>

        <section className="min-w-0">{content}</section>

        <RightSidebar />
      </main>
    </div>
  );
}

export default App;
