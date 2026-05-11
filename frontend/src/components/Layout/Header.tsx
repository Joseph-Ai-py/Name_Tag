import React from "react";

export function Header() {
  return (
    <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200">
      <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="text-2xl">🏷️</div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">NameTag</h1>
            <p className="text-sm text-gray-600">패키지 A</p>
          </div>
        </div>
      </div>
    </header>
  );
}
