import { Header } from "../components/Layout/Header";
import { Footer } from "../components/Layout/Footer";
import { ProgressBar } from "../components/Wizard/ProgressBar";
import { SectionO } from "./SectionO";
import { SectionA } from "./SectionA";
import { SectionB } from "./SectionB";
import { SectionC } from "./SectionC";
import { SectionDE } from "./SectionDE";
import { Preview } from "./Preview";
import { useBrandStore } from "../store/brandStore";

const steps = [
  { label: "01", title: "브랜드 기초" },
  { label: "02", title: "사업·포지셔닝" },
  { label: "03", title: "고객·가치" },
  { label: "04", title: "시장·사업 모델" },
  { label: "05", title: "시각 정체성" },
  { label: "06", title: "검토·PDF" },
];
const stepPageIds = [
  ["00", "02", "03", "04"],
  ["05", "06"],
  ["07", "08", "09", "10", "18"],
  ["11", "12", "13", "14", "15", "16", "17", "23", "24"],
  ["19", "20", "21", "22"],
  ["01"],
];

export function Generate() {
  const currentStep = useBrandStore((state) => state.currentStep);
  const setCurrentStep = useBrandStore((state) => state.setCurrentStep);
  const report = useBrandStore((state) => state.reportV2);
  const stepDetails = stepPageIds.map((pageIds) => {
    const count = pageIds.filter((pageId) => report.pages[pageId]).length;
    return count ? `${count}페이지 저장` : "";
  });
  const page = [
    <SectionO key="o" />,
    <SectionA key="a" />,
    <SectionB key="b" />,
    <SectionC key="c" />,
    <SectionDE key="de" />,
    <Preview key="preview" />,
  ][currentStep];

  return (
    <div className="min-h-screen bg-gradient-light-bg text-light-text dark:bg-gradient-dark-bg dark:text-dark-text">
      <Header />
      <main className="mx-auto w-full max-w-6xl px-4 py-8 md:px-6">
        <div className="space-y-6">
          <ProgressBar currentStep={currentStep} steps={steps} stepDetails={stepDetails} onStepChange={setCurrentStep} />
          {page}
          <div className="flex justify-between gap-3 rounded-2xl border border-stone-200 bg-white/80 p-4">
            <button type="button" className="btn-secondary px-4 py-2" disabled={currentStep === 0} onClick={() => setCurrentStep((currentStep - 1) as 0 | 1 | 2 | 3 | 4 | 5)}>이전 단계</button>
            <p className="self-center text-xs text-stone-500">{currentStep + 1} / {steps.length} · 새로고침 전까지 작성 중인 내용이 이어집니다</p>
            <button type="button" className="btn-primary px-4 py-2" disabled={currentStep === 5} onClick={() => setCurrentStep((currentStep + 1) as 0 | 1 | 2 | 3 | 4 | 5)}>다음 단계</button>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
