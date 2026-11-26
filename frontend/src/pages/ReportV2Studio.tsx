import { useCallback, useEffect, useMemo, useState } from "react";
import { downloadReportV2Pdf, generateReportV2Interview, generateReportV2Page, getOCandidates, getReportV2Meta, getReportV2Plan, type ReportV2Page } from "../api/client";
import { InterviewCard, type SubmittedInterviewAnswer } from "../components/InterviewCard";
import { CandidateSelector } from "../components/CandidateSelector";
import { ReportPageCards } from "../components/ResultDisplays/ReportPageCards";
import { SectionAResult } from "../components/ResultDisplays/SectionAResult";
import { SectionBResult } from "../components/ResultDisplays/SectionBResult";
import { SectionCResult } from "../components/ResultDisplays/SectionCResult";
import { SectionDEResult } from "../components/ResultDisplays/SectionDEResult";
import { PdfPreviewSidebar } from "../components/PdfPreviewSidebar";
import { PdfVariableSidebar } from "../components/PdfVariableSidebar";
import { buildSectionOHtml } from "../utils/htmlBuilder";
import { useBrandStore, type BrandInfo, type ReportV2Workspace } from "../store/brandStore";

export type StudioSection = "brand" | "business" | "customers" | "market" | "identity" | "review";
type Question = { question_id: number; question_text: string; options: string[] };
type Interview = { required_question_count: number; reasoning: string; questions: Question[] };
type Meta = {
  page_order: string[];
  page_specs: Record<string, { title: string; deps: string[]; conditional?: boolean }>;
  interviews: Record<string, { title: string; purpose: string }>;
  required_interviews_by_page?: Record<string, string[]>;
};
type StudioState = ReportV2Workspace;
const PAGE_GROUPS: Record<StudioSection, string[]> = {
  brand: ["00", "02", "03", "04"],
  business: ["05", "06"],
  customers: ["07", "08", "09", "10", "18"],
  market: ["11", "12", "13", "14", "15", "16", "17", "23", "24"],
  identity: ["19", "20", "21", "22"],
  review: ["01"],
};
const INTERVIEW_GROUPS: Record<StudioSection, string[]> = {
  brand: ["brand"], business: ["business"], customers: ["customer"], market: ["market"], identity: ["visual", "logo_character"], review: [],
};
const SECTION_HEADINGS: Record<StudioSection, { title: string; description: string }> = {
  brand: { title: "브랜드 기초", description: "브랜드 정보를 입력하고 표지, 브랜드 본질, 정체성, 스토리 내용을 작성합니다." },
  business: { title: "사업 개요와 포지셔닝", description: "사업 현황과 시장에서 차지할 자리를 정리합니다." },
  customers: { title: "고객 전략과 가치 제안", description: "페르소나, 고객 비교, 가치 적합도, 고객 여정을 확인합니다. 페르소나는 AI 분석 가설로 표시됩니다." },
  market: { title: "시장 분석과 사업 모델", description: "시장·경쟁 분석, 시장 규모, SWOT/TOWS, 사업 모델과 검증 계획을 정리합니다." },
  identity: { title: "시각 정체성과 브랜드 적용", description: "컬러, 타이포그래피, 로고, 캐릭터, 브랜드 적용안을 정리합니다." },
  review: { title: "보고서 검토와 PDF", description: "작성한 내용을 검토하고 PDF 변수를 조정한 뒤 보고서를 내려받습니다." },
};

function pagesInvalidatedByRoots(
  roots: string[],
  pageSpecs: Meta["page_specs"] | undefined,
): Set<string> {
  const invalidated = new Set(roots);
  if (!pageSpecs) return invalidated;
  let changed = true;
  while (changed) {
    changed = false;
    for (const [pageId, spec] of Object.entries(pageSpecs)) {
      if (!invalidated.has(pageId) && spec.deps.some((dependency) => invalidated.has(dependency))) {
        invalidated.add(pageId);
        changed = true;
      }
    }
  }
  return invalidated;
}

export function ReportV2Studio({ section = "brand" }: { section?: StudioSection }) {
  const state = useBrandStore((store) => store.reportV2);
  const setState = useBrandStore((store) => store.updateReportV2);
  const [brandDraft, setBrandDraft] = useState(state.brand);
  const [meta, setMeta] = useState<Meta | null>(null);
  const [plan, setPlan] = useState<{ ready_page_ids: string[]; ready_interview_ids: string[] }>({ ready_page_ids: [], ready_interview_ids: [] });
  const [selectedInterviewId, setSelectedInterviewId] = useState("");
  const [currentInterview, setCurrentInterview] = useState<Interview | null>(null);
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");

  useEffect(() => { setBrandDraft(state.brand); }, [state.brand]);

  const context = useMemo(() => ({
    brand: { ...state.brand, ...(state.selectedBrandInfo || {}), vibes: state.brand.vibes.split(",").map((item) => item.trim()).filter(Boolean) },
    pages: state.pages,
    interview_answers: state.answers,
  }), [state]);

  const refreshPlan = useCallback(async (snapshot: StudioState = state) => {
    try {
      const next = await getReportV2Plan({
        context: {
          brand: { ...snapshot.brand, ...(snapshot.selectedBrandInfo || {}), vibes: snapshot.brand.vibes.split(",").map((item) => item.trim()).filter(Boolean) },
          pages: snapshot.pages,
          interview_answers: snapshot.answers,
        },
        skipped_page_ids: Object.entries(snapshot.conditional).filter(([, enabled]) => !enabled).map(([id]) => id),
        conditional_decisions: snapshot.conditional,
      });
      setPlan(next as typeof plan);
    } catch (reason) { setError(reason instanceof Error ? reason.message : "진행 상태를 불러오지 못했습니다."); }
  }, [state]);

  useEffect(() => { void refreshPlan(state); }, [state, refreshPlan]);
  useEffect(() => {
    getReportV2Meta().then(setMeta).catch((reason: unknown) => setError(reason instanceof Error ? reason.message : "보고서 정보를 불러오지 못했습니다."));
  }, []);

  const hasUnappliedBrandChanges = JSON.stringify(brandDraft) !== JSON.stringify(state.brand);
  const applyBrandChanges = () => {
    if (!hasUnappliedBrandChanges) return;
    setState((previous) => ({
      ...previous,
      brand: brandDraft,
      selectedBrandInfo: null,
      brandCandidates: [],
      pages: {},
      interviews: {},
      answers: {},
    }));
    setCurrentInterview(null);
    setError("");
  };

  const generateBrandCandidates = async () => {
    const answers = state.answers.brand || [];
    if (!answers.length) return;
    setBusy("brand-candidates"); setError("");
    try {
      const interviewText = answers.map((answer) => `${answer.question_id}. ${answer.question_text}\n선택: ${answer.selected_option}\n직접 입력: ${answer.user_input}`).join("\n\n");
      const result = await getOCandidates({
        business_type: state.brand.business_type,
        vibes: state.brand.vibes.split(",").map((item) => item.trim()).filter(Boolean),
        target: state.brand.target,
        keywords: state.brand.keywords,
      }, interviewText) as { candidates?: unknown } | unknown[];
      const rawCandidates = Array.isArray(result) ? result : (result as { candidates?: unknown[] })?.candidates;
      if (!Array.isArray(rawCandidates) || rawCandidates.length !== 4) {
        throw new Error("브랜드 후보 4개를 받지 못했습니다. 인터뷰 답변을 확인한 뒤 다시 생성해 주세요.");
      }
      const requiredFields: Array<keyof BrandInfo> = ["brand_name", "brand_name_en", "name_meaning", "slogan", "story_summary", "seed_color", "seed_color_reason"];
      const candidates = rawCandidates.map((candidate, index) => {
        if (!candidate || typeof candidate !== "object") throw new Error("후보 데이터 형식이 올바르지 않습니다.");
        const item = candidate as Record<string, unknown>;
        if (requiredFields.some((field) => typeof item[field] !== "string" || !String(item[field]).trim())) {
          throw new Error("브랜드 후보에 필수 항목이 빠져 있습니다. 다시 생성해 주세요.");
        }
        return { ...item, id: Number(item.id) || index + 1 } as BrandInfo & { id: number };
      });
      setState((previous) => ({ ...previous, brandCandidates: candidates, selectedBrandInfo: null }));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "브랜드 후보 생성에 실패했습니다.");
    } finally { setBusy(""); }
  };

  const selectBrandCandidate = useCallback((candidate: Record<string, string>) => {
    const selected = candidate as unknown as BrandInfo;
    setState((previous) => ({
      ...previous,
      brand: { ...previous.brand, brand_name: selected.brand_name },
      selectedBrandInfo: selected,
      pages: {},
    }));
  }, [setState]);

  const availableInterviewIds = (plan.ready_interview_ids || []).filter((id) => INTERVIEW_GROUPS[section].includes(id));
  useEffect(() => {
    if (availableInterviewIds.includes(selectedInterviewId)) return;
    setSelectedInterviewId(availableInterviewIds[0] || "");
  }, [section, plan.ready_interview_ids.join("|"), selectedInterviewId]);
  const createInterview = async () => {
    if (!selectedInterviewId) return;
    setBusy(`interview:${selectedInterviewId}`); setError("");
    try {
      const result = await generateReportV2Interview(selectedInterviewId, context) as Interview;
      setCurrentInterview(result);
      setState((previous) => ({ ...previous, interviews: { ...previous.interviews, [selectedInterviewId]: result } }));
    } catch (reason) { setError(reason instanceof Error ? reason.message : "인터뷰 생성에 실패했습니다."); }
    finally { setBusy(""); }
  };

  const saveInterviewAnswers = (submitted: SubmittedInterviewAnswer[]) => {
    if (!selectedInterviewId) return;
    setState((previous) => {
      const changed = JSON.stringify(previous.answers[selectedInterviewId] || []) !== JSON.stringify(submitted);
      if (!changed) return { ...previous, answers: { ...previous.answers, [selectedInterviewId]: submitted } };
      const roots = Object.entries(meta?.required_interviews_by_page || {})
        .filter(([, interviewIds]) => interviewIds.includes(selectedInterviewId))
        .map(([pageId]) => pageId);
      const invalidated = pagesInvalidatedByRoots(roots, meta?.page_specs);
      const pages = { ...previous.pages };
      for (const pageId of invalidated) delete pages[pageId];
      return { ...previous, answers: { ...previous.answers, [selectedInterviewId]: submitted }, pages };
    });
    setCurrentInterview(null);
  };

  const createPage = async (pageId: string, regenerate = false) => {
    setBusy(`page:${pageId}`); setError("");
    try {
      const result = await generateReportV2Page(pageId, { context, regenerate, conditional_decisions: state.conditional }) as { page: ReportV2Page; invalidated_page_ids: string[] };
      setState((previous) => {
        const pages = { ...previous.pages };
        for (const invalidatedId of result.invalidated_page_ids || []) delete pages[invalidatedId];
        if (result.page?.page_id) pages[result.page.page_id] = result.page;
        return { ...previous, pages };
      });
    } catch (reason) { setError(reason instanceof Error ? reason.message : "페이지 생성에 실패했습니다."); }
    finally { setBusy(""); }
  };

  const updatePage = (pageId: string, data: Record<string, unknown>) => setState((previous) => previous.pages[pageId]
    ? { ...previous, pages: { ...previous.pages, [pageId]: { ...previous.pages[pageId], data } } }
    : previous);

  const exportPdf = async () => {
    setBusy("pdf"); setError("");
    try { await downloadReportV2Pdf(state.pages, state.brand.brand_name || "NAME TAG"); }
    catch (reason) { setError(reason instanceof Error ? reason.message : "PDF 생성에 실패했습니다."); }
    finally { setBusy(""); }
  };

  const inputClass = "w-full rounded-xl border border-light-border bg-white px-4 py-3 text-light-text dark:border-dark-border dark:bg-dark-bg dark:text-dark-text";
  const activePageIds = section === "review" ? (meta?.page_order || Object.keys(state.pages)).filter((id) => state.pages[id]) : PAGE_GROUPS[section];
  const readyPageIds = (plan.ready_page_ids || []).filter((id) => PAGE_GROUPS[section].includes(id));
  const savedInterviewIds = INTERVIEW_GROUPS[section].filter((id) => state.answers[id]?.length);
  const savedPageCount = Object.keys(state.pages).length;
  const savedAnswerCount = Object.keys(state.answers).filter((id) => state.answers[id]?.length).length;
  const recommendedPageId = readyPageIds[0];

  const renderResults = () => {
    const props = { pages: state.pages, busy: Boolean(busy) || hasUnappliedBrandChanges, onRegenerate: (id: string) => void createPage(id, true) };
    if (section === "business") return <SectionAResult {...props} />;
    if (section === "customers") return <SectionBResult {...props} />;
    if (section === "market") return <SectionCResult {...props} />;
    if (section === "identity") return <SectionDEResult {...props} />;
    return <ReportPageCards {...props} pageIds={activePageIds} />;
  };

  return <div className="space-y-6">
    <header className="space-y-2">
      <p className="text-xs font-bold uppercase tracking-[0.25em] text-neon-purple">NAME TAG · 브랜드 전략 보고서</p>
      <h1 className="text-3xl font-black md:text-4xl">{SECTION_HEADINGS[section].title}</h1>
      <p className="text-sm leading-6 text-light-text/70 dark:text-dark-text/70">{SECTION_HEADINGS[section].description} 단계 이동 중에는 작성 내용이 유지되며, 새로고침하면 초기화됩니다.</p>
      <div className="flex flex-wrap gap-2 pt-1 text-xs">
        <span className="rounded-full border border-light-border bg-white px-3 py-1.5 dark:border-dark-border dark:bg-dark-bg2">보고서 {savedPageCount}페이지 작성</span>
        <span className="rounded-full border border-light-border bg-white px-3 py-1.5 dark:border-dark-border dark:bg-dark-bg2">인터뷰 {savedAnswerCount}개 저장</span>
      </div>
    </header>
    {error && <div role="alert" className="rounded-xl border border-red-300 bg-red-50 p-4 text-sm text-red-800">{error}</div>}

    {section === "brand" && <section className="floating-card space-y-4 p-5">
      <h2 className="text-xl font-bold">브랜드 입력</h2>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="space-y-1 text-sm">브랜드명<input className={inputClass} value={brandDraft.brand_name} onChange={(e) => setBrandDraft((previous) => ({ ...previous, brand_name: e.target.value }))} /></label>
        <label className="space-y-1 text-sm">업종·서비스<input className={inputClass} value={brandDraft.business_type} onChange={(e) => setBrandDraft((previous) => ({ ...previous, business_type: e.target.value }))} /></label>
        <label className="space-y-1 text-sm">타겟 고객<input className={inputClass} value={brandDraft.target} onChange={(e) => setBrandDraft((previous) => ({ ...previous, target: e.target.value }))} /></label>
        <label className="space-y-1 text-sm">브랜드 분위기 (쉼표로 구분)<input className={inputClass} value={brandDraft.vibes} onChange={(e) => setBrandDraft((previous) => ({ ...previous, vibes: e.target.value }))} /></label>
        <label className="space-y-1 text-sm md:col-span-2">키워드<input className={inputClass} value={brandDraft.keywords} onChange={(e) => setBrandDraft((previous) => ({ ...previous, keywords: e.target.value }))} /></label>
      </div>
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-stone-200 bg-stone-50 p-3 dark:border-dark-border dark:bg-dark-bg">
        <p className="text-xs leading-5 text-stone-600 dark:text-dark-text/70">{hasUnappliedBrandChanges
          ? Object.keys(state.pages).length || Object.keys(state.answers).length
            ? "변경사항을 적용하면 기존 보고서 페이지와 인터뷰 답변이 초기화됩니다."
            : "변경사항을 적용해야 인터뷰와 보고서 생성에 사용됩니다."
          : "입력 내용을 바꾸면 적용 버튼이 나타납니다."}</p>
        <button type="button" className="btn-secondary shrink-0 px-4 py-2 text-sm" disabled={!hasUnappliedBrandChanges || Boolean(busy)} onClick={applyBrandChanges}>
          {Object.keys(state.pages).length || Object.keys(state.answers).length ? "변경 적용 후 다시 시작" : "입력 변경사항 적용"}
        </button>
      </div>
      <div className="grid gap-3 sm:grid-cols-2">{["17", "21"].map((pageId) => <label key={pageId} className="flex items-center gap-3 rounded-xl bg-black/5 p-3 text-sm dark:bg-white/5"><input type="checkbox" checked={state.conditional[pageId]} onChange={(e) => setState((previous) => {
        const pages = { ...previous.pages };
        for (const invalidatedId of pagesInvalidatedByRoots([pageId], meta?.page_specs)) delete pages[invalidatedId];
        return { ...previous, conditional: { ...previous.conditional, [pageId]: e.target.checked }, pages };
      })} />{pageId === "17" ? "Lean Canvas 페이지 포함" : "Character Identity 페이지 포함"}</label>)}</div>
      <div className="space-y-2"><h3 className="text-sm font-semibold">브랜드 입력 미리보기</h3><iframe title="브랜드 입력 미리보기" sandbox="" srcDoc={buildSectionOHtml(brandDraft)} className="h-64 w-full rounded-xl border border-stone-200 bg-white" /></div>
      <div className="space-y-3 border-t border-stone-200 pt-4">
        <div><h3 className="font-semibold">브랜드 후보 조합</h3><p className="mt-1 text-sm text-stone-500">초기 인터뷰 답변으로 후보 4개를 만들고 이름·의미·슬로건·스토리·컬러를 조합해 선택합니다.</p></div>
        <button type="button" className="btn-secondary px-4 py-2" disabled={!state.answers.brand?.length || hasUnappliedBrandChanges || Boolean(busy)} onClick={() => void generateBrandCandidates()}>{busy === "brand-candidates" ? "후보 생성 중…" : "인터뷰 답변으로 브랜드 후보 만들기"}</button>
        {hasUnappliedBrandChanges && <p className="text-xs text-amber-700 dark:text-amber-300">입력 변경사항을 먼저 적용해 주세요.</p>}
        {state.brandCandidates.length > 0 && <CandidateSelector candidates={state.brandCandidates} onComplete={selectBrandCandidate} />}
        {state.selectedBrandInfo && <p className="text-sm text-emerald-700">선택된 브랜드: {state.selectedBrandInfo.brand_name}</p>}
      </div>
    </section>}

    {section !== "review" && <section className="floating-card space-y-4 p-5">
      <div className="flex flex-wrap items-center justify-between gap-3"><div><h2 className="text-xl font-bold">단계 인터뷰</h2><p className="text-sm opacity-70">질문마다 선택지 4개, 자유 입력 답변을 지원합니다.</p></div>
        <div className="flex gap-2"><select className={inputClass + " min-w-52"} value={selectedInterviewId} onChange={(e) => setSelectedInterviewId(e.target.value)}><option value="">이번 단계의 인터뷰 선택</option>{availableInterviewIds.map((id) => <option key={id} value={id}>{meta?.interviews[id]?.title || id}</option>)}</select>
          <button className="btn-primary px-4 py-2" disabled={!selectedInterviewId || Boolean(busy)} onClick={() => void createInterview()}>{busy.startsWith("interview") ? "생성 중…" : "질문 생성"}</button></div>
      </div>
      {availableInterviewIds.length === 0 && <p className="rounded-xl bg-stone-50 p-3 text-sm leading-6 text-stone-600 dark:bg-dark-bg">앞 단계의 보고서 페이지와 인터뷰 답변이 준비되면 이 단계 질문을 만들 수 있습니다. 위 진행 단계에서 필요한 내용을 먼저 완료해 주세요.</p>}
      {currentInterview && <InterviewCard key={selectedInterviewId + currentInterview.questions.length} questions={currentInterview.questions} reasoning={currentInterview.reasoning} onComplete={() => undefined} onSubmitAnswers={saveInterviewAnswers} />}
      {savedInterviewIds.length > 0 && <p role="status" className="text-sm text-emerald-700 dark:text-emerald-300">저장된 답변: {savedInterviewIds.map((id) => meta?.interviews[id]?.title || id).join(", ")}</p>}
    </section>}

    <section className="floating-card space-y-4 p-5">
      <div className="flex flex-wrap items-center justify-between gap-3"><div><h2 className="text-xl font-bold">{section === "review" ? "보고서 페이지 검토" : "이 단계 보고서"}</h2><p className="text-sm opacity-70">작성된 페이지 {savedPageCount}개 · 인터뷰 답변 {savedAnswerCount}개</p></div>
        {section === "review" && <button type="button" className="btn-primary px-4 py-2" disabled={!savedPageCount || Boolean(busy) || hasUnappliedBrandChanges} aria-busy={busy === "pdf"} onClick={() => void exportPdf()}>{busy === "pdf" ? "PDF 생성 중…" : "PDF 다운로드"}</button>}
      </div>
      {hasUnappliedBrandChanges && <p role="status" className="rounded-xl border border-amber-300 bg-amber-50 p-3 text-sm leading-6 text-amber-900">브랜드 입력에 적용되지 않은 변경사항이 있습니다. 생성 전에 위의 변경사항 적용 버튼을 눌러 주세요.</p>}
      {recommendedPageId && !hasUnappliedBrandChanges && <div className="flex flex-wrap items-center gap-3 rounded-xl border border-neon-purple/20 bg-neon-purple/5 p-3 dark:border-neon-cyan/20 dark:bg-neon-cyan/5">
        <button type="button" className="btn-primary px-4 py-2 text-sm" disabled={Boolean(busy)} aria-busy={busy === `page:${recommendedPageId}`} onClick={() => void createPage(recommendedPageId)}>{busy === `page:${recommendedPageId}` ? "페이지 생성 중…" : `다음 추천: ${recommendedPageId} ${meta?.page_specs[recommendedPageId]?.title || "페이지 생성"}`}</button>
        <span className="text-xs text-light-text/70 dark:text-dark-text/70">선행 단계가 준비된 페이지입니다.</span>
      </div>}
      {readyPageIds.length > 1 && !hasUnappliedBrandChanges && <details className="rounded-xl border border-light-border p-3 dark:border-dark-border">
        <summary className="cursor-pointer text-sm font-semibold">다른 준비된 페이지 {readyPageIds.length - 1}개</summary>
        <div className="mt-3 flex flex-wrap gap-2">{readyPageIds.filter((pageId) => pageId !== recommendedPageId).map((pageId) => <button type="button" key={pageId} className="btn-secondary px-3 py-2 text-sm" disabled={Boolean(busy)} onClick={() => void createPage(pageId)}>{busy === `page:${pageId}` ? "생성 중…" : `${pageId} ${meta?.page_specs[pageId]?.title || "페이지 생성"}`}</button>)}</div>
      </details>}
      {!readyPageIds.length && !hasUnappliedBrandChanges && <p className="rounded-xl border border-dashed border-light-border p-4 text-sm leading-6 text-light-text/70 dark:border-dark-border dark:text-dark-text/70">현재 단계에서 바로 생성할 페이지가 없습니다. 위 단계에서 필요한 보고서와 인터뷰를 완료하면 다음 페이지가 열립니다.</p>}
      {renderResults()}
    </section>

    {section === "review" && <div className="grid gap-6 xl:grid-cols-2"><PdfVariableSidebar pages={state.pages} busy={Boolean(busy) || hasUnappliedBrandChanges} onChange={updatePage} /><PdfPreviewSidebar brand={state.brand} pages={state.pages} /></div>}
  </div>;
}
