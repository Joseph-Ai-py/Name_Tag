// Type definitions for NameTag frontend.

export interface BrandOption {
  name: string;
  meaning: string;
  story: string;
  slogan: string;
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
}
