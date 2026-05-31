const BASE_URL = import.meta.env.VITE_API_URL || "/api";

// 디버깅 로거
export const apiLogger = {
  info: (message: string, data?: unknown) => {
    console.log(`[NameTag API] ${message}`, data || "");
  },
  error: (message: string, error?: unknown) => {
    console.error(`[NameTag API ERROR] ${message}`, error || "");
  },
  timing: (endpoint: string, startTime: number) => {
    const duration = performance.now() - startTime;
    console.log(`[NameTag API] ${endpoint} took ${duration.toFixed(2)}ms`);
  },
};

async function apiPost(endpoint: string, body: unknown) {
  const startTime = performance.now();
  apiLogger.info(`📤 POST ${endpoint}`, body);

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      apiLogger.error(`${endpoint} - Status ${response.status}`, payload);
      throw new Error(payload.detail || "서버 오류가 발생했습니다.");
    }

    const data = await response.json();
    apiLogger.timing(endpoint, startTime);
    apiLogger.info(`✅ ${endpoint} success`);
    return data;
  } catch (error) {
    apiLogger.error(`${endpoint} - Network or parse error`, error);
    throw error;
  }
}

export const getOInterview = (brandData: unknown) => {
  apiLogger.info("🎯 Section O Interview 시작", { business_type: (brandData as any).business_type, target: (brandData as any).target, vibes: (brandData as any).vibes?.length ?? 0 });
  return apiPost("/section-o/interview", { brand_data: brandData });
};

export const getOCandidates = (brandData: unknown, interviewData: string) => {
  apiLogger.info("🎯 Section O Candidates 생성", { interviewLength: interviewData.length });
  return apiPost("/section-o/candidates", { brand_data: brandData, interview_data: interviewData });
};

export const getAInterview = (brandInfo: unknown) => {
  apiLogger.info("🎯 Section A Interview 시작", { brandName: (brandInfo as any)?.brand_name });
  return apiPost("/section-a/interview", { brand_info: brandInfo });
};

export const generateSectionA = (brandInfo: unknown, interviewDataA: string) => {
  apiLogger.info("🎯 Section A 데이터 생성", { brandName: (brandInfo as any)?.brand_name, interviewLength: interviewDataA.length });
  return apiPost("/section-a/generate", { brand_info: brandInfo, interview_data_a: interviewDataA });
};

export const regenerateSectionAField = (brandInfo: unknown, context: unknown, target: string) => {
  apiLogger.info("🎯 Section A Re-generate field", { brandName: (brandInfo as any)?.brand_name, target });
  return apiPost("/section-a/re-generate", { brand_info: brandInfo, context, target });
};

export const regenerateSectionBField = (brandInfo: unknown, context: unknown, target: string) => {
  apiLogger.info("🎯 Section B Re-generate field", { brandName: (brandInfo as any)?.brand_name, target });
  return apiPost("/section-b/re-generate", { brand_info: brandInfo, context, target });
};

export const regenerateSectionCField = (brandInfo: unknown, context: unknown, target: string) => {
  apiLogger.info("🎯 Section C Re-generate field", { brandName: (brandInfo as any)?.brand_name, target });
  return apiPost("/section-c/re-generate", { brand_info: brandInfo, context, target });
};

export const regenerateSectionDEField = (brandInfo: unknown, context: unknown, target: string) => {
  apiLogger.info("🎯 Section DE Re-generate field", { brandName: (brandInfo as any)?.brand_name, target });
  return apiPost("/section-de/re-generate", { brand_info: brandInfo, context, target });
};

export const regenerateSectionOField = (brandInfo: unknown, context: unknown, target: string) => {
  apiLogger.info("🎯 Section O Re-generate field", { brandName: (brandInfo as any)?.brand_name, target });
  return apiPost("/section-o/re-generate", { brand_data: brandInfo, context, target });
};

export const getBInterview = (brandInfo: unknown) => {
  apiLogger.info("🎯 Section B Interview 시작", { brandName: (brandInfo as any)?.brand_name });
  return apiPost("/section-b/interview", { brand_info: brandInfo });
};

export const generateSectionB = (brandInfo: unknown, interviewDataA: string, interviewDataB: string) => {
  apiLogger.info("🎯 Section B 데이터 생성", { brandName: (brandInfo as any)?.brand_name, interviewA: interviewDataA.length, interviewB: interviewDataB.length });
  return apiPost("/section-b/generate", {
    brand_info: brandInfo,
    interview_data_a: interviewDataA,
    interview_data_b: interviewDataB,
  });
};

export const getCInterview = (brandInfo: unknown) => {
  apiLogger.info("🎯 Section C Interview 시작", { brandName: (brandInfo as any)?.brand_name });
  return apiPost("/section-c/interview", { brand_info: brandInfo });
};

export const generateSectionC = (brandInfo: unknown, interviewDataA: string, interviewDataB: string, interviewDataC: string) => {
  apiLogger.info("🎯 Section C 데이터 생성", { brandName: (brandInfo as any)?.brand_name, interviewA: interviewDataA.length, interviewB: interviewDataB.length, interviewC: interviewDataC.length });
  return apiPost("/section-c/generate", {
    brand_info: brandInfo,
    interview_data_a: interviewDataA,
    interview_data_b: interviewDataB,
    interview_data_c: interviewDataC,
  });
};

export const getDEInterview = (brandInfo: unknown, interviewDataC: string) => {
  apiLogger.info("🎯 Section DE Interview 시작", { brandName: (brandInfo as any)?.brand_name, interviewC: interviewDataC.length });
  return apiPost("/section-de/interview", { brand_info: brandInfo, interview_data_c: interviewDataC });
};

export const generateSectionDE = (
  brandInfo: unknown,
  dataC: unknown,
  interviewDataA: string,
  interviewDataB: string,
  interviewDataC: string,
  interviewDataDE: string,
) => {
  apiLogger.info("🎯 Section DE 데이터 생성 (이미지 포함)", { 
    brandName: (brandInfo as any)?.brand_name,
    interviewA: interviewDataA.length, 
    interviewB: interviewDataB.length, 
    interviewC: interviewDataC.length,
    interviewDE: interviewDataDE.length,
  });
  return apiPost("/section-de/generate", {
    brand_info: brandInfo,
    data_c: dataC,
    interview_data_a: interviewDataA,
    interview_data_b: interviewDataB,
    interview_data_c: interviewDataC,
    interview_data_de: interviewDataDE,
  });
};

export const generateSectionDELogo = (
  brandInfo: unknown,
  dataC: unknown,
  interviewDataA: string,
  interviewDataB: string,
  interviewDataC: string,
  interviewDataDE: string,
) => {
  apiLogger.info("🎯 Section DE 로고 생성 (단독)", { brandName: (brandInfo as any)?.brand_name });
  return apiPost("/section-de/generate-logo", {
    brand_info: brandInfo,
    data_c: dataC,
    interview_data_a: interviewDataA,
    interview_data_b: interviewDataB,
    interview_data_c: interviewDataC,
    interview_data_de: interviewDataDE,
  });
};

export const generateSectionDECharacter = (
  brandInfo: unknown,
  dataC: unknown,
  interviewDataA: string,
  interviewDataB: string,
  interviewDataC: string,
  interviewDataDE: string,
) => {
  apiLogger.info("🎯 Section DE 캐릭터 생성 (단독)", { brandName: (brandInfo as any)?.brand_name });
  return apiPost("/section-de/generate-character", {
    brand_info: brandInfo,
    data_c: dataC,
    interview_data_a: interviewDataA,
    interview_data_b: interviewDataB,
    interview_data_c: interviewDataC,
    interview_data_de: interviewDataDE,
  });
};

export async function generatePDF(brandInfo: any, dataA: any, dataB: any, dataC: any, dataDE: any) {
  const startTime = performance.now();
  apiLogger.info("📄 PDF 생성 시작", {
    brandName: brandInfo.brand_name,
    hasA: Boolean(dataA),
    hasB: Boolean(dataB),
    hasC: Boolean(dataC),
    hasDE: Boolean(dataDE),
    logoPath: dataDE?.logo_path,
    charPath: dataDE?.char_path,
  });

  try {
    const response = await fetch(`${BASE_URL}/pdf/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        brand_info: brandInfo,
        data_a: dataA,
        data_b: dataB,
        data_c: dataC,
        data_de: dataDE,
      }),
    });

    if (!response.ok) {
      apiLogger.error(`PDF 생성 실패 - Status ${response.status}`, await response.text());
      throw new Error("PDF 생성 실패");
    }

    const blob = await response.blob();
    apiLogger.info(`✅ PDF 생성 완료 (${(blob.size / 1024).toFixed(2)}KB)`, blob.type);
    apiLogger.timing("/pdf/generate", startTime);

    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `nametag_${brandInfo.brand_name}_guideline.pdf`;
    anchor.click();
    URL.revokeObjectURL(url);
    
    apiLogger.info(`💾 PDF 다운로드 완료: ${anchor.download}`);
  } catch (error) {
    apiLogger.error("PDF 생성/다운로드 중 오류", error);
    throw error;
  }
}
