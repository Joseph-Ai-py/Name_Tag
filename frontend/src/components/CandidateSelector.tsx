import { useEffect, useState } from "react";

type Candidate = {
  id: number;
  brand_name: string;
  brand_name_en: string;
  name_meaning: string;
  slogan: string;
  story_summary: string;
  seed_color: string;
  seed_color_reason: string;
};

type Props = {
  candidates: Candidate[];
  onComplete: (brandInfo: Record<string, string>) => void;
};

const labels = ["브랜드명", "의미", "슬로건", "스토리", "컬러"] as const;

export function CandidateSelector({ candidates, onComplete }: Props) {
  const [selected, setSelected] = useState<Record<string, number | null>>({
    name: null,
    meaning: null,
    slogan: null,
    story: null,
    color: null,
  });

  useEffect(() => {
    if (candidates.length !== 4) return;
    const { name, meaning, slogan, story, color } = selected;
    if ([name, meaning, slogan, story, color].every((value) => value !== null)) {
      onComplete({
        brand_name: candidates[name!].brand_name,
        brand_name_en: candidates[name!].brand_name_en,
        name_meaning: candidates[meaning!].name_meaning,
        slogan: candidates[slogan!].slogan,
        story_summary: candidates[story!].story_summary,
        seed_color: candidates[color!].seed_color,
        seed_color_reason: candidates[color!].seed_color_reason,
      });
    }
  }, [candidates, onComplete, selected]);

  if (!candidates.length) {
    return null;
  }

  const panels = [
    {
      key: "name",
      title: labels[0],
      render: (candidate: Candidate) => `${candidate.brand_name} (${candidate.brand_name_en})`,
    },
    { key: "meaning", title: labels[1], render: (candidate: Candidate) => candidate.name_meaning },
    { key: "slogan", title: labels[2], render: (candidate: Candidate) => candidate.slogan },
    { key: "story", title: labels[3], render: (candidate: Candidate) => candidate.story_summary },
    {
      key: "color",
      title: labels[4],
      render: (candidate: Candidate) => `${candidate.seed_color} · ${candidate.seed_color_reason}`,
    },
  ] as const;

  return (
    <div className="space-y-5 rounded-3xl border border-stone-200 bg-white p-6 shadow-[0_24px_70px_rgba(15,23,42,0.06)] md:p-8">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.35em] text-stone-500">Candidate Mix & Match</p>
        <h3 className="mt-2 text-2xl font-black text-stone-900">브랜드 후보를 조합해 확정하세요</h3>
      </div>

      <div className="grid gap-4 xl:grid-cols-2">
        {panels.map((panel) => (
          <div key={panel.key} className="rounded-3xl border border-stone-200 bg-stone-50 p-4">
            <div className="mb-3 flex items-center justify-between">
              <p className="text-sm font-semibold text-stone-700">{panel.title}</p>
              <p className="text-xs text-stone-400">독립 선택</p>
            </div>
            <div className="space-y-2">
              {candidates.map((candidate, index) => {
                const active = selected[panel.key] === index;
                const display = panel.render(candidate);
                return (
                  <button
                    key={`${panel.key}-${candidate.id}`}
                    type="button"
                    onClick={() => setSelected((value) => ({ ...value, [panel.key]: index }))}
                    className={`w-full rounded-2xl border px-4 py-3 text-left text-sm leading-6 transition ${
                      active
                        ? "border-amber-500 bg-amber-50 text-amber-900 shadow-sm"
                        : "border-stone-200 bg-white text-stone-700 hover:border-amber-300 hover:bg-amber-50/40"
                    }`}
                  >
                    {panel.key === "color" ? (
                      <div className="flex items-center gap-3">
                        <span className="h-8 w-8 rounded-full border border-stone-200" style={{ backgroundColor: candidate.seed_color }} />
                        <span>{display}</span>
                      </div>
                    ) : (
                      display
                    )}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
