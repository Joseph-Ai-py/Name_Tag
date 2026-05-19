import React, { useState } from "react";
import { Wand2, Loader, Download } from "lucide-react";
import { useGenerationStore } from "../../stores/generationStore";
import { generateLogo } from "../../lib/api";
import type { LogoDesignInfo } from "../../types";

interface LogoDesignSidebarProps {
  brandIndex: number;
  logoDesignInfo: LogoDesignInfo;
  isGenerating?: boolean;
  onImageGenerated?: (image: string, filename: string) => void;
}

const COLOR_NAME_MAP: Record<string, string> = {
  "흰색": "#FFFFFF",
  "검은색": "#000000",
  "빨강": "#FF0000",
  "초록": "#00AA00",
  "파랑": "#0000FF",
  "노랑": "#FFFF00",
  "주황": "#FFA500",
  "보라": "#800080",
  "핑크": "#FFC0CB",
  "회색": "#808080",
  "베이지": "#F5F5DC",
  "올리브": "#808000",
  "무색": "#FFFFFF",
};

const SYMBOL_TYPES = ["기하학적", "유기적", "추상적", "구체적"];
const FONT_WEIGHTS = ["Light", "Regular", "Medium", "Bold", "ExtraBold"];
const LOGO_TYPES = ["심볼만", "텍스트만", "심볼+텍스트 조합"];
const BACKGROUNDS = ["흰색", "투명", "그라디언트", "색상"];

export function LogoDesignSidebar({
  brandIndex,
  logoDesignInfo,
  isGenerating = false,
  onImageGenerated,
}: LogoDesignSidebarProps) {
  const { updateLogoDesign, editedLogoDesigns, setIsGeneratingLogo } =
    useGenerationStore();

  const editedValues = editedLogoDesigns[brandIndex] || {};

  const getDisplayValue = (field: keyof LogoDesignInfo) => {
    return editedValues[field] ?? logoDesignInfo[field] ?? "";
  };

  const handleInputChange = (field: keyof LogoDesignInfo, value: string) => {
    updateLogoDesign(brandIndex, field, value);
  };

  const handleGenerateLogo = async () => {
    setIsGeneratingLogo(true);
    try {
      const params = {
        brand_name: getDisplayValue("brand_name"),
        brand_topic: getDisplayValue("brand_topic"),
        core_value: getDisplayValue("core_value"),
        target_mood: getDisplayValue("target_mood"),
        symbol_type: getDisplayValue("symbol_type"),
        font_style: getDisplayValue("font_style"),
        font_reference: getDisplayValue("font_reference"),
        font_weight: getDisplayValue("font_weight"),
        brand_color: getDisplayValue("brand_color"),
        logo_type: getDisplayValue("logo_type"),
        background: getDisplayValue("background"),
      };

      const data = await generateLogo(params);
      const imageBase64 = `data:image/png;base64,${data.image}`;
      onImageGenerated?.(imageBase64, data.filename);
    } catch (error) {
      alert("로고 생성에 실패했습니다. 다시 시도해주세요.");
      console.error(error);
    } finally {
      setIsGeneratingLogo(false);
    }
  };

  return (
    <div className="h-full overflow-y-auto bg-light-bg dark:bg-dark-bg2 p-6 space-y-6 border-l border-light-border dark:border-dark-border">
      <div>
        <h3 className="text-xl font-bold text-light-text dark:text-dark-text mb-2">
          🎨 로고 디자인 편집
        </h3>
        <p className="text-xs text-light-text/60 dark:text-dark-text/60">
          모든 값을 수정할 수 있습니다
        </p>
      </div>

      {/* 텍스트 입력 필드 */}
      <div className="space-y-4">
        {[
          {
            key: "brand_name" as const,
            label: "브랜드 이름",
          },
          {
            key: "brand_topic" as const,
            label: "사업 주제",
          },
          {
            key: "core_value" as const,
            label: "핵심 가치",
          },
          {
            key: "target_mood" as const,
            label: "타겟 감성",
          },
          {
            key: "font_style" as const,
            label: "서체 스타일",
          },
          {
            key: "font_reference" as const,
            label: "서체 참고",
          },
        ].map(({ key, label }) => (
          <div key={key}>
            <label className="text-xs font-semibold text-light-text dark:text-dark-text block mb-2">
              {label}
            </label>
            <input
              type="text"
              value={getDisplayValue(key)}
              onChange={(e) => handleInputChange(key, e.target.value)}
              placeholder={logoDesignInfo[key] ?? ""}
              className="w-full px-3 py-2 text-sm rounded-lg bg-light-border dark:bg-dark-border border border-light-border/50 dark:border-dark-border/50 text-light-text dark:text-dark-text placeholder-light-text/40 dark:placeholder-dark-text/40 focus:outline-none focus:border-neon-cyan/50"
            />
          </div>
        ))}
      </div>

      {/* Select 필드 */}
      <div className="space-y-4 pt-4 border-t border-light-border/20 dark:border-dark-border/20">
        {[
          {
            key: "symbol_type" as const,
            label: "심볼 스타일",
            options: SYMBOL_TYPES,
          },
          {
            key: "font_weight" as const,
            label: "서체 굵기",
            options: FONT_WEIGHTS,
          },
          {
            key: "logo_type" as const,
            label: "로고 유형",
            options: LOGO_TYPES,
          },
          {
            key: "background" as const,
            label: "배경",
            options: BACKGROUNDS,
          },
        ].map(({ key, label, options }) => (
          <div key={key}>
            <label className="text-xs font-semibold text-light-text dark:text-dark-text block mb-2">
              {label}
            </label>
            <select
              value={getDisplayValue(key)}
              onChange={(e) => handleInputChange(key, e.target.value)}
              className="w-full px-3 py-2 text-sm rounded-lg bg-light-border dark:bg-dark-border border border-light-border/50 dark:border-dark-border/50 text-light-text dark:text-dark-text focus:outline-none focus:border-neon-cyan/50"
            >
              <option value="">선택해주세요</option>
              {options.map((opt) => (
                <option key={opt} value={opt}>
                  {opt}
                </option>
              ))}
            </select>
          </div>
        ))}
      </div>

      {/* 색상 선택 */}
      <div className="pt-4 border-t border-light-border/20 dark:border-dark-border/20">
        <label className="text-xs font-semibold text-light-text dark:text-dark-text block mb-2">
          브랜드 색상
        </label>
        <div className="flex gap-3">
          <input
            type="color"
            value={getDisplayValue("brand_color") || "#000000"}
            onChange={(e) => handleInputChange("brand_color", e.target.value)}
            className="w-16 h-10 rounded-lg cursor-pointer border border-light-border/50 dark:border-dark-border/50"
          />
          <div className="flex-1">
            <input
              type="text"
              value={getDisplayValue("brand_color")}
              onChange={(e) => handleInputChange("brand_color", e.target.value)}
              placeholder="#000000"
              className="w-full px-3 py-2 text-sm rounded-lg bg-light-border dark:bg-dark-border border border-light-border/50 dark:border-dark-border/50 text-light-text dark:text-dark-text font-mono"
            />
          </div>
        </div>
      </div>

      {/* 로고 생성 버튼 */}
      <button
        onClick={handleGenerateLogo}
        disabled={isGenerating}
        className={`w-full mt-8 py-3 rounded-lg font-semibold transition-all flex items-center justify-center gap-2 ${
          isGenerating
            ? "bg-neon-cyan/20 text-neon-cyan cursor-not-allowed"
            : "bg-gradient-neon text-white hover:shadow-glow-cyan"
        }`}
      >
        {isGenerating ? (
          <>
            <Loader className="w-4 h-4 animate-spin" />
            생성 중...
          </>
        ) : (
          <>
            <Wand2 className="w-4 h-4" />
            🎨 로고 이미지 생성
          </>
        )}
      </button>
    </div>
  );
}
