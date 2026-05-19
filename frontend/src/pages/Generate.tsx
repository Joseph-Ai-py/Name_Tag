import React from "react";
import { useWizard } from "../hooks/useWizard";
import { Header } from "../components/Layout/Header";
import { Footer } from "../components/Layout/Footer";
import { ProgressBar } from "../components/Wizard/ProgressBar";
import { Step1Input } from "../components/Wizard/Step1Input";
import { Step2Vibe } from "../components/Wizard/Step2Vibe";
import { Step3Target } from "../components/Wizard/Step3Target";
import { Step4Loading } from "../components/Wizard/Step4Loading";
import { ResultView } from "../components/Result/ResultView";
import { LogoDesignSidebar } from "../components/Sidebar/LogoDesignSidebar";
import { useGenerationStore } from "../stores/generationStore";

export function Generate() {
  const { currentStep, isLoading, result, selectedBrandIndex } = useWizard();
  const { setGeneratedLogo, images } = useGenerationStore();

  const showSidebar = result && currentStep === 5;
  const selectedBrand = result?.brands[selectedBrandIndex];

  return (
    <div className="min-h-screen flex flex-col bg-gradient-light-bg dark:bg-gradient-dark-bg">
      <Header />

      <main className="flex-1 flex">
        {/* Main Content */}
        <div className={`flex-1 ${showSidebar ? "overflow-hidden" : ""}`}>
          <div className={`max-w-5xl mx-auto w-full px-4 py-12 ${showSidebar ? "h-full overflow-y-auto" : ""}`}>
            <div className="mb-10">
              <h1 className="text-4xl md:text-5xl font-black bg-gradient-neon bg-clip-text text-transparent mb-3">
                나만의 브랜드 정체성 만들기
              </h1>
              <p className="text-lg text-light-text/70 dark:text-dark-text/70">
                브랜드 네이밍 · 스토리텔링 · 서체 · 캐릭터를 AI가 함께 설계합니다
              </p>
            </div>

            <div className="mb-12 bg-light-bg dark:bg-dark-bg2 rounded-2xl p-8">
              <ProgressBar currentStep={currentStep} />
            </div>

            <div className="floating-card p-8 md:p-10">
              {currentStep === 1 && <Step1Input />}
              {currentStep === 2 && <Step2Vibe />}
              {currentStep === 3 && <Step3Target />}
              {currentStep === 4 && <Step4Loading />}
              {currentStep === 5 && <ResultView />}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        {showSidebar && selectedBrand && (
          <div className="hidden lg:block w-80 border-l border-light-border dark:border-dark-border bg-light-bg dark:bg-dark-bg2 overflow-y-auto">
            <LogoDesignSidebar
              brandIndex={selectedBrandIndex}
              logoDesignInfo={selectedBrand.logo_design}
              isGenerating={images.isGeneratingLogo}
              onImageGenerated={(image, filename) => {
                setGeneratedLogo(selectedBrandIndex, image, filename);
              }}
            />
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
