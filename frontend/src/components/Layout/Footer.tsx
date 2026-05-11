import React from "react";

export function Footer() {
  return (
    <footer className="mt-16 py-12 border-t border-light-border dark:border-dark-border/50 bg-light-bg dark:bg-dark-bg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center gap-8 mb-8">
          {/* Brand */}
          <div>
            <div className="text-2xl font-bold bg-gradient-neon bg-clip-text text-transparent mb-2">
              NameTag
            </div>
            <p className="text-sm text-light-text/70 dark:text-dark-text/70">
              AI로 만드는 브랜드 정체성
            </p>
          </div>

          {/* Links */}
          <div className="flex gap-8">
            <a
              href="#"
              className="text-sm text-light-text/60 dark:text-dark-text/60 hover:text-neon-purple transition-colors"
            >
              Privacy
            </a>
            <a
              href="#"
              className="text-sm text-light-text/60 dark:text-dark-text/60 hover:text-neon-purple transition-colors"
            >
              Terms
            </a>
            <a
              href="#"
              className="text-sm text-light-text/60 dark:text-dark-text/60 hover:text-neon-purple transition-colors"
            >
              Contact
            </a>
          </div>
        </div>

        {/* Copyright */}
        <div className="text-center text-sm text-light-text/50 dark:text-dark-text/50 border-t border-light-border dark:border-dark-border/30 pt-8">
          <p>© 2024 NameTag. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
