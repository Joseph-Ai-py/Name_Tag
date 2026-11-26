import type { ReportV2Page } from "../../api/client";

const LABELS: Record<string, string> = {
  brand_name: "브랜드명", industry: "업종", business_type: "사업 유형", report_version: "보고서 버전", report_date: "작성일",
  key_sentence: "핵심 문장", brand_promise: "브랜드 약속", brand_thesis: "브랜드 핵심 주장", key_metrics: "핵심 지표",
  key_findings_3: "핵심 발견", key_strategies_3: "핵심 전략", priority_actions: "우선 실행 과제", why: "Why · 존재 이유",
  how: "How · 고유한 방식", what: "What · 제품·서비스", brand_essence: "브랜드 본질", identity_prism: "아이덴티티 프리즘",
  core_values: "핵심 가치", archetype: "브랜드 원형", personas: "고객 페르소나", customer_jobs: "고객 과업",
  pains: "고객 문제", gains: "고객 기대", pain_relievers: "문제 완화 요소", gain_creators: "가치 창출 요소",
  customer_segments: "고객 세그먼트", value_propositions: "가치 제안", channels: "채널", customer_relationships: "고객 관계",
  revenue_streams: "수익원", key_resources: "핵심 자원", key_activities: "핵심 활동", key_partners: "핵심 파트너", cost_structure: "비용 구조",
  source_ids: "근거 출처 ID", confidence: "신뢰도", evidence: "근거", validation_method: "검증 방법", status: "상태",
};

function label(key: string) {
  return LABELS[key] || key.replace(/_/g, " ").replace(/^./, (letter: string) => letter.toUpperCase());
}

function renderInlineEmphasis(value: string) {
  return value.split(/(\*\*[^*]+\*\*)/g).map((part, index) =>
    part.startsWith("**") && part.endsWith("**")
      ? <strong key={index} className="font-bold text-stone-900">{part.slice(2, -2)}</strong>
      : part,
  );
}

function DataValue({ value }: { value: unknown }) {
  if (value === null || value === undefined || value === "") return <span className="text-sm text-stone-400">아직 입력된 내용이 없습니다.</span>;
  if (typeof value === "boolean") return <span>{value ? "예" : "아니요"}</span>;
  if (Array.isArray(value)) {
    if (!value.length) return <span className="text-sm text-stone-400">항목 없음</span>;
    return <div className="grid gap-2 sm:grid-cols-2">{value.map((item, index) => <div key={index} className="rounded-xl bg-stone-50 p-3"><DataValue value={item} /></div>)}</div>;
  }
  if (typeof value === "object") {
    return <dl className="grid gap-3 sm:grid-cols-2">{Object.entries(value as Record<string, unknown>).map(([key, item]) => <div key={key} className="min-w-0"><dt className="mb-1 text-xs font-semibold uppercase tracking-wide text-stone-500">{label(key)}</dt><dd className="text-sm leading-6 text-stone-800"><DataValue value={item} /></dd></div>)}</dl>;
  }
  return <span className="whitespace-pre-wrap break-words">{renderInlineEmphasis(String(value))}</span>;
}

export function ReportPageCards({
  pages,
  pageIds,
  onRegenerate,
  busy = false,
}: {
  pages: Record<string, ReportV2Page>;
  pageIds: string[];
  onRegenerate: (pageId: string) => void;
  busy?: boolean;
}) {
  const visible = pageIds.filter((id) => pages[id]);
  if (!visible.length) return <p className="rounded-2xl border border-dashed border-stone-300 p-5 text-sm text-stone-500">이 단계에서 생성된 페이지가 아직 없습니다. 준비된 페이지를 생성하면 여기에 표시됩니다.</p>;
  return <div className="space-y-3">{visible.map((id) => {
    const page = pages[id];
    return <details key={id} className="rounded-2xl border border-stone-200 bg-white p-4 shadow-sm" open={visible.length === 1}>
      <summary className="flex cursor-pointer list-none flex-wrap items-center justify-between gap-2 font-semibold text-stone-900"><span>{id} · {page.title}</span><span className="text-xs font-medium text-stone-500">{page.status} · {page.evidence_type || "출처 유형 미기록"} · 신뢰도 {page.confidence || "미기록"}</span></summary>
      <div className="mt-4 space-y-4">
        <DataValue value={page.data} />
        {page.source_ids?.length ? <p className="border-t border-stone-100 pt-3 text-xs text-stone-500">출처 ID: {page.source_ids.join(", ")}</p> : null}
        {page.validation_notes?.length ? <ul className="list-disc space-y-1 pl-5 text-xs text-amber-800">{page.validation_notes.map((note, index) => <li key={index}>{note}</li>)}</ul> : null}
        <button type="button" className="btn-secondary px-3 py-2 text-sm" disabled={busy} onClick={() => onRegenerate(id)}>이 페이지 다시 생성</button>
      </div>
    </details>;
  })}</div>;
}
