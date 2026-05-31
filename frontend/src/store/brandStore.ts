import { create } from "zustand";

export type BrandData = {
  business_type: string;
  vibes: string[];
  target: string;
  keywords: string;
};

export type BrandInfo = {
  brand_name: string;
  brand_name_en: string;
  name_meaning: string;
  slogan: string;
  story_summary: string;
  seed_color: string;
  seed_color_reason: string;
};

export type BrandStore = {
  brandData: BrandData | null;
  interviewDataO: string;
  brandInfo: BrandInfo | null;
  interviewDataA: string;
  dataA: Record<string, any> | null;
  interviewDataB: string;
  dataB: Record<string, any> | null;
  interviewDataC: string;
  dataC: Record<string, any> | null;
  interviewDataDE: string;
  dataDE: Record<string, any> | null;
  currentStep: 0 | 1 | 2 | 3 | 4 | 5;
  isLoading: boolean;
  error: string | null;
  setBrandData: (brandData: BrandData) => void;
  setInterviewDataO: (value: string) => void;
  setBrandInfo: (value: BrandInfo) => void;
  setInterviewDataA: (value: string) => void;
  setDataA: (value: Record<string, any>) => void;
  setInterviewDataB: (value: string) => void;
  setDataB: (value: Record<string, any>) => void;
  setInterviewDataC: (value: string) => void;
  setDataC: (value: Record<string, any>) => void;
  setInterviewDataDE: (value: string) => void;
  setDataDE: (value: Record<string, any>) => void;
  setCurrentStep: (value: 0 | 1 | 2 | 3 | 4 | 5) => void;
  setIsLoading: (value: boolean) => void;
  setError: (value: string | null) => void;
  reset: () => void;
};

const initialState = {
  brandData: null,
  interviewDataO: "",
  brandInfo: null,
  interviewDataA: "",
  dataA: null,
  interviewDataB: "",
  dataB: null,
  interviewDataC: "",
  dataC: null,
  interviewDataDE: "",
  dataDE: null,
  currentStep: 0 as 0 | 1 | 2 | 3 | 4 | 5,
  isLoading: false,
  error: null,
};

export const useBrandStore = create<BrandStore>((set) => ({
  ...initialState,
  setBrandData: (brandData) => set({ brandData }),
  setInterviewDataO: (value) => set({ interviewDataO: value }),
  setBrandInfo: (value) => set({ brandInfo: value }),
  setInterviewDataA: (value) => set({ interviewDataA: value }),
  setDataA: (value) => set({ dataA: value }),
  setInterviewDataB: (value) => set({ interviewDataB: value }),
  setDataB: (value) => set({ dataB: value }),
  setInterviewDataC: (value) => set({ interviewDataC: value }),
  setDataC: (value) => set({ dataC: value }),
  setInterviewDataDE: (value) => set({ interviewDataDE: value }),
  setDataDE: (value) => set({ dataDE: value }),
  setCurrentStep: (value) => set({ currentStep: value }),
  setIsLoading: (value) => set({ isLoading: value }),
  setError: (value) => set({ error: value }),
  reset: () => set({ ...initialState }),
}));
