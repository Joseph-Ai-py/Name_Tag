import { RefreshCw } from "lucide-react";

interface SectionAResultProps {
  data: any;
  onRegenerate: (key: string, label: string) => void;
}

export function SectionAResult({ data, onRegenerate }: SectionAResultProps) {
  if (!data) return null;

  const fields = [
    { key: "brand_name", label: "브랜드명", icon: "🏢" },
    { key: "name_meaning", label: "이름 의미", icon: "✨" },
    { key: "slogan", label: "슬로건", icon: "💬" },
    { key: "story_summary", label: "스토리 요약", icon: "📖" },
  ];

  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-2">
        {fields.map(({ key, label, icon }) => (
          <div key={key} className="rounded-2xl border border-stone-200 bg-white p-4 transition hover:border-amber-200 hover:shadow-md">
            <div className="mb-2 flex items-center justify-between">
              <h4 className="text-sm font-semibold text-stone-600">
                <span className="mr-2">{icon}</span>
                {label}
              </h4>
              <button
                type="button"
                onClick={() => onRegenerate(key, label)}
                className="rounded-full p-1 transition hover:bg-amber-100"
                title="재생성"
              >
                <RefreshCw size={14} className="text-amber-600" />
              </button>
            </div>
            <p className="text-sm leading-relaxed text-stone-700">{data[key] || "—"}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
