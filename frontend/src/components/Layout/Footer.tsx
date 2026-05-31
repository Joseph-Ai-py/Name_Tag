export function Footer() {
  return (
    <footer className="mt-16 border-t border-light-border bg-light-bg py-12 dark:border-dark-border/50 dark:bg-dark-bg">
      <div className="mx-auto max-w-6xl px-4 md:px-6">
        <div className="mb-8 flex flex-col items-center justify-between gap-8 md:flex-row">
          <div className="text-center md:text-left">
            <div className="mb-2 text-2xl font-bold bg-gradient-neon bg-clip-text text-transparent">NameTag</div>
            <p className="text-sm text-light-text/70 dark:text-dark-text/70">AI로 만드는 브랜드 정체성</p>
          </div>

          <div className="flex gap-8 text-sm">
            <a href="#" className="text-light-text/60 transition hover:text-neon-purple dark:text-dark-text/60">Privacy</a>
            <a href="#" className="text-light-text/60 transition hover:text-neon-purple dark:text-dark-text/60">Terms</a>
            <a href="#" className="text-light-text/60 transition hover:text-neon-purple dark:text-dark-text/60">Contact</a>
          </div>
        </div>

        <div className="border-t border-light-border pt-8 text-center text-sm text-light-text/50 dark:border-dark-border/30 dark:text-dark-text/50">
          <p>© 2026 NameTag. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}