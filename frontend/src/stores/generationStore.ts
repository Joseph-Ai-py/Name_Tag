import { create } from "zustand";
import type { GenerationState } from "../types";

interface GenerationStore extends GenerationState {
  setStep: (step: GenerationState["currentStep"]) => void;
  setBusinessType: (value: string) => void;
  setKeywords: (value: string) => void;
  setSelectedVibes: (vibes: string[]) => void;
  toggleVibe: (vibe: string) => void;
  setTarget: (value: string) => void;
  setResult: (result: GenerationState["result"]) => void;
  setSelectedBrandIndex: (index: number) => void;
  setIsLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialState: GenerationState = {
  currentStep: 1,
  businessType: "",
  keywords: "",
  selectedVibes: [],
  target: "",
  result: null,
  selectedBrandIndex: 0,
  isLoading: false,
  error: null,
};

export const useGenerationStore = create<GenerationStore>((set) => ({
  ...initialState,

  setStep: (step) => set({ currentStep: step }),
  setBusinessType: (value) => set({ businessType: value }),
  setKeywords: (value) => set({ keywords: value }),

  setSelectedVibes: (vibes) => set({ selectedVibes: vibes }),
  toggleVibe: (vibe) =>
    set((state) => {
      if (state.selectedVibes.includes(vibe)) {
        return {
          selectedVibes: state.selectedVibes.filter((v) => v !== vibe),
        };
      } else if (state.selectedVibes.length < 4) {
        return { selectedVibes: [...state.selectedVibes, vibe] };
      }
      return state;
    }),

  setTarget: (value) => set({ target: value }),
  setResult: (result) => set({ result, currentStep: 5 }),
  setSelectedBrandIndex: (index) => set({ selectedBrandIndex: index }),
  setIsLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),

  reset: () => set(initialState),
}));
