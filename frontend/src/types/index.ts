// Type definitions for NameTag frontend.

export interface LogoDesignInfo {
  brand_name: string;
  brand_topic: string;
  core_value: string;
  target_mood: string;
  symbol_type: string;
  font_style: string;
  font_reference: string;
  font_weight: string;
  brand_color: string;
  logo_type: string;
  background: string;
}

export interface BrandOption {
  name: string;
  meaning: string;
  story: string;
  slogan: string;
  typography: Typography;
  character: Character;
  logo_design: LogoDesignInfo;
}

export interface Typography {
  korean: string;
  english: string;
  reason: string;
}

export interface Character {
  name: string;
  concept: string;
  personality: string;
  visual: string;
}

export interface BrandResult {
  brands: BrandOption[];
  typography: Typography;
  character: Character;
}

export interface ImageGeneration {
  logoImage: string | null;
  characterImage: string | null;
  isGeneratingLogo: boolean;
  isGeneratingCharacter: boolean;
}

export interface GenerationState {
  currentStep: 1 | 2 | 3 | 4 | 5;
  businessType: string;
  keywords: string;
  selectedVibes: string[];
  target: string;
  result: BrandResult | null;
  selectedBrandIndex: number;
  isLoading: boolean;
  error: string | null;
  images: ImageGeneration;
}
