import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, BookOpen, Palette, Sparkles, Moon, Sun } from "lucide-react";

export function Home() {
  const [isDark, setIsDark] = useState(() => {
    if (typeof window === "undefined") return false;
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) return savedTheme === "dark";
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  });

  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDark);
    localStorage.setItem("theme", isDark ? "dark" : "light");
  }, [isDark]);

  const logoSrc = isDark ? "/logo/NameTag_Main_logo_white.png" : "/logo/NameTag_Main_logo_black.png";
  const symbolSrc = isDark ? "/logo/NameTag_Symbol_logo_white.png" : "/logo/NameTag_Symbol_logo_black.png";

  return (
    <div className="min-h-screen bg-gradient-light-bg px-4 py-10 text-light-text dark:bg-gradient-dark-bg dark:text-dark-text sm:px-6 lg:flex lg:items-center lg:justify-center">
      <div className="mx-auto w-full max-w-5xl space-y-10 lg:space-y-12">
        <section className="space-y-6 text-center">
          <div className="mx-auto flex justify-center">
            <div className="relative inline-flex items-center justify-center">
              <img src={logoSrc} alt="NameTag logo" className="h-12 w-auto" />
              <img
                src={symbolSrc}
                alt="NameTag symbol"
                className="absolute -bottom-2 -right-2 h-6 w-6 rounded-full bg-white p-0.5 shadow-md dark:bg-dark-bg"
              />
            </div>
          </div>

          {/* 사이트 헤더 로고는 프론트엔드 정적 파일을 사용합니다. 생성된 로고는 PDF 전용입니다. */}

          <div className="space-y-4">
            <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-[1.75rem] bg-gradient-neon text-white shadow-glow">
              <Sparkles size={34} />
            </div>
            <h1 className="text-5xl font-black tracking-tight md:text-7xl">
              <span className="bg-gradient-neon bg-clip-text text-transparent">NameTag</span>
            </h1>
            <p className="text-2xl font-semibold md:text-3xl">나만의 브랜드를 AI와 함께</p>
          </div>

          {/* 초기 페이지용 야간모드 토글 버튼 (우측 상단 고정) */}
          <button
            type="button"
            onClick={() => setIsDark((v) => !v)}
            aria-label="Toggle theme"
            className="fixed top-4 right-4 z-50 btn-secondary flex items-center gap-2 px-3 py-2"
          >
            {isDark ? <Sun size={18} className="text-neon-cyan" /> : <Moon size={18} className="text-neon-purple" />}
          </button>

          <p className="mx-auto max-w-3xl text-lg leading-8 text-light-text/70 dark:text-dark-text/70 md:text-xl">
            브랜드 이름, 스토리, 비주얼, 로고와 캐릭터까지 하나의 흐름으로 만들 수 있게 정리했습니다.
            <br />
            과거 프론트엔드의 진입 경험을 그대로 살리면서 현재 섹션형 API 흐름에 맞춰 연결합니다.
          </p>
        </section>

        <section className="flex flex-col items-center gap-5">
          <Link
            to="/generate"
            className="btn-primary inline-flex items-center gap-2 px-8 py-4 text-lg shadow-glow hover:shadow-glow-cyan"
          >
            생성 시작하기
            <ArrowRight size={20} />
          </Link>
          <p className="text-sm font-medium text-light-text/60 dark:text-dark-text/60">
            NameTag — AI 기반 브랜드 정체성 생성기: 섹션별 질문으로 브랜드 네임·스토리·비주얼을 만들고 PDF 가이드라인으로 제공합니다.
          </p>
        </section>

        <section className="grid gap-6 md:grid-cols-3">
          <div className="floating-card p-6 text-center">
            <div className="mb-4 flex justify-center">
              <div className="rounded-2xl bg-neon-purple/10 p-3 dark:bg-neon-purple/15">
                <Sparkles size={32} className="text-neon-purple" />
              </div>
            </div>
            <h3 className="mb-2 font-bold">브랜드 네이밍</h3>
            <p className="text-sm text-light-text/60 dark:text-dark-text/60">브랜드 후보와 핵심 스토리를 단계적으로 확정합니다.</p>
          </div>

          <div className="floating-card p-6 text-center">
            <div className="mb-4 flex justify-center">
              <div className="rounded-2xl bg-neon-cyan/10 p-3 dark:bg-neon-cyan/15">
                <BookOpen size={32} className="text-neon-cyan" />
              </div>
            </div>
            <h3 className="mb-2 font-bold">스토리텔링</h3>
            <p className="text-sm text-light-text/60 dark:text-dark-text/60">인터뷰 응답이 다음 섹션으로 자연스럽게 이어집니다.</p>
          </div>

          <div className="floating-card p-6 text-center">
            <div className="mb-4 flex justify-center">
              <div className="rounded-2xl bg-neon-magenta/10 p-3 dark:bg-neon-magenta/15">
                <Palette size={32} className="text-neon-magenta" />
              </div>
            </div>
            <h3 className="mb-2 font-bold">디자인 가이드</h3>
            <p className="text-sm text-light-text/60 dark:text-dark-text/60">비주얼과 로고/캐릭터까지 한 번에 연결합니다.</p>
          </div>
        </section>

        <section className="flex items-center gap-4 py-2">
          <div className="h-px flex-1 bg-gradient-to-r from-transparent via-neon-purple/30 to-transparent" />
          <span className="text-sm text-light-text/50 dark:text-dark-text/50">다른 패키지는 준비 중입니다</span>
          <div className="h-px flex-1 bg-gradient-to-r from-transparent via-neon-purple/30 to-transparent" />
        </section>

        <section className="floating-card border-2 border-neon-cyan/20 p-6 dark:glow-border">
          <div className="flex items-start gap-4">
            <Sparkles size={24} className="mt-1 flex-shrink-0 text-neon-cyan" />
            <div>
              <h3 className="mb-1 font-semibold">AI 기반 맞춤형 브랜드 생성</h3>
              <p className="text-sm leading-7 text-light-text/70 dark:text-dark-text/70">
                Google Gemini와 현재 백엔드 섹션 API를 연결해 브랜드 정체성을 만들고 PDF로 정리합니다.
              </p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}