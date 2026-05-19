import React, { useState } from "react";

interface ImageGenerationFormProps {
  brandData?: {
    brandName?: string;
    businessType?: string;
    vibes?: string[];
    target?: string;
    keywords?: string;
  };
  onGenerate?: (formData: any) => void;
}

export function ImageGenerationForm({ brandData, onGenerate }: ImageGenerationFormProps) {
  const [formData, setFormData] = useState({
    brand_name: brandData?.brandName || "",
    brand_topic: "",
    core_value: "",
    vibes: brandData?.vibes || [],
    symbol_type: "",
    character_concept: "",
    character_personality: "",
    character_style: "",
  });

  const symbolTypeOptions = ["기하학적", "유기적", "미니멀", "레터마크", "아이콘형"];
  const characterStyleOptions = ["플랫 일러스트", "손그림 느낌", "2.5D", "3D 렌더", "픽셀아트"];
  const characterAgeOptions = ["어린이", "청소년", "청년", "중장년", "나이 초월"];

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleMultiSelect = (name: string, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [name]: prev[name as keyof typeof prev].includes(value)
        ? (prev[name as keyof typeof prev] as string[]).filter((v) => v !== value)
        : [...(prev[name as keyof typeof prev] as string[]), value],
    }));
  };

  return (
    <div className="space-y-8">
      {/* 로고 생성 섹션 */}
      <div className="bg-light-bg dark:bg-dark-bg2 rounded-xl p-6 border border-light-border dark:border-dark-border">
        <h3 className="text-2xl font-bold mb-4 text-light-text dark:text-dark-text">🎨 로고 생성</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-semibold mb-2 text-light-text dark:text-dark-text">
              브랜드명 (선택)
            </label>
            <input
              type="text"
              name="brand_name"
              value={formData.brand_name}
              onChange={handleInputChange}
              placeholder="예: Brewly"
              className="w-full px-4 py-2 rounded-lg bg-white dark:bg-dark-bg text-light-text dark:text-dark-text border border-light-border dark:border-dark-border focus:outline-none focus:ring-2 focus:ring-neon-blue"
            />
            <p className="text-xs mt-1 text-light-text/60 dark:text-dark-text/60">비워두면 AI가 추천합니다</p>
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-light-text dark:text-dark-text">
              업종/주제 (선택)
            </label>
            <input
              type="text"
              name="brand_topic"
              value={formData.brand_topic}
              onChange={handleInputChange}
              placeholder="예: 수제 커피 구독 서비스"
              className="w-full px-4 py-2 rounded-lg bg-white dark:bg-dark-bg text-light-text dark:text-dark-text border border-light-border dark:border-dark-border focus:outline-none focus:ring-2 focus:ring-neon-blue"
            />
            <p className="text-xs mt-1 text-light-text/60 dark:text-dark-text/60">비워두면 AI가 추론합니다</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-semibold mb-2 text-light-text dark:text-dark-text">
              핵심 가치 (선택)
            </label>
            <input
              type="text"
              name="core_value"
              value={formData.core_value}
              onChange={handleInputChange}
              placeholder="예: 신뢰, 정밀함"
              className="w-full px-4 py-2 rounded-lg bg-white dark:bg-dark-bg text-light-text dark:text-dark-text border border-light-border dark:border-dark-border focus:outline-none focus:ring-2 focus:ring-neon-blue"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-light-text dark:text-dark-text">
              심볼 스타일 (선택)
            </label>
            <select
              name="symbol_type"
              value={formData.symbol_type}
              onChange={handleInputChange}
              className="w-full px-4 py-2 rounded-lg bg-white dark:bg-dark-bg text-light-text dark:text-dark-text border border-light-border dark:border-dark-border focus:outline-none focus:ring-2 focus:ring-neon-blue"
            >
              <option value="">AI가 선택</option>
              {symbolTypeOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* 캐릭터 생성 섹션 */}
      <div className="bg-light-bg dark:bg-dark-bg2 rounded-xl p-6 border border-light-border dark:border-dark-border">
        <h3 className="text-2xl font-bold mb-4 text-light-text dark:text-dark-text">🎭 캐릭터 생성</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-semibold mb-2 text-light-text dark:text-dark-text">
              캐릭터 컨셉 (선택)
            </label>
            <input
              type="text"
              name="character_concept"
              value={formData.character_concept}
              onChange={handleInputChange}
              placeholder="예: 커피 원두의 의인화"
              className="w-full px-4 py-2 rounded-lg bg-white dark:bg-dark-bg text-light-text dark:text-dark-text border border-light-border dark:border-dark-border focus:outline-none focus:ring-2 focus:ring-neon-blue"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold mb-2 text-light-text dark:text-dark-text">
              성격 특징 (선택)
            </label>
            <input
              type="text"
              name="character_personality"
              value={formData.character_personality}
              onChange={handleInputChange}
              placeholder="예: 친근함, 따뜻함, 신뢰"
              className="w-full px-4 py-2 rounded-lg bg-white dark:bg-dark-bg text-light-text dark:text-dark-text border border-light-border dark:border-dark-border focus:outline-none focus:ring-2 focus:ring-neon-blue"
            />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold mb-2 text-light-text dark:text-dark-text">
              일러스트 스타일 (선택)
            </label>
            <select
              name="character_style"
              value={formData.character_style}
              onChange={handleInputChange}
              className="w-full px-4 py-2 rounded-lg bg-white dark:bg-dark-bg text-light-text dark:text-dark-text border border-light-border dark:border-dark-border focus:outline-none focus:ring-2 focus:ring-neon-blue"
            >
              <option value="">AI가 선택</option>
              {characterStyleOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* 도움말 */}
      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
        <p className="text-sm text-light-text dark:text-dark-text">
          💡 <strong>선택적 입력:</strong> 빈칸으로 두면 이전 단계에서 입력한 정보를 기반으로 AI가 자동으로 추천합니다.
        </p>
      </div>
    </div>
  );
}
