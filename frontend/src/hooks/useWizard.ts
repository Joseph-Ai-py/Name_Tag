import React from "react";
import { useGenerationStore } from "../stores/generationStore";

export function useWizard() {
  const state = useGenerationStore();
  
  const canProceedStep1 = state.businessType.trim().length > 2;
  const canProceedStep2 = state.selectedVibes.length >= 1 && state.selectedVibes.length <= 4;
  const canProceedStep3 = state.target.trim().length > 2;

  return {
    ...state,
    canProceedStep1,
    canProceedStep2,
    canProceedStep3,
  };
}
