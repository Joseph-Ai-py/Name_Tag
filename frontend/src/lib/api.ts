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

export async function generateBrand(params: BrandGenerateParams) {
  const response = await api.post("/api/v1/brand/generate", params);
  return response.data;
}

export default api;
