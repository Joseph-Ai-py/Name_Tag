import { RefreshCw } from "lucide-react";

interface SectionBResultProps {
  data: any;
  onRegenerate: (key: string, label: string) => void;
}

export function SectionBResult({ data, onRegenerate }: SectionBResultProps) {
  if (!data) return null;

  // Section B의 일반적인 필드들
  const mainFields = [
    { key: "target_audience", label: "타겟 오디언스", icon: "👥" },
    { key: "key_characteristics", label: "핵심 특징", icon: "🎯" },
    { key: "primary_need", label: "주요 니즈", icon: "💡" },
    { key: "pain_points", label: "페인 포인트", icon: "⚠️" },
  ];

  const journeyFields = [
    { key: "awareness", label: "인지 단계", icon: "👀" },
    { key: "consideration", label: "검토 단계", icon: "🤔" },
    { key: "decision", label: "결정 단계", icon: "✅" },
    { key: "retention", label: "유지 단계", icon: "🤝" },
  ];

  return (
    <div className="space-y-6">
      {/* 타겟 오디언스 정보 */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-stone-900">👥 타겟 오디언스</h4>
        <div className="grid gap-3 md:grid-cols-2">
          {mainFields.map(({ key, label, icon }) => (
            data[key] && (
              <div key={key} className="rounded-xl border border-stone-200 bg-stone-50 p-3 transition hover:border-amber-200">
                <div className="mb-2 flex items-center justify-between">
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
                <p className="text-sm leading-relaxed text-stone-700">{data[key]}</p>
              </div>
            )
          ))}
        </div>
      </div>

      {/* 고객 여정 */}
      <div className="space-y-3">
        <h4 className="text-sm font-semibold text-stone-900">🛤️ 고객 여정 맵</h4>
        <div className="grid gap-3 md:grid-cols-4">
          {journeyFields.map(({ key, label, icon }) => (
            <div key={key} className="rounded-xl border border-amber-200 bg-amber-50/50 p-3">
              <p className="text-xs font-semibold text-amber-900">
                <span className="mr-1">{icon}</span>
                {label}
              </p>
              <p className="mt-2 text-xs leading-relaxed text-amber-800">{data[key] || "—"}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
