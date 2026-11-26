import { useEffect, useState } from "react";
import { Eye, FileText } from "lucide-react";
import { createReportV2PdfBlob, type ReportV2Page } from "../api/client";

export function PdfPreviewSidebar({ brand, pages }: {
  brand: { brand_name: string; business_type: string; target: string };
  pages: Record<string, ReportV2Page>;
}) {
  const [pdfUrl, setPdfUrl] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  useEffect(() => {
    if (!Object.keys(pages).length) {
      setPdfUrl("");
      return;
    }
    let disposed = false;
    let nextUrl = "";
    setLoading(true);
    setError("");
    createReportV2PdfBlob(pages, brand.brand_name || "NAME TAG")
      .then((blob) => {
        if (disposed) return;
        nextUrl = URL.createObjectURL(blob);
        setPdfUrl(nextUrl);
      })
      .catch((reason: unknown) => {
        if (!disposed) setError(reason instanceof Error ? reason.message : "PDF 미리보기를 만들지 못했습니다.");
      })
      .finally(() => { if (!disposed) setLoading(false); });
    return () => {
      disposed = true;
      if (nextUrl) URL.revokeObjectURL(nextUrl);
    };
  }, [brand.brand_name, pages]);

  return <aside className="space-y-4 rounded-3xl border border-stone-200 bg-white/90 p-5 shadow-sm">
    <div className="flex items-start gap-3"><div className="rounded-2xl bg-amber-50 p-3 text-amber-700"><Eye size={20} /></div><div>
      <p className="text-xs font-semibold uppercase tracking-[0.25em] text-stone-500">NAME TAG · PDF BUILDER</p><h2 className="mt-1 text-xl font-black text-stone-900">실제 PDF 미리보기</h2>
      <p className="mt-2 text-sm leading-6 text-stone-600">백엔드 PDF 빌더가 렌더링한 결과입니다. 페이지마다 지정된 A4/A3 크기와 방향이 그대로 표시됩니다.</p>
    </div></div>
    <div className="rounded-2xl bg-stone-50 p-4"><div className="flex items-center gap-2 text-xs font-semibold text-stone-500"><FileText size={14} />브랜드 정보</div>
      <h3 className="mt-2 text-lg font-bold text-stone-900">{brand.brand_name || "브랜드명 입력 대기"}</h3>
      <p className="text-sm text-stone-600">{[brand.business_type, brand.target].filter(Boolean).join(" · ")}</p>
      <p className="mt-2 text-xs text-stone-500">포함 페이지 {Object.keys(pages).length}개</p>
    </div>
    {error && <p role="alert" className="rounded-xl bg-rose-50 p-3 text-sm text-rose-700">{error}</p>}
    {loading && <p className="text-sm text-stone-500">PDF 페이지를 다시 렌더링하는 중입니다…</p>}
    {pdfUrl && <iframe title="NAME TAG PDF 미리보기" src={pdfUrl} className="h-[70vh] min-h-[32rem] w-full rounded-xl border border-stone-200" />}
    {!Object.keys(pages).length && <p className="rounded-2xl border border-dashed border-stone-300 p-4 text-sm text-stone-500">아직 PDF에 담을 보고서 페이지가 없습니다.</p>}
  </aside>;
}
