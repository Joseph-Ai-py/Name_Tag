import { useState } from "react";
import { ArrowLeft, ArrowRight, Sparkles } from "lucide-react";
import { generateSectionDE, getDEInterview, generateSectionDELogo, generateSectionDECharacter, regenerateSectionDEField } from "../api/client";
import { apiLogger } from "../api/client";
import { InterviewCard } from "../components/InterviewCard";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { PageFrame } from "../components/PageFrame";
import { SectionDEResult } from "../components/ResultDisplays/SectionDEResult";
import { useBrandStore } from "../store/brandStore";

export function SectionDE() {
  const brandInfo = useBrandStore((state) => state.brandInfo);
  const interviewDataA = useBrandStore((state) => state.interviewDataA);
  const interviewDataB = useBrandStore((state) => state.interviewDataB);
  const interviewDataC = useBrandStore((state) => state.interviewDataC);
  const interviewDataDE = useBrandStore((state) => state.interviewDataDE);
  const dataC = useBrandStore((state) => state.dataC);
  const dataDE = useBrandStore((state) => state.dataDE);
  const setInterviewDataDE = useBrandStore((state) => state.setInterviewDataDE);
  const setDataDE = useBrandStore((state) => state.setDataDE);
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
    return <PageFrame eyebrow="Section DE" title="브랜드 정보가 필요합니다" description="먼저 Section O에서 브랜드 후보를 확정해야 합니다." />;
  }

  const logoPreview = dataDE?.logo_path ? `http://localhost:8000${dataDE.logo_path}` : null;
  const characterPreview = dataDE?.char_path ? `http://localhost:8000${dataDE.char_path}` : null;

  return (
    <PageFrame
      eyebrow="Section DE"
      title="로고·캐릭터 인터뷰와 이미지 생성"
      description="비주얼 가이드 결과를 바탕으로 로고와 캐릭터 기획안을 만들고 이미지를 생성합니다."
      footer={
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <button
            type="button"
            onClick={() => setCurrentStep(3)}
            className="inline-flex items-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            <ArrowLeft size={16} />
            이전 단계
          </button>
          <button
            type="button"
            onClick={() => setCurrentStep(5)}
            disabled={!dataDE}
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
                apiLogger.info("Section DE: interview request", { brandName: brandInfo.brand_name, interviewCLength: interviewDataC.length });
                const response = await getDEInterview(brandInfo, interviewDataC);
                apiLogger.info("Section DE: interview response", { questionCount: response.questions?.length ?? 0 });
                setReasoning(response.reasoning || "");
                setQuestions(response.questions || []);
              } catch (error) {
                setError(error instanceof Error ? error.message : "Section DE 인터뷰 실패");
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
                if (!dataC) {
                  throw new Error("Section C 데이터를 먼저 생성해야 합니다.");
                }
                setError(null);
                setIsLoading(true);
                apiLogger.info("Section DE: generate request", {
                  brandName: brandInfo.brand_name,
                  dataCLength: Object.keys(dataC || {}).length,
                  interviewALength: interviewDataA.length,
                  interviewBLength: interviewDataB.length,
                  interviewCLength: interviewDataC.length,
                  interviewDELength: interviewDataDE.length,
                });
                const response = await generateSectionDE(
                  brandInfo,
                  dataC,
                  interviewDataA,
                  interviewDataB,
                  interviewDataC,
                  interviewDataDE,
                );
                apiLogger.info("Section DE: generate response", {
                  logoPath: response.data_de?.logo_path,
                  charPath: response.data_de?.char_path,
                  keys: Object.keys(response.data_de || {}),
                });
                setDataDE(response.data_de || {});
              } catch (error) {
                setError(error instanceof Error ? error.message : "Section DE 생성 실패");
              } finally {
                setIsLoading(false);
              }
            }}
            className="inline-flex items-center justify-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            생성 시작
          </button>
          <button
            type="button"
            onClick={async () => {
              try {
                if (!dataC) {
                  throw new Error("Section C 데이터를 먼저 생성해야 합니다.");
                }
                setError(null);
                setIsLoading(true);
                apiLogger.info("Section DE: generate logo only request", { brandName: brandInfo.brand_name });
                const response = await (await import("../api/client")).generateSectionDELogo(
                  brandInfo,
                  dataC,
                  interviewDataA,
                  interviewDataB,
                  interviewDataC,
                  interviewDataDE,
                );
                apiLogger.info("Section DE: generate logo only response", { logoPath: response.logo_path });
                setDataDE((prev: any) => ({ ...(prev || {}), ...response.data_de, logo_path: response.logo_path || response.data_de?.logo_path }));
              } catch (error) {
                setError(error instanceof Error ? error.message : "로고 생성 실패");
              } finally {
                setIsLoading(false);
              }
            }}
            className="inline-flex items-center justify-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            로고만 생성
          </button>

          <button
            type="button"
            onClick={async () => {
              try {
                if (!dataC) {
                  throw new Error("Section C 데이터를 먼저 생성해야 합니다.");
                }
                setError(null);
                setIsLoading(true);
                apiLogger.info("Section DE: generate character only request", { brandName: brandInfo.brand_name });
                const response = await (await import("../api/client")).generateSectionDECharacter(
                  brandInfo,
                  dataC,
                  interviewDataA,
                  interviewDataB,
                  interviewDataC,
                  interviewDataDE,
                );
                apiLogger.info("Section DE: generate character only response", { charPath: response.char_path });
                setDataDE((prev: any) => ({ ...(prev || {}), ...response.data_de, char_path: response.char_path || response.data_de?.char_path }));
              } catch (error) {
                setError(error instanceof Error ? error.message : "캐릭터 생성 실패");
              } finally {
                setIsLoading(false);
              }
            }}
            className="inline-flex items-center justify-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            캐릭터만 생성
          </button>
        </div>

        {isLoading && <LoadingSpinner label="D/E 섹션을 생성 중입니다..." />}
        {error && <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>}

        {questions.length > 0 && (
          <InterviewCard
            sectionKey="DE"
            questions={questions}
            reasoning={reasoning}
            onComplete={(formattedText) => {
              apiLogger.info("Section DE: interview text stored", { length: formattedText.length });
              setInterviewDataDE(formattedText);
            }}
          />
        )}

        {dataDE && (
          <>
            <div className="rounded-3xl border border-stone-200 bg-stone-50 p-6">
              <p className="font-semibold text-stone-900 mb-6">✨ 생성 결과</p>
              <SectionDEResult
                data={dataDE}
                onRegenerate={async (key, label) => {
                  try {
                    setError(null);
                    setIsLoading(true);
                    apiLogger.info(`Section DE: re-generate ${key}`, { brandName: brandInfo.brand_name });
                    const context = { existing: dataDE };
                    const resp = await regenerateSectionDEField(brandInfo, context, key);
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
          </>
        )}
      </div>
    </PageFrame>
  );
}
