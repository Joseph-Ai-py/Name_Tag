import { useMemo } from "react";
import { Eye, FileText, Image as ImageIcon } from "lucide-react";
import { useBrandStore } from "../store/brandStore";

function escapeHtml(value: unknown) {
  return String(value ?? "")
    .split("&").join("&amp;")
    .split("<").join("&lt;")
    .split(">").join("&gt;")
    .split('"').join("&quot;")
    .split("'").join("&#39;");
}

function renderSection(title: string, data: Record<string, any> | null) {
  const entries = data ? Object.entries(data) : [];

  return `
    <section style="margin-top: 18px; padding-top: 18px; border-top: 1px solid #e7e5e4;">
      <p style="margin: 0 0 10px; font-size: 12px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #a16207;">${escapeHtml(title)}</p>
      ${entries.length > 0 ? entries
        .map(
          ([key, value]) => `
            <div style="margin-bottom: 10px;">
              <div style="font-size: 12px; font-weight: 700; color: #44403c; margin-bottom: 4px;">${escapeHtml(key)}</div>
              <div style="font-size: 13px; line-height: 1.7; color: #57534e; white-space: pre-wrap; word-break: break-word;">${escapeHtml(value)}</div>
            </div>
          `,
        )
        .join("") : '<p style="margin: 0; font-size: 13px; color: #a8a29e;">아직 생성된 내용이 없습니다.</p>'}
    </section>
  `;
}

export function PdfPreviewSidebar() {
  const brandInfo = useBrandStore((state) => state.brandInfo);
  const dataA = useBrandStore((state) => state.dataA);
  const dataB = useBrandStore((state) => state.dataB);
  const dataC = useBrandStore((state) => state.dataC);
  const dataDE = useBrandStore((state) => state.dataDE);

  const logoPreview = dataDE?.logo_path ? `http://localhost:8000${dataDE.logo_path}` : null;
  const characterPreview = dataDE?.char_path ? `http://localhost:8000${dataDE.char_path}` : null;

  const htmlPreview = useMemo(() => {
    if (!brandInfo) {
      return null;
    }

    return `
      <div style="padding: 22px; font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #fffdf8; color: #1c1917;">
        <div style="display: flex; align-items: center; justify-content: space-between; gap: 16px; margin-bottom: 18px;">
          <div>
            <p style="margin: 0 0 6px; font-size: 12px; font-weight: 700; letter-spacing: 0.16em; text-transform: uppercase; color: #a16207;">PDF Preview</p>
            <h2 style="margin: 0; font-size: 26px; line-height: 1.2; color: #171717;">${escapeHtml(brandInfo.brand_name)}</h2>
            <p style="margin: 8px 0 0; font-size: 14px; color: #78716c;">${escapeHtml(brandInfo.brand_name_en)}</p>
          </div>
          <div style="width: 72px; height: 72px; border-radius: 18px; background: ${escapeHtml(brandInfo.seed_color)}; box-shadow: inset 0 0 0 1px rgba(255,255,255,0.55);"></div>
        </div>

        <div style="padding: 16px; border-radius: 20px; background: #ffffff; border: 1px solid #e7e5e4;">
          <p style="margin: 0 0 6px; font-size: 12px; font-weight: 700; color: #a16207;">핵심 요약</p>
          <p style="margin: 0; font-size: 14px; line-height: 1.8; color: #44403c;">${escapeHtml(brandInfo.story_summary)}</p>
        </div>

        ${renderSection("Section A", dataA)}
        ${renderSection("Section B", dataB)}
        ${renderSection("Section C", dataC)}
        ${renderSection("Section DE", dataDE)}
      </div>
    `;
  }, [brandInfo, dataA, dataB, dataC, dataDE]);

  return (
    <aside className="w-full rounded-3xl border border-stone-200 bg-white/85 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.07)] backdrop-blur dark:border-dark-border dark:bg-dark-bg2/85">
      <div className="mb-4 flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.35em] text-stone-500">Preview</p>
          <h2 className="mt-2 text-xl font-black tracking-tight text-stone-900">PDF 미리보기</h2>
          <p className="mt-2 text-sm leading-6 text-stone-500">생성 직전의 HTML 구조를 확인합니다.</p>
        </div>
        <div className="rounded-2xl bg-amber-50 p-3 text-amber-600">
          <Eye size={20} />
        </div>
      </div>

      <div className="space-y-4 overflow-y-auto pr-1">
        <div className="grid grid-cols-2 gap-3">
          <div className="rounded-2xl border border-stone-200 bg-stone-50 p-3">
            <div className="mb-2 flex items-center gap-2 text-xs font-semibold text-stone-500">
              <FileText size={14} />
              브랜드 요약
            </div>
            <p className="text-sm font-medium leading-6 text-stone-800">{brandInfo?.brand_name ?? "브랜드 정보 대기 중"}</p>
          </div>
          <div className="rounded-2xl border border-stone-200 bg-stone-50 p-3">
            <div className="mb-2 flex items-center gap-2 text-xs font-semibold text-stone-500">
              <ImageIcon size={14} />
              이미지
            </div>
            <p className="text-sm font-medium leading-6 text-stone-800">{logoPreview || characterPreview ? "생성됨" : "대기 중"}</p>
          </div>
        </div>

        <div className="space-y-3">
          <p className="text-sm font-semibold text-stone-700">생성 이미지</p>
          <div className="space-y-3">
            {logoPreview ? (
              <img src={logoPreview} alt="logo preview" className="h-32 w-full rounded-2xl border border-stone-200 bg-white p-3 object-contain" />
            ) : (
              <div className="rounded-2xl border border-dashed border-stone-300 bg-stone-50 p-6 text-center text-sm text-stone-500">로고 이미지가 아직 없습니다.</div>
            )}
            {characterPreview ? (
              <img src={characterPreview} alt="character preview" className="h-32 w-full rounded-2xl border border-stone-200 bg-white p-3 object-contain" />
            ) : (
              <div className="rounded-2xl border border-dashed border-stone-300 bg-stone-50 p-6 text-center text-sm text-stone-500">캐릭터 이미지가 아직 없습니다.</div>
            )}
          </div>
        </div>

        <div className="rounded-[1.5rem] border border-stone-200 bg-stone-50 p-1">
          {htmlPreview ? (
            <div className="max-h-[42rem] overflow-y-auto rounded-[1.25rem] bg-white" dangerouslySetInnerHTML={{ __html: htmlPreview }} />
          ) : (
            <div className="rounded-[1.25rem] bg-white p-6 text-sm leading-7 text-stone-500">
              Section O에서 브랜드를 확정하면 PDF 미리보기가 표시됩니다.
            </div>
          )}
        </div>
      </div>
    </aside>
  );
}