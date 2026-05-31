import { useMemo } from "react";
import { Header } from "../components/Layout/Header";
import { Footer } from "../components/Layout/Footer";
import { ProgressBar } from "../components/Wizard/ProgressBar";
import { RightSidebar } from "../components/RightSidebar";
import { SectionA } from "./SectionA";
import { SectionB } from "./SectionB";
import { SectionC } from "./SectionC";
import { SectionDE } from "./SectionDE";
import { SectionO } from "./SectionO";
import { Preview } from "./Preview";
import { useBrandStore } from "../store/brandStore";

export function Generate() {
  const currentStep = useBrandStore((state) => state.currentStep);
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

  const showSidebar = currentStep === 5;

  return (
    <div className="min-h-screen bg-gradient-light-bg text-light-text dark:bg-gradient-dark-bg dark:text-dark-text">
      <Header />

      <main className="mx-auto flex w-full max-w-[1600px] gap-6 px-4 py-6 md:px-6 md:py-8">
        <div className={`min-w-0 flex-1 ${showSidebar ? "overflow-hidden" : ""}`}>
          <div className={`mx-auto w-full max-w-5xl ${showSidebar ? "h-full overflow-y-auto" : ""}`}>
            <div className="mb-10 space-y-3">
              <p className="text-xs font-semibold uppercase tracking-[0.35em] text-light-text/50 dark:text-dark-text/50">Generate</p>
              <h1 className="text-4xl font-black tracking-tight md:text-5xl">나만의 브랜드 정체성 만들기</h1>
              <p className="text-lg text-light-text/70 dark:text-dark-text/70">
                섹션 O, A, B, C, DE를 순서대로 진행한 뒤 PDF 미리보기까지 연결합니다.
              </p>
            </div>

            <div className="mb-12 rounded-[2rem] border border-light-border bg-white/80 p-6 shadow-soft backdrop-blur dark:border-dark-border dark:bg-dark-bg2/80 dark:shadow-soft-dark md:p-8">
              <ProgressBar currentStep={currentStep} steps={steps} />
            </div>

            <div className="floating-card p-6 md:p-10">{content}</div>
          </div>
        </div>

        {showSidebar && <RightSidebar />}
      </main>

      <Footer />
    </div>
  );
}