import { useState } from "react";
import { ArrowLeft, Download, AlertCircle } from "lucide-react";
import { generatePDF } from "../api/client";
import { apiLogger } from "../api/client";
import { PageFrame } from "../components/PageFrame";
import { useBrandStore } from "../store/brandStore";
import { PdfPreviewSidebar } from "../components/PdfPreviewSidebar";

export function Preview() {
  const brandInfo = useBrandStore((state) => state.brandInfo);
  const dataA = useBrandStore((state) => state.dataA);
  const dataB = useBrandStore((state) => state.dataB);
  const dataC = useBrandStore((state) => state.dataC);
  const dataDE = useBrandStore((state) => state.dataDE);
  const setCurrentStep = useBrandStore((state) => state.setCurrentStep);
  const setError = useBrandStore((state) => state.setError);
  const error = useBrandStore((state) => state.error);

  const [isExporting, setIsExporting] = useState(false);

  // 💡 빈 객체({}) 일 경우에도 정확히 필터링하도록 검증 로직 강화
  const isReadyToExport =
    dataA && Object.keys(dataA).length > 0 &&
    dataB && Object.keys(dataB).length > 0 &&
    dataC && Object.keys(dataC).length > 0 &&
    dataDE && Object.keys(dataDE).length > 0;

  if (!brandInfo) {
    return <PageFrame eyebrow="Preview" title="브랜드 정보가 필요합니다" description="먼저 Section O에서 브랜드 후보를 확정해야 합니다." />;
  }

  return (
    <PageFrame
      eyebrow="Preview"
      title="PDF 미리보기와 다운로드"
      description="섹션별 데이터가 모두 모이면 브랜드 가이드를 PDF로 내려받을 수 있습니다."
      footer={
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <button
            type="button"
            onClick={() => setCurrentStep(4)}
            className="inline-flex items-center justify-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            <ArrowLeft size={16} />
            이전 단계
          </button>
          <button
            type="button"
            disabled={!isReadyToExport || isExporting}
            onClick={async () => {
              try {
                setError(null);
                setIsExporting(true);
                apiLogger.info("Preview: pdf export clicked", {
                  brandName: brandInfo.brand_name,
                  hasA: Boolean(dataA),
                  hasB: Boolean(dataB),
                  hasC: Boolean(dataC),
                  hasDE: Boolean(dataDE),
                });
                await generatePDF(brandInfo, dataA, dataB, dataC, dataDE);
              } catch (err) {
                setError(err instanceof Error ? err.message : "PDF 다운로드 중 오류가 발생했습니다.");
              } finally {
                setIsExporting(false);
              }
            }}
            className="inline-flex items-center justify-center gap-2 rounded-full bg-amber-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-amber-600 disabled:cursor-not-allowed disabled:bg-stone-300"
          >
            <Download size={16} />
            {isExporting ? "다운로드 준비 중..." : "PDF 다운로드"}
          </button>
        </div>
      }
    >
      {/* 💡 에러 발생 시 알림 표시 */}
      {error && (
        <div className="mb-6 flex items-center gap-3 rounded-2xl border border-rose-200 bg-rose-50 px-5 py-4 text-sm text-rose-700">
          <AlertCircle size={18} className="shrink-0" />
          <p>{error}</p>
        </div>
      )}

      {/* 💡 반응형 그리드: 모바일은 1열 세로 스택, 데스크톱은 2:1 분할 레이아웃 */}
      <div className="grid gap-6 lg:grid-cols-3 lg:items-start">
        
        {/* 좌측 콘텐츠 (브랜드 정보 + 체크리스트) */}
        <div className="flex flex-col gap-6 lg:col-span-2">
          <div className="rounded-3xl border border-stone-200 bg-white p-6 shadow-[0_8px_30px_rgba(15,23,42,0.04)] md:p-8">
            <p className="text-sm font-semibold text-amber-500 tracking-wide uppercase">확정 브랜드</p>
            <h3 className="mt-2 text-3xl font-black tracking-tight text-stone-900 md:text-4xl">{brandInfo.brand_name}</h3>
            <p className="mt-4 text-base leading-relaxed text-stone-600">{brandInfo.story_summary}</p>
          </div>

          <div className="rounded-3xl border border-stone-200 bg-stone-50 p-6 md:p-8 text-sm leading-7 text-stone-700">
            <p className="text-base font-semibold text-stone-900 mb-3">📋 내보내기 체크리스트</p>
            <ul className="space-y-3">
              <li className="flex items-start gap-2">
                <span className="text-stone-400 mt-0.5">•</span>
                <span className={!isReadyToExport ? "text-rose-500 font-medium" : "text-stone-600"}>
                  Section A, B, C, DE 결과가 모두 저장되어 있는지 확인합니다. {!isReadyToExport && "(데이터 누락 됨)"}
                </span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-stone-400 mt-0.5">•</span>
                <span>이미지는 로컬 백엔드의 <code className="rounded bg-stone-200 px-1.5 py-0.5 text-xs">/assets</code> 경로를 통해 렌더링됩니다.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-stone-400 mt-0.5">•</span>
                <span>다운로드 후 PDF가 깨지면 백엔드의 WeasyPrint 의존성을 확인합니다.</span>
              </li>
            </ul>
          </div>
        </div>

        {/* 우측 사이드바 (PDF 미리보기) */}
        <div className="lg:col-span-1 lg:sticky lg:top-6">
          <div className="overflow-hidden rounded-3xl border border-stone-200 bg-white shadow-[0_8px_30px_rgba(15,23,42,0.04)]">
            <PdfPreviewSidebar />
          </div>
        </div>
        
      </div>
    </PageFrame>
  );
}
