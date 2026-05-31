import { useState } from "react";
import { ArrowLeft, ArrowRight, Sparkles } from "lucide-react";
import { generateSectionC, getCInterview } from "../api/client";
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
                const response = await getCInterview(brandInfo);
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
                const response = await generateSectionC(brandInfo, interviewDataA, interviewDataB, interviewDataC);
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

        {questions.length > 0 && <InterviewCard questions={questions} reasoning={reasoning} onComplete={setInterviewDataC} />}

        {dataC && (
          <div className="rounded-3xl border border-stone-200 bg-stone-50 p-5 text-sm leading-7 text-stone-700">
            <p className="font-semibold text-stone-900">생성 결과</p>
            <pre className="mt-3 overflow-x-auto whitespace-pre-wrap">{JSON.stringify(dataC, null, 2)}</pre>
          </div>
        )}
      </div>
    </PageFrame>
  );
}
