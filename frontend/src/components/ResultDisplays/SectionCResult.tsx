import { RefreshCw } from "lucide-react";

interface SectionCResultProps {
  data: any;
  onRegenerate: (key: string, label: string) => void;
}

export function SectionCResult({ data, onRegenerate }: SectionCResultProps) {
  if (!data) return null;

  const colorFields = [
    { key: "primary_color", label: "주요색", icon: "🎨" },
    { key: "secondary_color", label: "보조색", icon: "🖌️" },
    { key: "accent_color", label: "강조색", icon: "✨" },
  ];

  const typographyFields = [
    { key: "primary_font", label: "주요 폰트", icon: "🔤" },
    { key: "secondary_font", label: "보조 폰트", icon: "📝" },
  ];

  const styleFields = [
    { key: "photography_style", label: "사진 스타일", icon: "📸" },
    { key: "illustration_style", label: "일러스트 스타일", icon: "🎭" },
    { key: "graphic_elements", label: "그래픽 요소", icon: "🎪" },
  ];

  return (
    <div className="space-y-6">
      {/* 컬러 팔레트 */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-stone-900">🎨 컬러 팔레트</h4>
        <div className="grid gap-3 md:grid-cols-3">
          {colorFields.map(({ key, label, icon }) => (
            data[key] && (
              <div key={key} className="rounded-xl border border-stone-200 overflow-hidden transition hover:shadow-md">
                <div className="h-16 bg-gradient-to-br from-stone-100 to-stone-200 flex items-center justify-center text-xs font-semibold">
                  {data[key]}
                </div>
                <div className="bg-white p-3">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-xs font-semibold text-stone-600">
                      <span className="mr-1">{icon}</span>
                      {label}
                    </p>
                    <button
                      type="button"
                      onClick={() => onRegenerate(key, label)}
                      className="rounded-full p-1 transition hover:bg-amber-100"
                    >
                      <RefreshCw size={12} className="text-amber-600" />
                    </button>
                  </div>
                  <p className="text-xs text-stone-600">{data[key]}</p>
                </div>
              </div>
            )
          ))}
        </div>
      </div>

      {/* 타이포그래피 */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-stone-900">🔤 타이포그래피</h4>
        <div className="grid gap-3 md:grid-cols-2">
          {typographyFields.map(({ key, label, icon }) => (
            data[key] && (
              <div key={key} className="rounded-xl border border-stone-200 bg-white p-4">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm font-semibold text-stone-700">
                    <span className="mr-1">{icon}</span>
                    {label}
                  </p>
                  <button
                    type="button"
                    onClick={() => onRegenerate(key, label)}
                    className="rounded-full p-1 transition hover:bg-amber-100"
                  >
                    <RefreshCw size={12} className="text-amber-600" />
                  </button>
                </div>
                <p className="text-xs text-stone-600">{data[key]}</p>
              </div>
            )
          ))}
        </div>
      </div>

      {/* 스타일 가이드 */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-stone-900">🎭 시각 스타일</h4>
        <div className="grid gap-3 md:grid-cols-3">
          {styleFields.map(({ key, label, icon }) => (
            data[key] && (
              <div key={key} className="rounded-xl border border-indigo-200 bg-indigo-50 p-3">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-xs font-semibold text-indigo-900">
                    <span className="mr-1">{icon}</span>
                    {label}
                  </p>
                  <button
                    type="button"
                    onClick={() => onRegenerate(key, label)}
                    className="rounded-full p-1 transition hover:bg-indigo-100"
                  >
                    <RefreshCw size={12} className="text-indigo-600" />
                  </button>
                </div>
                <p className="text-xs leading-relaxed text-indigo-900">{data[key]}</p>
              </div>
            )
          ))}
        </div>
      </div>
    </div>
  );
}
