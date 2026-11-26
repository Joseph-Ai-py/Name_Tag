function escapeHtml(value: unknown): string {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

/** Small browser-only brand brief preview. The final report PDF is rendered by the backend PDF builder. */
export function buildSectionOHtml(brandData: Record<string, unknown> = {}, selected: Record<string, unknown> = {}) {
  const vibes = Array.isArray(brandData.vibes) ? brandData.vibes.map(escapeHtml).join(", ") : escapeHtml(brandData.vibes);
  const brandName = escapeHtml(selected.brand_name || brandData.brand_name || "브랜드명 미정");
  const rows = [
    ["업종 / 서비스", brandData.business_type],
    ["타겟 고객", brandData.target],
    ["브랜드 분위기", vibes],
    ["핵심 키워드", brandData.keywords],
  ].map(([key, value]) => `<div class="row"><span>${escapeHtml(key)}</span><strong>${escapeHtml(value)}</strong></div>`).join("");
  return `<!doctype html><html lang="ko"><meta charset="utf-8"><style>
    *{box-sizing:border-box}body{margin:0;padding:24px;background:#fafaf9;color:#1c1917;font-family:Arial,'Malgun Gothic',sans-serif}
    main{max-width:680px;margin:auto;padding:28px;border:1px solid #e7e5e4;border-radius:22px;background:#fff}
    .eyebrow{color:#a16207;font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase}
    h1{margin:10px 0 22px;font-size:32px}.row{display:flex;justify-content:space-between;gap:18px;padding:12px 0;border-top:1px solid #f0eeeb;font-size:14px}
    .row span{color:#78716c}.row strong{text-align:right;font-weight:600}
  </style><main><p class="eyebrow">NAME TAG · 브랜드 전략 보고서</p><h1>${brandName}</h1>${rows}</main></html>`;
}
