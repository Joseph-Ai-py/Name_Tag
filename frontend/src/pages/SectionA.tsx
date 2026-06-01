import { useState } from "react";
import { ArrowLeft, ArrowRight, Sparkles } from "lucide-react";
import { generateSectionA, getAInterview, regenerateSectionAField } from "../api/client";
import { apiLogger } from "../api/client";
import { InterviewCard } from "../components/InterviewCard";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { PageFrame } from "../components/PageFrame";
import { SectionAResult } from "../components/ResultDisplays/SectionAResult";
import { useBrandStore } from "../store/brandStore";

export function SectionA() {
  const brandInfo = useBrandStore((state) => state.brandInfo);
  const interviewDataA = useBrandStore((state) => state.interviewDataA);
  const dataA = useBrandStore((state) => state.dataA);
  const setInterviewDataA = useBrandStore((state) => state.setInterviewDataA);
  const setDataA = useBrandStore((state) => state.setDataA);
  const setCurrentStep = useBrandStore((state) => state.setCurrentStep);
  const setIsLoading = useBrandStore((state) => state.setIsLoading);
  const setError = useBrandStore((state) => state.setError);
  const isLoading = useBrandStore((state) => state.isLoading);
  const error = useBrandStore((state) => state.error);

  const [questions, setQuestions] = useState<any[]>([]);
  const [reasoning, setReasoning] = useState("");
  const [regenCandidates, setRegenCandidates] = useState<any[]>([]);
  const [regenOpen, setRegenOpen] = useState(false);
  const [regenTarget, setRegenTarget] = useState<string | null>(null);

  if (!brandInfo) {
    return <PageFrame eyebrow="Section A" title="브랜드 정보가 필요합니다" description="먼저 Section O에서 브랜드 후보를 확정해야 합니다." />;
  }

  return (
    <PageFrame
      eyebrow="Section A"
      title="철학·스토리·포지셔닝 인터뷰"
      description="확정된 브랜드 조합을 바탕으로 브랜드 철학과 스토리, 포지셔닝을 확장합니다."
      footer={
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <button
            type="button"
            onClick={() => setCurrentStep(0)}
            className="inline-flex items-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            <ArrowLeft size={16} />
            이전 단계
          </button>
          <button
            type="button"
            onClick={() => setCurrentStep(2)}
            disabled={!dataA}
            className="inline-flex items-center justify-center gap-2 rounded-full bg-stone-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-stone-800 disabled:cursor-not-allowed disabled:bg-stone-300"
          >
            다음 단계
            <ArrowRight size={16} />
          </button>
        </div>
      }
    >
      <div className="space-y-5">
        <div className="flex flex-col gap-3 sm:flex-row">
          <button
            type="button"
            onClick={async () => {
              try {
                setError(null);
                setIsLoading(true);
                apiLogger.info("Section A: interview request", { brandName: brandInfo.brand_name });
                const response = await getAInterview(brandInfo);
                apiLogger.info("Section A: interview response", { questionCount: response.questions?.length ?? 0 });
                setReasoning(response.reasoning || "");
                setQuestions(response.questions || []);
              } catch (error) {
                setError(error instanceof Error ? error.message : "Section A 인터뷰 실패");
              } finally {
                setIsLoading(false);
              }
            }}
            className="inline-flex items-center justify-center gap-2 rounded-full bg-amber-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-amber-600"
          >
            <Sparkles size={16} />
            인터뷰 시작
          </button>

          <button
            type="button"
            onClick={async () => {
              try {
                setError(null);
                setIsLoading(true);
                apiLogger.info("Section A: generate request", {
                  brandName: brandInfo.brand_name,
                  interviewLength: interviewDataA.length,
                });
                const response = await generateSectionA(brandInfo, interviewDataA);
                apiLogger.info("Section A: generate response", { keys: Object.keys(response.data_a || {}) });
                setDataA(response.data_a || {});
              } catch (error) {
                setError(error instanceof Error ? error.message : "Section A 생성 실패");
              } finally {
                setIsLoading(false);
              }
            }}
            className="inline-flex items-center justify-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            생성 시작
          </button>
        </div>

        {isLoading && <LoadingSpinner label="A 섹션을 생성 중입니다..." />}
        {error && <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>}

        {questions.length > 0 && (
          <InterviewCard sectionKey="A" questions={questions} reasoning={reasoning} onComplete={setInterviewDataA} />
        )}

        {dataA && (
          <div className="rounded-3xl border border-stone-200 bg-stone-50 p-6 space-y-6">
            <div>
              <p className="font-semibold text-stone-900 mb-4">✨ 생성 결과</p>
              <SectionAResult
                data={dataA}
                onRegenerate={async (key, label) => {
                  try {
                    setError(null);
                    setIsLoading(true);
                    apiLogger.info(`Section A: re-generate ${key}`, { brandName: brandInfo.brand_name });
                    const context = { existing: dataA };
                    const resp = await regenerateSectionAField(brandInfo, context, key);
                    const c = resp.result?.candidates || [];
                    setRegenCandidates(Array.isArray(c) ? c.map((x: any) => ({ text: x.text || x })) : []);
                    setRegenTarget(key);
                    setRegenOpen(true);
                  } catch (err) {
                    setError(err instanceof Error ? err.message : "재생성 실패");
                  } finally {
                    setIsLoading(false);
                  }
                }}
              />
            </div>
            
            {regenOpen && (
              <div className="mt-6 rounded-xl border bg-white p-4">
                <div className="flex items-center justify-between mb-4">
                  <p className="font-medium">재생성된 후보 {regenTarget ? `- ${regenTarget}` : ""}</p>
                  <button
                    type="button"
                    onClick={async () => {
                      try {
                        setError(null);
                        setIsLoading(true);
                        apiLogger.info(`Section A: force re-generate ${regenTarget}`, { brandName: brandInfo.brand_name });
                        const context = { existing: dataA };
                        const resp = await regenerateSectionAField(brandInfo, context, String(regenTarget));
                        const c = resp.result?.candidates || [];
                        setRegenCandidates(Array.isArray(c) ? c.map((x: any) => ({ text: x.text || x })) : []);
                      } catch (err) {
                        setError(err instanceof Error ? err.message : "재생성 실패");
                      } finally {
                        setIsLoading(false);
                      }
                    }}
                    className="rounded-full border px-3 py-1 text-sm bg-amber-50 border-amber-200 hover:bg-amber-100"
                  >
                    새로 생성
                  </button>
                </div>
                <div className="mt-2 grid gap-2">
                  {regenCandidates.length ? regenCandidates.map((c: any) => (
                    <div key={c.text || String(c)} className="flex items-center justify-between gap-2 rounded-md border px-3 py-2 hover:bg-stone-50">
                      <div className="text-sm text-stone-700">
                        <div>{c.text || String(c)}</div>
                        {c.rationale ? <div className="text-xs text-stone-500">{c.rationale}</div> : null}
                      </div>
                      <button
                        type="button"
                        onClick={async () => {
                          try {
                            const mod = await import("../store/brandStore");
                            const store = mod.useBrandStore.getState();
                            const newBrand = { ...(brandInfo as any) } as any;
                            const newDataA = { ...(dataA as any) } as any;
                            const value = c.text || c;
                            if (regenTarget === "brand_name") {
                              newBrand.brand_name = value;
                              newDataA.brand_name = value;
                            } else if (regenTarget === "name_meaning") {
                              newBrand.name_meaning = value;
                              newDataA.name_meaning = value;
                            } else if (regenTarget === "slogan") {
                              newBrand.slogan = value;
                              newDataA.slogan = value;
                            } else if (regenTarget === "story_summary") {
                              newBrand.story_summary = value;
                              newDataA.story_summary = value;
                            }
                            setDataA(newDataA);
                            store.setBrandInfo(newBrand);
                            if (regenTarget) {
                              store.setAppliedSelection("A", regenTarget, value);
                            }
                            setRegenOpen(false);
                            setRegenCandidates([]);
                            setRegenTarget(null);
                          } catch (e) {}
                        }}
                        className="rounded-full bg-amber-500 px-3 py-1 text-sm text-white"
                      >
                        적용
                      </button>
                    </div>
                  )) : <div className="text-sm text-stone-500">후보가 없습니다.</div>}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </PageFrame>
  );
}
