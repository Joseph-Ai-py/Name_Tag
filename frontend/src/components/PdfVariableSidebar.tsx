import { useState } from "react";
import { FileJson } from "lucide-react";
import type { ReportV2Page } from "../api/client";

export function PdfVariableSidebar({ pages, onChange, busy = false }: {
  pages: Record<string, ReportV2Page>;
  busy?: boolean;
  onChange: (pageId: string, data: Record<string, unknown>) => void;
}) {
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [errors, setErrors] = useState<Record<string, string>>({});
  const pageIds = Object.keys(pages).sort();
  return <aside className="space-y-4 rounded-3xl border border-stone-200 bg-white/90 p-5 shadow-sm">
    <div className="flex items-start gap-3"><div className="rounded-2xl bg-stone-100 p-3 text-stone-600"><FileJson size={20} /></div><div><h2 className="text-xl font-black text-stone-900">PDF 변수 편집</h2><p className="mt-2 text-sm leading-6 text-stone-600">페이지별 data 객체를 JSON으로 수정합니다. 유효한 객체만 미리보기와 PDF에 반영됩니다.</p></div></div>
    {!pageIds.length && <p className="rounded-2xl border border-dashed border-stone-300 p-4 text-sm text-stone-500">편집할 보고서 페이지가 없습니다.</p>}
    <div className="space-y-3">{pageIds.map((id) => {
      const page = pages[id];
      const value = drafts[id] ?? JSON.stringify(page.data, null, 2);
      const savedValue = JSON.stringify(page.data, null, 2);
      const hasChanges = value !== savedValue;
      return <details key={id} className="rounded-2xl border border-stone-200 p-4">
        <summary className="cursor-pointer font-semibold">{id} · {page.title}</summary>
        <textarea aria-label={`${id} PDF 데이터 JSON`} value={value} spellCheck={false} className="mt-3 min-h-48 w-full rounded-xl border border-stone-200 bg-stone-50 p-3 font-mono text-xs leading-5" onChange={(event) => {
          const next = event.target.value;
          setDrafts((previous) => ({ ...previous, [id]: next }));
          try {
            const parsed: unknown = JSON.parse(next);
            if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") throw new Error();
            setErrors((previous) => ({ ...previous, [id]: "" }));
          } catch {
            setErrors((previous) => ({ ...previous, [id]: "올바른 JSON 객체를 입력하세요." }));
          }
        }} />
        {errors[id] && <p className="mt-2 text-xs font-medium text-rose-600">{errors[id]}</p>}
        {!errors[id] && <p className="mt-2 text-xs text-stone-500">{hasChanges ? "적용 버튼을 눌러야 PDF 미리보기에 반영됩니다." : "JSON 수정 후 적용하면 오른쪽 미리보기가 갱신됩니다."}</p>}
        <button type="button" className="btn-secondary mt-3 px-3 py-2 text-sm" disabled={!hasChanges || Boolean(errors[id]) || busy} onClick={() => {
          try {
            const parsed: unknown = JSON.parse(value);
            if (!parsed || Array.isArray(parsed) || typeof parsed !== "object") throw new Error();
            onChange(id, parsed as Record<string, unknown>);
            setDrafts((previous) => { const next = { ...previous }; delete next[id]; return next; });
            setErrors((previous) => ({ ...previous, [id]: "" }));
          } catch {
            setErrors((previous) => ({ ...previous, [id]: "올바른 JSON 객체를 입력하세요." }));
          }
        }}>변경사항 적용</button>
      </details>;
    })}</div>
  </aside>;
}
