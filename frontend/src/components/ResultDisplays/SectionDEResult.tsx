import { RefreshCw } from "lucide-react";

interface SectionDEResultProps {
  data: any;
  onRegenerate: (key: string, label: string) => void;
}

export function SectionDEResult({ data, onRegenerate }: SectionDEResultProps) {
  if (!data) return null;

  // 로고 섹션
  const logoData = data.logo_identity || {};
  const concept = logoData.concept || {};
  const guide = logoData.guide || {};

  // 캐릭터 섹션
  const charData = data.character_guide || {};
  const charIntro = charData.intro || {};
  const charReasoning = charData.reasoning || {};
  const charStory = charData.story || {};

  return (
    <div className="space-y-8">
      {/* 로고 정체성 */}
      <div className="rounded-2xl border-2 border-amber-200 bg-gradient-to-br from-amber-50 to-white p-6">
        <h3 className="mb-4 text-lg font-bold text-amber-900">
          🎨 로고 정체성 & 개념
        </h3>

        {/* 로고 이미지 미리보기 */}
        {data.logo_path && (
          <div className="mb-6 flex justify-center rounded-xl bg-white p-6 border border-amber-100">
            <img 
              src={`http://localhost:8000${data.logo_path}`} 
              alt="Logo" 
              className="max-h-64 max-w-64 object-contain"
            />
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-2">
          {concept.symbol_reason && (
            <div className="rounded-lg bg-white p-4 border border-amber-100">
              <p className="mb-2 text-sm font-semibold text-amber-900">💎 심볼 모티프</p>
              <p className="text-sm text-amber-800">{concept.symbol_reason}</p>
            </div>
          )}
          
          {concept.color_reason && (
            <div className="rounded-lg bg-white p-4 border border-amber-100">
              <p className="mb-2 text-sm font-semibold text-amber-900">🎨 색상 정체성</p>
              <p className="text-sm text-amber-800">{concept.color_reason}</p>
            </div>
          )}

          {concept.direction_text && (
            <div className="rounded-lg bg-white p-4 border border-amber-100 md:col-span-2">
              <p className="mb-2 text-sm font-semibold text-amber-900">📐 디자인 방향성</p>
              <p className="italic text-sm text-amber-800">"{concept.direction_text}"</p>
            </div>
          )}

          {concept.overall_message && (
            <div className="rounded-lg bg-white p-4 border border-amber-100 md:col-span-2">
              <p className="mb-2 text-sm font-semibold text-amber-900">💬 브랜드 메시지</p>
              <p className="text-sm leading-relaxed text-amber-800">{concept.overall_message}</p>
            </div>
          )}
        </div>

        {/* 로고 가이드 */}
        {Object.keys(guide).length > 0 && (
          <div className="mt-4 rounded-lg bg-amber-50 p-4 text-xs text-amber-900 border border-amber-200">
            <p className="font-semibold mb-2">📏 사용 가이드</p>
            <ul className="space-y-1">
              {guide.minimum_size && <li>• 최소 크기: {guide.minimum_size}</li>}
              {guide.clear_space && <li>• 여백: {guide.clear_space}</li>}
            </ul>
          </div>
        )}
      </div>

      {/* 캐릭터 페르소나 */}
      <div className="rounded-2xl border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-white p-6">
        <h3 className="mb-4 text-lg font-bold text-purple-900">
          🎭 캐릭터 페르소나
        </h3>

        {/* 캐릭터 이미지 미리보기 */}
        {data.char_path && (
          <div className="mb-6 flex justify-center rounded-xl bg-white p-6 border border-purple-100">
            <img 
              src={`http://localhost:8000${data.char_path}`} 
              alt="Character" 
              className="max-h-72 max-w-72 object-contain"
            />
          </div>
        )}

        {/* 페르소나 이름 */}
        {charIntro.name && (
          <div className="mb-4 rounded-lg bg-gradient-to-r from-purple-100 to-pink-100 p-4 text-center">
            <p className="text-xs font-semibold text-purple-600 mb-1">Persona Name</p>
            <p className="text-2xl font-bold text-purple-900">{charIntro.name}</p>
          </div>
        )}

        <div className="grid gap-4 md:grid-cols-2">
          {charIntro.appearance && (
            <div className="rounded-lg bg-white p-4 border border-purple-100">
              <p className="mb-2 text-sm font-semibold text-purple-900">👤 외형 특징</p>
              <p className="text-sm text-purple-800">{charIntro.appearance}</p>
            </div>
          )}

          {charIntro.symbolic_value && (
            <div className="rounded-lg bg-white p-4 border border-purple-100">
              <p className="mb-2 text-sm font-semibold text-purple-900">✨ 상징 가치</p>
              <p className="text-sm text-purple-800">{charIntro.symbolic_value}</p>
            </div>
          )}

          {charReasoning.selection_reason && (
            <div className="rounded-lg bg-white p-4 border border-purple-100">
              <p className="mb-2 text-sm font-semibold text-purple-900">🎯 선택 이유</p>
              <p className="text-sm text-purple-800">{charReasoning.selection_reason}</p>
            </div>
          )}

          {charReasoning.emotional_connection && (
            <div className="rounded-lg bg-white p-4 border border-purple-100">
              <p className="mb-2 text-sm font-semibold text-purple-900">💝 감정적 연결</p>
              <p className="text-sm text-purple-800">{charReasoning.emotional_connection}</p>
            </div>
          )}

          {charStory.background && (
            <div className="rounded-lg bg-white p-4 border border-purple-100 md:col-span-2">
              <p className="mb-2 text-sm font-semibold text-purple-900">📖 배경 스토리</p>
              <p className="text-sm leading-relaxed text-purple-800">{charStory.background}</p>
            </div>
          )}

          {charStory.brand_role && (
            <div className="rounded-lg bg-white p-4 border border-purple-100 md:col-span-2">
              <p className="mb-2 text-sm font-semibold text-purple-900">🌟 브랜드 내 역할</p>
              <p className="text-sm leading-relaxed text-purple-800">{charStory.brand_role}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
