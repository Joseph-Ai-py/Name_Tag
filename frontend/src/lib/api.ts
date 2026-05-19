/// <reference types="vite/client" />
import axios, { AxiosInstance } from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface BrandGenerateParams {
  business_type: string;
  vibes: string[];
  target: string;
  keywords: string;
}

export interface LogoGenerateParams {
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

export interface CharacterGenerateParams {
  character_name: string;
  character_concept: string;
  character_visual: string;
  vibes: string[];
  character_style?: string;
  character_age_feel?: string;
  brand_name?: string;
  brand_topic?: string;
  core_value?: string;
}

export async function generateBrand(params: BrandGenerateParams) {
  const response = await api.post("/api/v1/brand/generate", params);
  return response.data;
}

export async function generateLogo(params: LogoGenerateParams) {
  const response = await api.post("/api/v1/brand/logo-custom", params);
  return response.data;
}

export async function generateCharacter(params: CharacterGenerateParams) {
  const response = await api.post("/api/v1/brand/character", params);
  return response.data;
}

export default api;
