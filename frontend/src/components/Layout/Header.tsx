import React, { useState } from "react";
import { Moon, Sun } from "lucide-react";

export function Header() {
  const [isDark, setIsDark] = useState(
    document.documentElement.classList.contains("dark")
  );

  const toggleTheme = () => {
    const html = document.documentElement;
    if (isDark) {
      html.classList.remove("dark");
      localStorage.setItem("theme", "light");
    } else {
      html.classList.add("dark");
      localStorage.setItem("theme", "dark");
    }
    setIsDark(!isDark);
  };

  return (
    <header className="sticky top-0 z-50 bg-white dark:bg-dark-bg2 backdrop-blur-md border-b border-light-border dark:border-dark-border/50 shadow-soft dark:shadow-soft-dark">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        {/* Logo & Brand */}
        <a href="/" className="flex items-center gap-3 hover:opacity-80 transition">
          <img 
            src={isDark ? "/logo_white.png" : "/logo_black.png"}
            alt="NameTag Logo"
            className="h-10 w-auto"
          />
          <div>
            <h1 className="text-2xl font-bold bg-gradient-neon bg-clip-text text-transparent">
              NameTag
            </h1>
            <p className="text-xs text-light-text/60 dark:text-dark-text/60 font-medium">
              AI 브랜드 정체성 생성기
            </p>
          </div>
        </a>

        {/* Theme Toggle */}
        <button
          onClick={toggleTheme}
          className="btn-secondary p-2"
          aria-label="Toggle theme"
        >
          {isDark ? (
            <Sun size={20} className="text-neon-cyan" />
          ) : (
            <Moon size={20} className="text-neon-purple" />
          )}
        </button>
      </div>
    </header>
  );
}
