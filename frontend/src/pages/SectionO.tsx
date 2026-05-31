import { useMemo, useState } from "react";
import { ArrowRight, Sparkles } from "lucide-react";
import { getOCandidates, getOInterview } from "../api/client";
import { CandidateSelector } from "../components/CandidateSelector";
import { InterviewCard } from "../components/InterviewCard";
import { LoadingSpinner } from "../components/LoadingSpinner";
import { PageFrame } from "../components/PageFrame";
import { apiLogger } from "../api/client";
import { BrandData, useBrandStore } from "../store/brandStore";

const vibeOptions = ["모던", "미니멀", "따뜻함", "프리미엄", "감성", "자연", "테크", "클래식"];

const emptyBrandData: BrandData = {
  business_type: "",
  vibes: [],
  target: "",
  keywords: "",
};

export function SectionO() {
  const brandInfo = useBrandStore((state) => state.brandInfo);
  const brandData = useBrandStore((state) => state.brandData ?? emptyBrandData);
  const setBrandData = useBrandStore((state) => state.setBrandData);
  const setBrandInfo = useBrandStore((state) => state.setBrandInfo);
  const setInterviewDataO = useBrandStore((state) => state.setInterviewDataO);
  const setCurrentStep = useBrandStore((state) => state.setCurrentStep);
  const setIsLoading = useBrandStore((state) => state.setIsLoading);
  const setError = useBrandStore((state) => state.setError);
  const interviewDataO = useBrandStore((state) => state.interviewDataO);
  const isLoading = useBrandStore((state) => state.isLoading);
  const error = useBrandStore((state) => state.error);

  const [questions, setQuestions] = useState<any[]>([]);
  const [reasoning, setReasoning] = useState("");
  const [candidates, setCandidates] = useState<any[]>([]);

  const canInterview = brandData.business_type.trim().length > 1 && brandData.target.trim().length > 1;
  const canGenerateCandidates = interviewDataO.trim().length > 0;

  const vibeSet = useMemo(() => new Set(brandData.vibes), [brandData.vibes]);

  const updateBrandData = (patch: Partial<BrandData>) => {
    setBrandData({ ...brandData, ...patch });
  };

  return (
    <PageFrame
      eyebrow="Section O"
      title="브랜드 초안 입력과 MVB 선택"
      description="업종, 감성, 타겟을 입력한 뒤 인터뷰를 거쳐 후보 4개를 믹스앤매치로 확정합니다."
      footer={
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="text-sm text-stone-500">섹션 O에서 브랜드 뼈대를 확정해야 다음 단계로 이동할 수 있습니다.</div>
          <button
            type="button"
            onClick={() => setCurrentStep(1)}
            disabled={!brandInfo}
            className="inline-flex items-center justify-center gap-2 rounded-full bg-stone-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-stone-800 disabled:cursor-not-allowed disabled:bg-stone-300"
          >
            다음 단계
            <ArrowRight size={16} />
          </button>
        </div>
      }
    >
      <div className="space-y-6">
        <div className="grid gap-4 md:grid-cols-2">
          <label className="space-y-2">
            <span className="text-sm font-semibold text-stone-700">업종 / 서비스</span>
            <input
              value={brandData.business_type}
              onChange={(event) => updateBrandData({ business_type: event.target.value })}
              className="w-full rounded-2xl border border-stone-200 bg-white px-4 py-3 text-stone-900 outline-none transition focus:border-amber-500"
              placeholder="예: 프리미엄 베이커리"
            />
          </label>

          <label className="space-y-2">
            <span className="text-sm font-semibold text-stone-700">타겟 고객</span>
            <input
              value={brandData.target}
              onChange={(event) => updateBrandData({ target: event.target.value })}
              className="w-full rounded-2xl border border-stone-200 bg-white px-4 py-3 text-stone-900 outline-none transition focus:border-amber-500"
              placeholder="예: 감도 높은 20~30대"
            />
          </label>

          <label className="space-y-2 md:col-span-2">
            <span className="text-sm font-semibold text-stone-700">추가 키워드</span>
            <input
              value={brandData.keywords}
              onChange={(event) => updateBrandData({ keywords: event.target.value })}
              className="w-full rounded-2xl border border-stone-200 bg-white px-4 py-3 text-stone-900 outline-none transition focus:border-amber-500"
              placeholder="예: 지속가능성, 감성, 세련됨"
            />
          </label>
        </div>

        <div className="space-y-3">
          <p className="text-sm font-semibold text-stone-700">브랜드 감성 선택</p>
          <div className="flex flex-wrap gap-2">
            {vibeOptions.map((vibe) => {
              const active = vibeSet.has(vibe);
              return (
                <button
                  key={vibe}
                  type="button"
                  onClick={() =>
                    updateBrandData({
                      vibes: active ? brandData.vibes.filter((item) => item !== vibe) : [...brandData.vibes, vibe],
                    })
                  }
                  className={`rounded-full border px-4 py-2 text-sm font-medium transition ${
                    active
                      ? "border-amber-500 bg-amber-50 text-amber-900"
                      : "border-stone-200 bg-white text-stone-600 hover:border-amber-300 hover:bg-amber-50/40"
                  }`}
                >
                  {vibe}
                </button>
              );
            })}
          </div>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row">
          <button
            type="button"
            disabled={!canInterview}
            onClick={async () => {
              try {
                setError(null);
                setIsLoading(true);
                apiLogger.info("Section O: interview request", {
                  business_type: brandData.business_type,
                  target: brandData.target,
                  vibes: brandData.vibes,
                  keywords: brandData.keywords,
                });
                const response = await getOInterview(brandData);
                apiLogger.info("Section O: interview response", {
                  questionCount: response.questions?.length ?? 0,
                  reasoningLength: String(response.reasoning || "").length,
                });
                setReasoning(response.reasoning || "");
                setQuestions(response.questions || []);
              } catch (error) {
                setError(error instanceof Error ? error.message : "인터뷰 질문 생성 실패");
              } finally {
                setIsLoading(false);
              }
            }}
            className="inline-flex items-center justify-center gap-2 rounded-full bg-amber-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-amber-600 disabled:cursor-not-allowed disabled:bg-stone-300"
          >
            <Sparkles size={16} />
            인터뷰 시작
          </button>

          <button
            type="button"
            disabled={!canGenerateCandidates}
            onClick={async () => {
              try {
                setError(null);
                setIsLoading(true);
                apiLogger.info("Section O: candidates request", {
                  interviewLength: interviewDataO.length,
                  brandName: brandInfo?.brand_name,
                });
                const response = await getOCandidates(brandData, interviewDataO);
                apiLogger.info("Section O: candidates response", {
                  candidateCount: response.candidates?.length ?? 0,
                });
                setCandidates(response.candidates || []);
              } catch (error) {
                setError(error instanceof Error ? error.message : "후보 생성 실패");
              } finally {
                setIsLoading(false);
              }
            }}
            className="inline-flex items-center justify-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40 disabled:cursor-not-allowed disabled:bg-stone-100"
          >
            후보 생성
          </button>
        </div>

        {isLoading && <LoadingSpinner label="AI가 질문 또는 후보를 생성 중입니다..." />}

        {error && <div className="rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</div>}

        {questions.length > 0 && (
          <InterviewCard
            questions={questions}
            reasoning={reasoning}
            onComplete={(formattedText) => {
              apiLogger.info("Section O: interview text stored", { length: formattedText.length });
              setInterviewDataO(formattedText);
            }}
          />
        )}

        {candidates.length > 0 && (
          <CandidateSelector
            candidates={candidates}
            onComplete={(brandInfo) => {
              apiLogger.info("Section O: brand candidate selected", { brandName: (brandInfo as any)?.brand_name });
              setBrandInfo(brandInfo as any);
              setCurrentStep(1);
            }}
          />
        )}
      </div>
    </PageFrame>
  );
}
