import { useMemo, useState } from "react";
import { Eye, Settings, ChevronDown } from "lucide-react";
import { useBrandStore } from "../store/brandStore";

type SidebarTab = "preview" | "editor";

export function RightSidebar() {
  const [activeTab, setActiveTab] = useState<SidebarTab>("preview");
  const [expandedSections, setExpandedSections] = useState<Set<string>>(
    new Set(["brandInfo", "dataA"])
  );

  const brandInfo = useBrandStore((state) => state.brandInfo);
  const dataA = useBrandStore((state) => state.dataA);
  const dataB = useBrandStore((state) => state.dataB);
  const dataC = useBrandStore((state) => state.dataC);
  const dataDE = useBrandStore((state) => state.dataDE);

  const toggleSection = (sectionId: string) => {
    const newSet = new Set(expandedSections);
    if (newSet.has(sectionId)) {
      newSet.delete(sectionId);
    } else {
      newSet.add(sectionId);
    }
    setExpandedSections(newSet);
  };

  const htmlPreview = useMemo(() => {
    // 간단한 HTML 미리보기 생성
    if (!brandInfo) return null;

    return `
      <div style="padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;">
        <h2 style="font-size: 24px; margin: 0 0 12px 0; color: #1a1a1a;">
          ${brandInfo.brand_name}
        </h2>
        <p style="font-size: 14px; color: #737373; margin: 0 0 16px 0;">
          ${brandInfo.brand_name_en}
        </p>
        <div style="border-top: 1px solid #e5e5e5; padding: 12px 0; margin: 12px 0;">
          <p style="font-size: 13px; color: #737373; margin: 0 0 4px 0;">의미</p>
          <p style="font-size: 14px; margin: 0; color: #1a1a1a;">
            ${brandInfo.name_meaning}
          </p>
        </div>
        <div style="border-top: 1px solid #e5e5e5; padding: 12px 0; margin: 12px 0;">
          <p style="font-size: 13px; color: #737373; margin: 0 0 4px 0;">슬로건</p>
          <p style="font-size: 14px; margin: 0; color: #1a1a1a;">
            ${brandInfo.slogan}
          </p>
        </div>
        <div style="background: ${brandInfo.seed_color}; width: 100%; height: 60px; border-radius: 8px; margin-top: 12px;"></div>
      </div>
    `;
  }, [brandInfo]);

  return (
    <aside className="hidden rounded-3xl border border-stone-200 bg-white/80 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.07)] backdrop-blur lg:block">
      {/* 탭 버튼 */}
      <div className="mb-5 flex gap-2 border-b border-stone-200">
        <button
          onClick={() => setActiveTab("preview")}
          className={`flex items-center gap-2 pb-3 text-sm font-semibold transition ${
            activeTab === "preview"
              ? "border-b-2 border-amber-500 text-amber-600"
              : "text-stone-500 hover:text-stone-700"
          }`}
        >
          <Eye size={16} />
          미리보기
        </button>
        <button
          onClick={() => setActiveTab("editor")}
          className={`flex items-center gap-2 pb-3 text-sm font-semibold transition ${
            activeTab === "editor"
              ? "border-b-2 border-amber-500 text-amber-600"
              : "text-stone-500 hover:text-stone-700"
          }`}
        >
          <Settings size={16} />
          변수 수정
        </button>
      </div>

      {/* 미리보기 탭 */}
      {activeTab === "preview" && (
        <div className="max-h-[600px] overflow-y-auto">
          <div className="mb-4 flex items-center justify-center gap-3">
            <img src="/logo/logo_onoff_20260531.png" alt="logo preview" className="h-16 w-auto rounded-md bg-white p-1 object-contain" />
            <img src="/logo/char_onoff_20260531.png" alt="char preview" className="h-16 w-auto rounded-md bg-white p-1 object-contain" />
          </div>
          {htmlPreview ? (
            <div
              className="rounded-xl border border-stone-200 bg-stone-50"
              dangerouslySetInnerHTML={{ __html: htmlPreview }}
            />
          ) : (
            <div className="rounded-xl border border-stone-200 bg-stone-50 p-4 text-center text-sm text-stone-500">
              브랜드 정보를 입력하면 미리보기가 표시됩니다.
            </div>
          )}
        </div>
      )}

      {/* 변수 수정 탭 */}
      {activeTab === "editor" && (
        <div className="max-h-[600px] space-y-3 overflow-y-auto">
          {/* 브랜드 정보 */}
          <div className="rounded-xl border border-stone-200">
            <button
              onClick={() => toggleSection("brandInfo")}
              className="flex w-full items-center justify-between bg-stone-50 px-4 py-3 text-sm font-semibold text-stone-900 hover:bg-stone-100"
            >
              <span>브랜드 정보</span>
              <ChevronDown
                size={16}
                className={`transition ${
                  expandedSections.has("brandInfo") ? "rotate-180" : ""
                }`}
              />
            </button>
            {expandedSections.has("brandInfo") && brandInfo && (
              <div className="space-y-2 border-t border-stone-200 p-3 text-xs">
                <div>
                  <p className="font-semibold text-stone-700">브랜드명</p>
                  <p className="text-stone-600">{brandInfo.brand_name}</p>
                </div>
                <div>
                  <p className="font-semibold text-stone-700">의미</p>
                  <p className="text-stone-600">{brandInfo.name_meaning}</p>
                </div>
                <div>
                  <p className="font-semibold text-stone-700">슬로건</p>
                  <p className="text-stone-600">{brandInfo.slogan}</p>
                </div>
                <div className="flex items-center gap-2">
                  <p className="font-semibold text-stone-700">대표색</p>
                  <div
                    className="h-6 w-6 rounded border border-stone-300"
                    style={{ backgroundColor: brandInfo.seed_color }}
                  />
                </div>
              </div>
            )}
          </div>

          {/* 섹션 A */}
          {dataA && (
            <div className="rounded-xl border border-stone-200">
              <button
                onClick={() => toggleSection("dataA")}
                className="flex w-full items-center justify-between bg-stone-50 px-4 py-3 text-sm font-semibold text-stone-900 hover:bg-stone-100"
              >
                <span>Section A - 철학/스토리</span>
                <ChevronDown
                  size={16}
                  className={`transition ${
                    expandedSections.has("dataA") ? "rotate-180" : ""
                  }`}
                />
              </button>
              {expandedSections.has("dataA") && (
                <div className="space-y-2 border-t border-stone-200 p-3 text-xs">
                  {Object.entries(dataA).map(([key, value]) => (
                    <div key={key}>
                      <p className="font-semibold text-stone-700">{key}</p>
                      <p className="truncate text-stone-600">
                        {String(value).substring(0, 50)}
                        {String(value).length > 50 ? "..." : ""}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* 섹션 B */}
          {dataB && (
            <div className="rounded-xl border border-stone-200">
              <button
                onClick={() => toggleSection("dataB")}
                className="flex w-full items-center justify-between bg-stone-50 px-4 py-3 text-sm font-semibold text-stone-900 hover:bg-stone-100"
              >
                <span>Section B - 타겟/여정</span>
                <ChevronDown
                  size={16}
                  className={`transition ${
                    expandedSections.has("dataB") ? "rotate-180" : ""
                  }`}
                />
              </button>
              {expandedSections.has("dataB") && (
                <div className="space-y-2 border-t border-stone-200 p-3 text-xs">
                  {Object.entries(dataB).map(([key, value]) => (
                    <div key={key}>
                      <p className="font-semibold text-stone-700">{key}</p>
                      <p className="truncate text-stone-600">
                        {String(value).substring(0, 50)}
                        {String(value).length > 50 ? "..." : ""}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* 섹션 C */}
          {dataC && (
            <div className="rounded-xl border border-stone-200">
              <button
                onClick={() => toggleSection("dataC")}
                className="flex w-full items-center justify-between bg-stone-50 px-4 py-3 text-sm font-semibold text-stone-900 hover:bg-stone-100"
              >
                <span>Section C - 비주얼</span>
                <ChevronDown
                  size={16}
                  className={`transition ${
                    expandedSections.has("dataC") ? "rotate-180" : ""
                  }`}
                />
              </button>
              {expandedSections.has("dataC") && (
                <div className="space-y-2 border-t border-stone-200 p-3 text-xs">
                  {Object.entries(dataC).map(([key, value]) => (
                    <div key={key}>
                      <p className="font-semibold text-stone-700">{key}</p>
                      <p className="truncate text-stone-600">
                        {String(value).substring(0, 50)}
                        {String(value).length > 50 ? "..." : ""}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* 섹션 DE */}
          {dataDE && (
            <div className="rounded-xl border border-stone-200">
              <button
                onClick={() => toggleSection("dataDE")}
                className="flex w-full items-center justify-between bg-stone-50 px-4 py-3 text-sm font-semibold text-stone-900 hover:bg-stone-100"
              >
                <span>Section DE - 로고/캐릭터</span>
                <ChevronDown
                  size={16}
                  className={`transition ${
                    expandedSections.has("dataDE") ? "rotate-180" : ""
                  }`}
                />
              </button>
              {expandedSections.has("dataDE") && (
                <div className="space-y-2 border-t border-stone-200 p-3 text-xs">
                  {Object.entries(dataDE).map(([key, value]) => (
                    <div key={key}>
                      <p className="font-semibold text-stone-700">{key}</p>
                      <p className="truncate text-stone-600">
                        {String(value).substring(0, 50)}
                        {String(value).length > 50 ? "..." : ""}
                      </p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </aside>
  );
}
