import { useEffect, useMemo, useState } from "react";
import { FileJson, Palette, SlidersHorizontal, Type } from "lucide-react";
import { type BrandInfo, useBrandStore } from "../store/brandStore";

function useJsonDraft<T extends Record<string, any>>(value: T | null) {
  const [draft, setDraft] = useState(() => JSON.stringify(value ?? {}, null, 2));
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setDraft(JSON.stringify(value ?? {}, null, 2));
    setError(null);
  }, [value]);

  const updateDraft = (next: string, onValid: (parsed: T) => void) => {
    setDraft(next);

    if (next.trim().length === 0) {
      setError("JSON 객체를 입력하세요.");
      return;
    }

    try {
      const parsed = JSON.parse(next) as T;
      if (parsed === null || Array.isArray(parsed) || typeof parsed !== "object") {
        setError("JSON 객체만 허용됩니다.");
        return;
      }

      setError(null);
      onValid(parsed);
    } catch {
      setError("유효한 JSON 형식이 아닙니다.");
    }
  };

  return { draft, error, updateDraft };
}

function JsonEditor<T extends Record<string, any>>({
  title,
  description,
  value,
  onChange,
}: {
  title: string;
  description: string;
  value: T | null;
  onChange: (next: T) => void;
}) {
  const { draft, error, updateDraft } = useJsonDraft(value);

  return (
    <div className="rounded-3xl border border-stone-200 bg-white p-4 shadow-sm">
      <div className="mb-3 flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-bold text-stone-900">{title}</p>
          <p className="mt-1 text-xs leading-5 text-stone-500">{description}</p>
        </div>
        <div className="rounded-2xl bg-stone-100 p-2 text-stone-500">
          <FileJson size={16} />
        </div>
      </div>

      <textarea
        value={draft}
        onChange={(event) => updateDraft(event.target.value, onChange)}
        className="min-h-[14rem] w-full rounded-2xl border border-stone-200 bg-stone-50 px-4 py-3 font-mono text-xs leading-6 text-stone-800 outline-none transition focus:border-amber-400 focus:bg-white"
        spellCheck={false}
      />

      {error ? (
        <p className="mt-2 text-xs font-medium text-rose-600">{error}</p>
      ) : (
        <p className="mt-2 text-xs text-stone-500">저장된 값은 즉시 미리보기와 PDF 생성에 반영됩니다.</p>
      )}
    </div>
  );
}

function BrandField({
  label,
  value,
  onChange,
  placeholder,
}: {
  label: string;
  value: string;
  onChange: (next: string) => void;
  placeholder?: string;
}) {
  return (
    <label className="space-y-2">
      <span className="text-xs font-semibold uppercase tracking-[0.25em] text-stone-500">{label}</span>
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="w-full rounded-2xl border border-stone-200 bg-stone-50 px-4 py-3 text-sm text-stone-900 outline-none transition focus:border-amber-400 focus:bg-white"
      />
    </label>
  );
}

export function PdfVariableSidebar() {
  const brandInfo = useBrandStore((state) => state.brandInfo);
  const dataA = useBrandStore((state) => state.dataA);
  const dataB = useBrandStore((state) => state.dataB);
  const dataC = useBrandStore((state) => state.dataC);
  const dataDE = useBrandStore((state) => state.dataDE);
  const setBrandInfo = useBrandStore((state) => state.setBrandInfo);
  const setDataA = useBrandStore((state) => state.setDataA);
  const setDataB = useBrandStore((state) => state.setDataB);
  const setDataC = useBrandStore((state) => state.setDataC);
  const setDataDE = useBrandStore((state) => state.setDataDE);

  const editableBrandInfo = useMemo<BrandInfo>(
    () =>
      brandInfo ?? {
        brand_name: "",
        brand_name_en: "",
        name_meaning: "",
        slogan: "",
        story_summary: "",
        seed_color: "#000000",
        seed_color_reason: "",
      },
    [brandInfo],
  );

  const updateBrandField = (field: keyof BrandInfo, value: string) => {
    setBrandInfo({ ...editableBrandInfo, [field]: value });
  };

  return (
    <aside className="w-full rounded-3xl border border-stone-200 bg-white/85 p-5 shadow-[0_24px_70px_rgba(15,23,42,0.07)] backdrop-blur dark:border-dark-border dark:bg-dark-bg2/85">
      <div className="mb-5 flex items-start justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.35em] text-stone-500">Variables</p>
          <h2 className="mt-2 text-xl font-black tracking-tight text-stone-900">PDF 변수 수정</h2>
          <p className="mt-2 text-sm leading-6 text-stone-500">브랜드 정보와 섹션 데이터를 직접 수정합니다.</p>
        </div>
        <div className="rounded-2xl bg-stone-100 p-3 text-stone-500">
          <SlidersHorizontal size={20} />
        </div>
      </div>

      <div className="space-y-5 overflow-y-auto pr-1">
        <div className="rounded-3xl border border-stone-200 bg-stone-50 p-4">
          <div className="mb-4 flex items-center gap-2 text-sm font-semibold text-stone-700">
            <Type size={16} />
            브랜드 기본 변수
          </div>

          <div className="grid gap-4">
            <BrandField label="브랜드명" value={editableBrandInfo.brand_name} onChange={(value) => updateBrandField("brand_name", value)} placeholder="브랜드명을 입력하세요" />
            <BrandField label="영문명" value={editableBrandInfo.brand_name_en} onChange={(value) => updateBrandField("brand_name_en", value)} placeholder="Brand name in English" />
            <BrandField label="이름 의미" value={editableBrandInfo.name_meaning} onChange={(value) => updateBrandField("name_meaning", value)} placeholder="이름에 담긴 의미" />
            <BrandField label="슬로건" value={editableBrandInfo.slogan} onChange={(value) => updateBrandField("slogan", value)} placeholder="짧은 슬로건" />
            <label className="space-y-2">
              <span className="text-xs font-semibold uppercase tracking-[0.25em] text-stone-500">대표색</span>
              <div className="flex gap-3">
                <input
                  type="color"
                  value={editableBrandInfo.seed_color || "#000000"}
                  onChange={(event) => updateBrandField("seed_color", event.target.value)}
                  className="h-12 w-14 cursor-pointer rounded-2xl border border-stone-200 bg-white p-1"
                />
                <input
                  value={editableBrandInfo.seed_color}
                  onChange={(event) => updateBrandField("seed_color", event.target.value)}
                  placeholder="#000000"
                  className="flex-1 rounded-2xl border border-stone-200 bg-white px-4 py-3 text-sm text-stone-900 outline-none transition focus:border-amber-400"
                />
              </div>
            </label>
            <label className="space-y-2">
              <span className="text-xs font-semibold uppercase tracking-[0.25em] text-stone-500">대표색 이유</span>
              <textarea
                value={editableBrandInfo.seed_color_reason}
                onChange={(event) => updateBrandField("seed_color_reason", event.target.value)}
                className="min-h-[7rem] w-full rounded-2xl border border-stone-200 bg-white px-4 py-3 text-sm leading-6 text-stone-800 outline-none transition focus:border-amber-400"
                placeholder="색상 선정 이유"
              />
            </label>
            <label className="space-y-2">
              <span className="text-xs font-semibold uppercase tracking-[0.25em] text-stone-500">브랜드 요약</span>
              <textarea
                value={editableBrandInfo.story_summary}
                onChange={(event) => updateBrandField("story_summary", event.target.value)}
                className="min-h-[8rem] w-full rounded-2xl border border-stone-200 bg-white px-4 py-3 text-sm leading-6 text-stone-800 outline-none transition focus:border-amber-400"
                placeholder="브랜드 가이드에 들어갈 요약"
              />
            </label>
          </div>
        </div>

        <JsonEditor
          title="Section A 데이터"
          description="철학/스토리 섹션 전체를 JSON 객체로 수정합니다."
          value={dataA}
          onChange={setDataA}
        />
        <JsonEditor
          title="Section B 데이터"
          description="타겟/여정 섹션 전체를 JSON 객체로 수정합니다."
          value={dataB}
          onChange={setDataB}
        />
        <JsonEditor
          title="Section C 데이터"
          description="비주얼 섹션 전체를 JSON 객체로 수정합니다."
          value={dataC}
          onChange={setDataC}
        />
        <JsonEditor
          title="Section DE 데이터"
          description="로고/캐릭터 정보와 이미지 경로를 포함한 객체를 수정합니다."
          value={dataDE}
          onChange={setDataDE}
        />
      </div>
    </aside>
  );
}