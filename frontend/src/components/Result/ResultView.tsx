import React from "react";
import { useWizard } from "../../hooks/useWizard";

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
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          브랜드 네임 - 3가지 제안
        </h2>

        <div className="flex gap-3 mb-6">
          {brands.map((brand, idx) => (
            <button
              key={idx}
              onClick={() => setSelectedBrandIndex(idx)}
              className={`flex-1 px-4 py-3 rounded-lg font-semibold transition ${
                selectedBrandIndex === idx
                  ? "bg-blue-600 text-white ring-2 ring-blue-400"
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200"
              }`}
            >
              {brand.name}
            </button>
          ))}
        </div>

        <div className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-blue-200">
          <h3 className="text-3xl font-bold text-gray-900 mb-2">
            {selectedBrand.name}
          </h3>
          <p className="text-sm text-gray-700 mb-4">{selectedBrand.meaning}</p>
          <p className="text-gray-800 mb-4">{selectedBrand.story}</p>
          <p className="text-lg italic text-gray-700">
            "{selectedBrand.slogan}"
          </p>
        </div>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">추천 서체</h2>
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-600 mb-2">한글</p>
            <p className="text-xl font-bold text-gray-900">
              {typography.korean}
            </p>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-600 mb-2">English</p>
            <p className="text-xl font-bold text-gray-900">
              {typography.english}
            </p>
          </div>
        </div>
        <p className="mt-3 text-sm text-gray-700">{typography.reason}</p>
      </div>

      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">
          브랜드 캐릭터 컨셉
        </h2>
        <div className="p-6 bg-gray-50 rounded-lg border border-gray-200 space-y-3">
          <h3 className="text-2xl font-bold text-gray-900">
            {character.name}
          </h3>
          <p className="text-sm text-gray-700">{character.concept}</p>
          <p className="text-gray-800">
            <strong>성격:</strong> {character.personality}
          </p>
          <p className="text-gray-800">{character.visual}</p>
        </div>
      </div>

      <div className="flex gap-3">
        <button
          onClick={reset}
          className="flex-1 py-3 px-4 bg-gray-200 text-gray-900 font-semibold rounded-lg hover:bg-gray-300 transition"
        >
          ↺ 다시 시작하기
        </button>
        <button
          onClick={() => alert("PDF 다운로드는 곧 제공됩니다!")}
          className="flex-1 py-3 px-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition"
        >
          📄 PDF 저장하기
        </button>
      </div>
    </div>
  );
}
