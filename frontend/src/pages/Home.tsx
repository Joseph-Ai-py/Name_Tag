import React from "react";
import { useNavigate } from "react-router-dom";

export function Home() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center px-4">
      <div className="max-w-2xl text-center space-y-8">
        <div className="space-y-4">
          <div className="text-6xl">🏷️</div>
          <h1 className="text-5xl font-bold text-gray-900">NameTag</h1>
          <p className="text-2xl text-gray-700">나만의 브랜드를 AI와 함께</p>
        </div>

        <p className="text-lg text-gray-600 max-w-xl mx-auto">
          브랜드 이름, 스토리, 서체, 캐릭터까지 AI가 한 번에 만들어줍니다.
          <br />
          당신의 비즈니스에 맞는 완벽한 브랜드 정체성을 발견해보세요.
        </p>

        <div className="space-y-4">
          <button
            onClick={() => navigate("/generate")}
            className="px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-lg font-semibold rounded-lg hover:shadow-lg transform hover:-translate-y-1 transition"
          >
            패키지 A 시작하기 →
          </button>
          <p className="text-sm text-gray-600">
            약 2분 소요 | 무료 이용 가능
          </p>
        </div>

        <div className="grid grid-cols-3 gap-4 mt-12 pt-8 border-t border-gray-200">
          <div>
            <div className="text-3xl mb-2">✨</div>
            <p className="font-semibold text-gray-900">브랜드 네이밍</p>
            <p className="text-sm text-gray-600">맞춤형 이름 3개</p>
          </div>
          <div>
            <div className="text-3xl mb-2">📖</div>
            <p className="font-semibold text-gray-900">스토리텔링</p>
            <p className="text-sm text-gray-600">감정 있는 설명</p>
          </div>
          <div>
            <div className="text-3xl mb-2">🎨</div>
            <p className="font-semibold text-gray-900">디자인 가이드</p>
            <p className="text-sm text-gray-600">서체 & 캐릭터</p>
          </div>
        </div>
      </div>
    </div>
  );
}
