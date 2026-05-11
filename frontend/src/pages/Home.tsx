import React from "react";
import { useNavigate } from "react-router-dom";
import { Sparkles, BookOpen, Palette, ArrowRight } from "lucide-react";

export function Home() {
  const navigate = useNavigate();
  const isDark = document.documentElement.classList.contains("dark");

  return (
    <div className="min-h-screen bg-gradient-light-bg dark:bg-gradient-dark-bg flex items-center justify-center px-4">
      <div className="max-w-3xl w-full space-y-12">
        {/* Hero Section */}
        <div className="text-center space-y-6">
          <div className="space-y-4">
            {/* Logo */}
            <div className="inline-block">
              <img 
                src={isDark ? "/logo_white.png" : "/logo_black.png"}
                alt="NameTag Logo"
                className="h-24 w-auto mx-auto mb-4 hover:scale-105 transition-transform"
              />
            </div>
            <h1 className="text-6xl md:text-7xl font-black bg-gradient-neon bg-clip-text text-transparent">
              NameTag
            </h1>
            <p className="text-2xl md:text-3xl font-semibold text-light-text dark:text-dark-text">
              나만의 브랜드를 AI와 함께
            </p>
          </div>

          <p className="text-lg text-light-text/70 dark:text-dark-text/70 max-w-2xl mx-auto leading-relaxed">
            브랜드 이름, 스토리, 서체, 캐릭터까지 AI가 한 번에 만들어줍니다.
            <br />
            당신의 비즈니스에 맞는 완벽한 브랜드 정체성을 발견해보세요.
          </p>
        </div>

        {/* CTA Button */}
        <div className="flex flex-col items-center gap-6">
          <button
            onClick={() => navigate("/generate")}
            className="btn-primary px-8 py-4 text-lg font-semibold flex items-center gap-2 shadow-glow hover:shadow-glow-cyan"
          >
            <Sparkles size={20} />
            패키지 A 시작하기
            <ArrowRight size={20} />
          </button>
          <p className="text-sm text-light-text/60 dark:text-dark-text/60 font-medium">
            약 2분 소요 | 무료 이용 가능
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          {/* Feature 1 */}
          <div className="floating-card p-6 text-center group">
            <div className="mb-4 flex justify-center">
              <div className="p-3 rounded-xl bg-gradient-neon/10 group-hover:bg-gradient-neon/20 transition">
                <Sparkles size={32} className="text-neon-purple" />
              </div>
            </div>
            <h3 className="font-bold text-light-text dark:text-dark-text mb-2">
              브랜드 네이밍
            </h3>
            <p className="text-sm text-light-text/60 dark:text-dark-text/60">
              맞춤형 이름 3개
            </p>
          </div>

          {/* Feature 2 */}
          <div className="floating-card p-6 text-center group">
            <div className="mb-4 flex justify-center">
              <div className="p-3 rounded-xl bg-gradient-neon/10 group-hover:bg-gradient-neon/20 transition">
                <BookOpen size={32} className="text-neon-cyan" />
              </div>
            </div>
            <h3 className="font-bold text-light-text dark:text-dark-text mb-2">
              스토리텔링
            </h3>
            <p className="text-sm text-light-text/60 dark:text-dark-text/60">
              감정 있는 설명 & 슬로건
            </p>
          </div>

          {/* Feature 3 */}
          <div className="floating-card p-6 text-center group">
            <div className="mb-4 flex justify-center">
              <div className="p-3 rounded-xl bg-gradient-neon/10 group-hover:bg-gradient-neon/20 transition">
                <Palette size={32} className="text-neon-magenta" />
              </div>
            </div>
            <h3 className="font-bold text-light-text dark:text-dark-text mb-2">
              디자인 가이드
            </h3>
            <p className="text-sm text-light-text/60 dark:text-dark-text/60">
              서체 & 캐릭터 설계
            </p>
          </div>
        </div>

        {/* Divider */}
        <div className="flex items-center gap-4 py-8">
          <div className="flex-1 h-px bg-gradient-to-r from-transparent via-neon-purple/30 to-transparent" />
          <span className="text-sm text-light-text/50 dark:text-dark-text/50">
            다른 패키지는 준비 중입니다
          </span>
          <div className="flex-1 h-px bg-gradient-to-r from-transparent via-neon-purple/30 to-transparent" />
        </div>

        {/* Info Box */}
        <div className="floating-card p-6 border-2 border-neon-cyan/20 dark:glow-border">
          <div className="flex items-start gap-4">
            <Sparkles size={24} className="text-neon-cyan flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-light-text dark:text-dark-text mb-1">
                🚀 AI 기반 맞춤형 브랜드 생성
              </h3>
              <p className="text-sm text-light-text/70 dark:text-dark-text/70">
                Google Gemini AI가 당신의 비즈니스를 분석하여 독특하고 효과적인 브랜드 정체성을 만들어줍니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
