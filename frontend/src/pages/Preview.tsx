import { useState } from "react";
import { ArrowLeft, Download } from "lucide-react";
import { generatePDF } from "../api/client";
import { PageFrame } from "../components/PageFrame";
import { useBrandStore } from "../store/brandStore";

export function Preview() {
  const brandInfo = useBrandStore((state) => state.brandInfo);
  const dataA = useBrandStore((state) => state.dataA);
  const dataB = useBrandStore((state) => state.dataB);
  const dataC = useBrandStore((state) => state.dataC);
  const dataDE = useBrandStore((state) => state.dataDE);
  const setCurrentStep = useBrandStore((state) => state.setCurrentStep);

  const [isExporting, setIsExporting] = useState(false);

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
            className="inline-flex items-center gap-2 rounded-full border border-stone-200 bg-white px-5 py-3 text-sm font-semibold text-stone-800 transition hover:border-amber-300 hover:bg-amber-50/40"
          >
            <ArrowLeft size={16} />
            이전 단계
          </button>
          <button
            type="button"
            disabled={!dataA || !dataB || !dataC || !dataDE || isExporting}
            onClick={async () => {
              try {
                setIsExporting(true);
                await generatePDF(brandInfo, dataA, dataB, dataC, dataDE);
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
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="rounded-3xl border border-stone-200 bg-stone-50 p-5">
          <p className="text-sm font-semibold text-stone-500">확정 브랜드</p>
          <h3 className="mt-2 text-2xl font-black text-stone-900">{brandInfo.brand_name}</h3>
          <p className="mt-2 text-sm text-stone-600">{brandInfo.story_summary}</p>
        </div>

        <div className="rounded-3xl border border-stone-200 bg-stone-50 p-5 text-sm leading-7 text-stone-700">
          <p className="font-semibold text-stone-900">체크리스트</p>
          <ul className="mt-3 space-y-2">
            <li>Section A, B, C, DE 결과가 모두 저장되어 있는지 확인합니다.</li>
            <li>이미지는 로컬 백엔드의 /assets 경로를 통해 렌더링됩니다.</li>
            <li>다운로드 후 PDF가 깨지면 백엔드의 WeasyPrint 의존성을 확인합니다.</li>
          </ul>
        </div>
      </div>
    </PageFrame>
  );
}
