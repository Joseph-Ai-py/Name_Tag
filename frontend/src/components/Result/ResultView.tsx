import React from "react";
import { useWizard } from "../../hooks/useWizard";
import { Download, RotateCcw } from "lucide-react";

export function ResultView() {
  const {
    result,
    selectedBrandIndex,
    setSelectedBrandIndex,
    reset,
  } = useWizard();

  if (!result) return null;

  const brands = result.brands;
  const selectedBrand = brands[selectedBrandIndex];
  const typography = result.typography;
  const character = result.character;

  return (
    <div className="space-y-8">
      {/* Brand Names Section */}
      <div>
        <h2 className="text-3xl font-bold text-light-text dark:text-dark-text mb-6">
          ✨ 브랜드 네이밍 - 3가지 제안
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-8">
          {brands.map((brand, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedBrandIndex(idx)}
              className={`px-4 py-3 rounded-xl font-semibold transition-all ${
                selectedBrandIndex === idx
                  ? "bg-gradient-neon text-white shadow-glow-cyan"
                  : "bg-light-border dark:bg-dark-border/50 text-light-text dark:text-dark-text hover:bg-light-border/80"
              }`}
            >
              {brand.name}
            </button>
          ))}
        </div>

        <div className="floating-card p-8 border-2 border-neon-purple/20 dark:glow-border">
          <h3 className="text-5xl font-black bg-gradient-neon bg-clip-text text-transparent mb-4">
            {selectedBrand.name}
          </h3>
          <p className="text-sm font-semibold text-neon-cyan mb-4">
            🎯 브랜드 의미
          </p>
          <p className="text-light-text/80 dark:text-dark-text/80 mb-6">
            {selectedBrand.meaning}
          </p>

          <p className="text-sm font-semibold text-neon-purple mb-3">
            📖 브랜드 스토리
          </p>
          <p className="text-light-text/80 dark:text-dark-text/80 mb-6 leading-relaxed">
            {selectedBrand.story}
          </p>

          <div className="p-4 rounded-xl bg-gradient-neon/5 border border-neon-purple/20">
            <p className="text-xl italic font-semibold bg-gradient-neon bg-clip-text text-transparent">
              "{selectedBrand.slogan}"
            </p>
          </div>
        </div>
      </div>

      {/* Typography Section */}
      <div>
        <h2 className="text-3xl font-bold text-light-text dark:text-dark-text mb-6">
          🎨 추천 서체
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="floating-card p-6">
            <p className="text-sm font-semibold text-neon-cyan mb-3">한글</p>
            <p className="text-4xl font-bold text-light-text dark:text-dark-text font-serif">
              {typography.korean}
            </p>
          </div>
          <div className="floating-card p-6">
            <p className="text-sm font-semibold text-neon-magenta mb-3">
              English
            </p>
            <p className="text-4xl font-bold text-light-text dark:text-dark-text">
              {typography.english}
            </p>
          </div>
        </div>
        <div className="floating-card p-6 mt-6">
          <p className="text-sm font-semibold text-neon-green mb-3">💡 선택 이유</p>
          <p className="text-light-text/80 dark:text-dark-text/80 leading-relaxed">
            {typography.reason}
          </p>
        </div>
      </div>

      {/* Character Section */}
      <div>
        <h2 className="text-3xl font-bold text-light-text dark:text-dark-text mb-6">
          🎭 브랜드 캐릭터 컨셉
        </h2>
        <div className="floating-card p-8">
          <h3 className="text-4xl font-bold bg-gradient-neon bg-clip-text text-transparent mb-4">
            {character.name}
          </h3>

          <div className="space-y-4">
            <div>
              <p className="text-sm font-semibold text-neon-cyan mb-2">
                컨셉
              </p>
              <p className="text-light-text/80 dark:text-dark-text/80">
                {character.concept}
              </p>
            </div>

            <div className="h-px bg-gradient-neon/20" />

            <div>
              <p className="text-sm font-semibold text-neon-purple mb-2">
                성격 & 특징
              </p>
              <p className="text-light-text/80 dark:text-dark-text/80">
                {character.personality}
              </p>
            </div>

            <div className="h-px bg-gradient-neon/20" />

            <div>
              <p className="text-sm font-semibold text-neon-magenta mb-2">
                시각적 표현
              </p>
              <p className="text-light-text/80 dark:text-dark-text/80">
                {character.visual}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-3 pt-8">
        <button
          onClick={reset}
          className="flex-1 btn-secondary flex items-center justify-center gap-2"
        >
          <RotateCcw size={18} />
          다시 시작하기
        </button>
        <button
          onClick={() => alert("PDF 다운로드는 곧 제공됩니다!")}
          className="flex-1 btn-primary flex items-center justify-center gap-2"
        >
          <Download size={18} />
          PDF 저장하기
        </button>
      </div>
    </div>
  );
}
