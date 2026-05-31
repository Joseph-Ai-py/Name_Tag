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
  // interview snapshots: key by section (e.g. 'O','A')
  interviewSnapshots: Record<string, { answers?: string[]; currentIndex?: number; user_inputs?: Record<string, string> }>;
  saveInterviewSnapshot: (section: string, snapshot: { answers?: string[]; currentIndex?: number; user_inputs?: Record<string, string> }) => void;
  getInterviewSnapshot: (section: string) => { answers?: string[]; currentIndex?: number; user_inputs?: Record<string, string> } | undefined;
  clearInterviewSnapshot: (section: string) => void;
  appliedSelections: Record<string, Record<string, string>>;
  setAppliedSelection: (section: string, field: string, value: string) => void;
  getAppliedSelection: (section: string, field: string) => string | undefined;
  clearAppliedSelections: (section?: string) => void;
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
  appliedSelections: {},
};

export const useBrandStore = create<BrandStore>((set, get) => ({
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
  interviewSnapshots: (typeof window !== "undefined" && localStorage.getItem("nametag_interviewSnapshots"))
    ? JSON.parse(localStorage.getItem("nametag_interviewSnapshots") || "{}")
    : {},
  appliedSelections: (typeof window !== "undefined" && localStorage.getItem("nametag_appliedSelections"))
    ? JSON.parse(localStorage.getItem("nametag_appliedSelections") || "{}")
    : {},
  setAppliedSelection: (section, field, value) =>
    set((state) => {
      const copy = { ...(state.appliedSelections || {}) };
      copy[section] = { ...(copy[section] || {}), [field]: value };
      try {
        if (typeof window !== "undefined") {
          localStorage.setItem("nametag_appliedSelections", JSON.stringify(copy));
        }
      } catch (e) {}
      return { appliedSelections: copy };
    }),
  getAppliedSelection: (section, field) => {
    const s = get().appliedSelections?.[section];
    return s ? s[field] : undefined;
  },
  clearAppliedSelections: (section) => set((state) => {
    const copy = { ...(state.appliedSelections || {}) };
    if (section) {
      delete copy[section];
    } else {
      Object.keys(copy).forEach((k) => delete copy[k]);
    }
    try {
      if (typeof window !== "undefined") {
        localStorage.setItem("nametag_appliedSelections", JSON.stringify(copy));
      }
    } catch (e) {}
    return { appliedSelections: copy };
  }),
  saveInterviewSnapshot: (section, snapshot) =>
    set((state) => {
      const copy = { ...(state.interviewSnapshots || {}) };
      copy[section] = { ...(copy[section] || {}), ...snapshot };
      try {
        if (typeof window !== "undefined") {
          localStorage.setItem("nametag_interviewSnapshots", JSON.stringify(copy));
        }
      } catch (e) {}
      return { interviewSnapshots: copy };
    }),
  getInterviewSnapshot: (section) => {
    const s = get().interviewSnapshots?.[section];
    return s;
  },
  clearInterviewSnapshot: (section) => set((state) => {
    const copy = { ...(state.interviewSnapshots || {}) };
    delete copy[section];
    return { interviewSnapshots: copy };
  }),
}));
