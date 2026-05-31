import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Moon, Sun } from "lucide-react";

export function Header() {
  const [isDark, setIsDark] = useState(() => {
    if (typeof window === "undefined") {
      return false;
    }

    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
      return savedTheme === "dark";
    }

    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  });

  useEffect(() => {
    document.documentElement.classList.toggle("dark", isDark);
    localStorage.setItem("theme", isDark ? "dark" : "light");
  }, [isDark]);

  const logoSrc = isDark ? "/logo/logo_white.png" : "/logo/logo_black.png";

  return (
    <header className="sticky top-0 z-50 border-b border-light-border/80 bg-white/75 backdrop-blur-md dark:border-dark-border/50 dark:bg-dark-bg2/75">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-4 md:px-6">
        <Link to="/" className="flex items-center gap-3 transition hover:opacity-80">
          <img src={logoSrc} alt="NameTag" className="h-11 w-11 rounded-2xl object-contain" />
          <div>
            <h1 className="text-2xl font-bold tracking-tight">NameTag</h1>
            <p className="text-xs font-medium text-light-text/60 dark:text-dark-text/60">AI 브랜드 정체성 생성기</p>
          </div>
        </Link>

        <button
          type="button"
          onClick={() => setIsDark((value) => !value)}
          className="btn-secondary flex items-center gap-2 px-3 py-2"
          aria-label="Toggle theme"
        >
          {isDark ? <Sun size={18} className="text-neon-cyan" /> : <Moon size={18} className="text-neon-purple" />}
        </button>
      </div>
    </header>
  );
}