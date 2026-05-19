import { create } from "zustand";
import type { GenerationState, ImageGeneration, LogoDesignInfo } from "../types";

interface GenerationStore extends GenerationState {
  editedLogoDesigns: Record<number, Partial<LogoDesignInfo>>;
  generatedLogos: Record<number, { image: string; filename: string }>;
  
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
  setLogoImage: (image: string | null) => void;
  setCharacterImage: (image: string | null) => void;
  setIsGeneratingLogo: (loading: boolean) => void;
  setIsGeneratingCharacter: (loading: boolean) => void;
  updateLogoDesign: (brandIndex: number, field: string, value: any) => void;
  setGeneratedLogo: (brandIndex: number, image: string, filename: string) => void;
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
  images: {
    logoImage: null,
    characterImage: null,
    isGeneratingLogo: false,
    isGeneratingCharacter: false,
  },
};

export const useGenerationStore = create<GenerationStore>((set) => ({
  ...initialState,
  editedLogoDesigns: {},
  generatedLogos: {},

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

  setLogoImage: (image) =>
    set((state) => ({
      images: { ...state.images, logoImage: image },
    })),

  setCharacterImage: (image) =>
    set((state) => ({
      images: { ...state.images, characterImage: image },
    })),

  setIsGeneratingLogo: (loading) =>
    set((state) => ({
      images: { ...state.images, isGeneratingLogo: loading },
    })),

  setIsGeneratingCharacter: (loading) =>
    set((state) => ({
      images: { ...state.images, isGeneratingCharacter: loading },
    })),

  updateLogoDesign: (brandIndex, field, value) =>
    set((state) => ({
      editedLogoDesigns: {
        ...state.editedLogoDesigns,
        [brandIndex]: {
          ...(state.editedLogoDesigns[brandIndex] || {}),
          [field]: value,
        },
      },
    })),

  setGeneratedLogo: (brandIndex, image, filename) =>
    set((state) => ({
      generatedLogos: {
        ...state.generatedLogos,
        [brandIndex]: { image, filename },
      },
    })),

  reset: () => set({ ...initialState, editedLogoDesigns: {}, generatedLogos: {} }),
}));
