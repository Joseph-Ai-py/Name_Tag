import { useState } from "react";
import { ArrowLeft, ArrowRight, Sparkles } from "lucide-react";
import { generateSectionC, getCInterview } from "../api/client";
import { apiLogger } from "../api/client";
import { InterviewCard } from "../components/InterviewCard";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { PageFrame } from "../components/PageFrame";
import { useBrandStore } from "../store/brandStore";

export function SectionC() {
  const brandInfo = useBrandStore((state) => state.brandInfo);
  const interviewDataA = useBrandStore((state) => state.interviewDataA);
  const interviewDataB = useBrandStore((state) => state.interviewDataB);
  const interviewDataC = useBrandStore((state) => state.interviewDataC);
  const dataC = useBrandStore((state) => state.dataC);
  const setInterviewDataC = useBrandStore((state) => state.setInterviewDataC);
  const setDataC = useBrandStore((state) => state.setDataC);
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
    return <PageFrame eyebrow="Section C" title="브랜드 정보가 필요합니다" description="먼저 Section O에서 브랜드 후보를 확정해야 합니다." />;
  }

  return (
    <PageFrame
      eyebrow="Section C"
      title="비주얼 아이덴티티 인터뷰"
      description="레이아웃, 타이포, 무드의 방향을 정리해서 시각 가이드를 확정합니다."
      footer={
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <button
            type="button"
            onClick={() => setCurrentStep(2)}
            className="inline-flex items-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            <ArrowLeft size={16} />
            이전 단계
          </button>
          <button
            type="button"
            onClick={() => setCurrentStep(4)}
            disabled={!dataC}
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
                apiLogger.info("Section C: interview request", { brandName: brandInfo.brand_name });
                const response = await getCInterview(brandInfo);
                apiLogger.info("Section C: interview response", { questionCount: response.questions?.length ?? 0 });
                setReasoning(response.reasoning || "");
                setQuestions(response.questions || []);
              } catch (error) {
                setError(error instanceof Error ? error.message : "Section C 인터뷰 실패");
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
                apiLogger.info("Section C: generate request", {
                  brandName: brandInfo.brand_name,
                  interviewALength: interviewDataA.length,
                  interviewBLength: interviewDataB.length,
                  interviewCLength: interviewDataC.length,
                });
                const response = await generateSectionC(brandInfo, interviewDataA, interviewDataB, interviewDataC);
                apiLogger.info("Section C: generate response", { keys: Object.keys(response.data_c || {}) });
                setDataC(response.data_c || {});
              } catch (error) {
                setError(error instanceof Error ? error.message : "Section C 생성 실패");
              } finally {
                setIsLoading(false);
              }
            }}
            className="inline-flex items-center justify-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            생성 시작
          </button>
        </div>

        {isLoading && <LoadingSpinner label="C 섹션을 생성 중입니다..." />}
        {error && <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>}

        {questions.length > 0 && (
          <InterviewCard
            sectionKey="C"
            questions={questions}
            reasoning={reasoning}
            onComplete={(formattedText) => {
              apiLogger.info("Section C: interview text stored", { length: formattedText.length });
              setInterviewDataC(formattedText);
            }}
          />
        )}

        {dataC && (
          <div className="rounded-3xl border border-stone-200 bg-stone-50 p-5 text-sm leading-7 text-stone-700">
            <p className="font-semibold text-stone-900">생성 결과</p>
            <pre className="mt-3 overflow-x-auto whitespace-pre-wrap">{JSON.stringify(dataC, null, 2)}</pre>
            <div className="mt-4 flex gap-2">
              {["brand_name", "name_meaning", "slogan", "story_summary"].map((key) => (
                <button
                  key={key}
                  type="button"
                  onClick={async () => {
                    try {
                      setError(null);
                      setIsLoading(true);
                      apiLogger.info(`Section C: re-generate ${key}`, { brandName: brandInfo.brand_name });
                      const mod = await import("../store/brandStore");
                      const store = mod.useBrandStore.getState();
                      const applied = store.getAppliedSelection("C", key);
                      if (applied) {
                        setRegenCandidates([{ text: applied }]);
                        setRegenTarget(key);
                        setRegenOpen(true);
                        return;
                      }
                      const context = { existing: dataC };
                      const resp = await (await import("../api/client")).regenerateSectionCField(brandInfo, context, key);
                      const c = resp.result?.candidates || [];
                      setRegenCandidates(Array.isArray(c) ? c : []);
                      setRegenTarget(key);
                      setRegenOpen(true);
                    } catch (err) {
                      setError(err instanceof Error ? err.message : "재생성 실패");
                    } finally {
                      setIsLoading(false);
                    }
                  }}
                  className="rounded-full border border-stone-200 bg-white px-4 py-2 text-sm text-stone-800"
                >
                  재생성 ({key})
                </button>
              ))}
            </div>
            {regenOpen && (
              <div className="mt-4 rounded-xl border bg-white p-4">
                      <div className="flex items-center justify-between">
                        <p className="font-medium">재생성된 후보 {regenTarget ? `- ${regenTarget}` : ""}</p>
                        <button
                          type="button"
                          onClick={async () => {
                            try {
                              setError(null);
                              setIsLoading(true);
                              apiLogger.info(`Section C: force re-generate ${regenTarget}`, { brandName: brandInfo.brand_name });
                              const context = { existing: dataC };
                              const resp = await (await import("../api/client")).regenerateSectionCField(brandInfo, context, String(regenTarget));
                              const c = resp.result?.candidates || [];
                              setRegenCandidates(Array.isArray(c) ? c : []);
                            } catch (err) {
                              setError(err instanceof Error ? err.message : "재생성 실패");
                            } finally {
                              setIsLoading(false);
                            }
                          }}
                          className="rounded-full border px-3 py-1 text-sm bg-white"
                        >
                          새로 생성
                        </button>
                      </div>
                      <div className="mt-2 grid gap-2">
                  {regenCandidates.length ? regenCandidates.map((c) => (
                    <div key={c.text || String(c)} className="flex items-center justify-between gap-2 rounded-md border px-3 py-2">
                      <div className="text-sm text-stone-700">
                        <div>{c.text || String(c)}</div>
                        {c.rationale ? <div className="text-xs text-stone-500">{c.rationale}</div> : null}
                      </div>
                      <div className="flex gap-2">
                        <button
                          type="button"
                          onClick={async () => {
                            try {
                              const mod = await import("../store/brandStore");
                              const store = mod.useBrandStore.getState();
                              const newBrand = { ...(brandInfo as any) } as any;
                              const newDataC = { ...(dataC as any) } as any;
                              if (regenTarget === "brand_name") {
                                newBrand.brand_name = c.text || c;
                                newDataC.brand_name = c.text || c;
                                store.setBrandInfo(newBrand);
                                setDataC(newDataC);
                              } else if (regenTarget === "name_meaning") {
                                newBrand.name_meaning = c.text || c;
                                newDataC.name_meaning = c.text || c;
                                store.setBrandInfo(newBrand);
                                setDataC(newDataC);
                              } else if (regenTarget === "slogan") {
                                newBrand.slogan = c.text || c;
                                newDataC.slogan = c.text || c;
                                store.setBrandInfo(newBrand);
                                setDataC(newDataC);
                              } else if (regenTarget === "story_summary") {
                                newBrand.story_summary = c.text || c;
                                newDataC.story_summary = c.text || c;
                                store.setBrandInfo(newBrand);
                                setDataC(newDataC);
                              }
                              if (regenTarget) {
                                store.setAppliedSelection("C", regenTarget, c.text || c);
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
