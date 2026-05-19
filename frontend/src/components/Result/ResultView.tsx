import React, { useState } from "react";
import { useWizard } from "../../hooks/useWizard";
import { Download, RotateCcw, Wand2, Loader } from "lucide-react";
import { generateCharacter } from "../../lib/api";
import { useGenerationStore } from "../../stores/generationStore";

export function ResultView() {
  const {
    result,
    selectedBrandIndex,
    setSelectedBrandIndex,
    reset,
  } = useWizard();

  const {
    images,
    setCharacterImage,
    setIsGeneratingCharacter,
    generatedLogos,
    setGeneratedLogo,
  } = useGenerationStore();

  if (!result) return null;

  const brands = result.brands;
  const selectedBrand = brands[selectedBrandIndex];
  const logoDesign = selectedBrand.logo_design[0];
  const generatedLogo = generatedLogos[selectedBrandIndex];

  const handleGenerateCharacter = async () => {
    setIsGeneratingCharacter(true);
    try {
      const data = await generateCharacter({
        character_name: selectedBrand.character[0].name,
        character_concept: selectedBrand.character[0].concept,
        character_visual: selectedBrand.character[0].visual,
        vibes: [],
      });
      setCharacterImage(`data:image/png;base64,${data.image}`);
    } catch (error) {
      alert("캐릭터 생성에 실패했습니다. 다시 시도해주세요.");
      console.error(error);
    } finally {
      setIsGeneratingCharacter(false);
    }
  };

  const handleDownloadLogo = () => {
    if (!generatedLogo?.image) return;
    const link = document.createElement("a");
    link.href = generatedLogo.image;
    link.download = generatedLogo.filename || "logo.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

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

      {/* Logo Generation Section */}
      <div>
        <h2 className="text-3xl font-bold text-light-text dark:text-dark-text mb-6">
          🎨 로고 디자인 정보
        </h2>
        <div className="floating-card p-8">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-8">
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                브랜드 이름
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.brand_name}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                사업 주제
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.brand_topic}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                핵심 가치
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.core_value}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                타겟 감성
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.target_mood}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                서체 스타일
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.font_style}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                서체 참고
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.font_reference}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                심볼 스타일
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.symbol_type}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                서체 굵기
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.font_weight}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                로고 유형
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.logo_type}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                배경
              </p>
              <p className="font-semibold text-light-text dark:text-dark-text truncate">
                {logoDesign.background}
              </p>
            </div>
            <div className="p-4 rounded-lg bg-light-border/50 dark:bg-dark-border/50">
              <p className="text-xs text-light-text/60 dark:text-dark-text/60 mb-1">
                브랜드 색상
              </p>
              <div className="flex items-center gap-2">
                <div
                  className="w-6 h-6 rounded border border-light-border/50"
                  style={{ backgroundColor: logoDesign.brand_color }}
                />
                <p className="font-mono text-sm text-light-text dark:text-dark-text">
                  {logoDesign.brand_color}
                </p>
              </div>
            </div>
          </div>

          {generatedLogo?.image ? (
            <div className="flex flex-col items-center gap-4">
              <img
                src={generatedLogo.image}
                alt="Generated Logo"
                className="max-w-sm max-h-96 rounded-lg border-2 border-neon-cyan/30"
              />
              <button
                onClick={handleDownloadLogo}
                className="btn-primary flex items-center justify-center gap-2"
              >
                <Download size={18} />
                로고 다운로드
              </button>
            </div>
          ) : (
            <p className="text-center text-light-text/60 dark:text-dark-text/60 py-8">
              사이드바에서 "🎨 로고 이미지 생성"을 클릭하여 로고를 생성하세요
            </p>
          )}
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
              {selectedBrand.typography[0].korean}
            </p>
          </div>
          <div className="floating-card p-6">
            <p className="text-sm font-semibold text-neon-magenta mb-3">
              English
            </p>
            <p className="text-4xl font-bold text-light-text dark:text-dark-text">
              {selectedBrand.typography[0].english}
            </p>
          </div>
        </div>
        <div className="floating-card p-6 mt-6">
          <p className="text-sm font-semibold text-neon-green mb-3">💡 선택 이유</p>
          <p className="text-light-text/80 dark:text-dark-text/80 leading-relaxed">
            {selectedBrand.typography[0].reason}
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
            {selectedBrand.character[0].name}
          </h3>

          <div className="space-y-4">
            <div>
              <p className="text-sm font-semibold text-neon-cyan mb-2">
                컨셉
              </p>
              <p className="text-light-text/80 dark:text-dark-text/80">
                {selectedBrand.character[0].concept}
              </p>
            </div>

            <div className="h-px bg-gradient-neon/20" />

            <div>
              <p className="text-sm font-semibold text-neon-purple mb-2">
                성격 & 특징
              </p>
              <p className="text-light-text/80 dark:text-dark-text/80">
                {selectedBrand.character[0].personality}
              </p>
            </div>

            <div className="h-px bg-gradient-neon/20" />

            <div>
              <p className="text-sm font-semibold text-neon-magenta mb-2">
                시각적 표현
              </p>
              <p className="text-light-text/80 dark:text-dark-text/80">
                {selectedBrand.character[0].visual}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Character Image Generation Section */}
      <div>
        <h2 className="text-3xl font-bold text-light-text dark:text-dark-text mb-6">
          🤖 캐릭터 이미지
        </h2>
        <div className="floating-card p-8">
          {images.characterImage ? (
            <div className="flex flex-col items-center gap-4">
              <img
                src={images.characterImage}
                alt="Generated Character"
                className="max-w-sm max-h-96 rounded-lg border-2 border-neon-magenta/30"
              />
              <button
                onClick={handleGenerateCharacter}
                disabled={images.isGeneratingCharacter}
                className="btn-secondary flex items-center justify-center gap-2"
              >
                {images.isGeneratingCharacter ? (
                  <>
                    <Loader size={18} className="animate-spin" />
                    생성 중...
                  </>
                ) : (
                  <>
                    <Wand2 size={18} />
                    다시 생성하기
                  </>
                )}
              </button>
            </div>
          ) : (
            <button
              onClick={handleGenerateCharacter}
              disabled={images.isGeneratingCharacter}
              className="w-full btn-primary flex items-center justify-center gap-2 py-6"
            >
              {images.isGeneratingCharacter ? (
                <>
                  <Loader size={18} className="animate-spin" />
                  캐릭터 생성 중...
                </>
              ) : (
                <>
                  <Wand2 size={18} />
                  AI로 캐릭터 생성하기
                </>
              )}
            </button>
          )}
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
