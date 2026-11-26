// 💡 [수정 3] 이중 슬래시 방지: 환경변수 끝에 '/'가 있으면 제거
const BASE_URL = (import.meta.env.VITE_API_URL || "/api").replace(/\/$/, "");

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
  // 💡 endpoint가 '/'로 시작하지 않으면 '/'를 붙여 안전하게 결합
  const safeEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  apiLogger.info(`📤 POST ${safeEndpoint}`, body);

  try {
    const response = await fetch(`${BASE_URL}${safeEndpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const payload = await response.json().catch(() => ({}));
      apiLogger.error(`${safeEndpoint} - Status ${response.status}`, payload);
      
      // Show the server's validation detail together with status and endpoint.
      let detailMessage = "서버가 상세 오류 내용을 반환하지 않았습니다.";
      if (payload.detail) {
        if (typeof payload.detail === "string") {
          detailMessage = payload.detail;
        } else if (Array.isArray(payload.detail)) {
          detailMessage = payload.detail.map((err: any) => `${err.loc?.join(".") || "요청"}: ${err.msg || JSON.stringify(err)}`).join("\n");
        } else {
          detailMessage = JSON.stringify(payload.detail);
        }
      }
      throw new Error(`HTTP ${response.status} · ${safeEndpoint}\n${detailMessage}`);
    }

    const data = await response.json();
    apiLogger.timing(safeEndpoint, startTime);
    apiLogger.info(`✅ ${safeEndpoint} success`);
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

export const regenerateSectionOField = (brandData: unknown, context: unknown, target: string) => {
  apiLogger.info("🎯 Section O Re-generate field", { brandName: (brandData as any)?.brand_name, target });
  return apiPost("/section-o/re-generate", { brand_data: brandData, context, target });
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

export type ReportV2Page = {
  page_id: string;
  title: string;
  status: string;
  data: Record<string, unknown>;
  evidence_type?: string;
  source_ids?: string[];
  confidence?: string;
  validation_notes?: string[];
};

export const getReportV2Meta = () => fetch(`${BASE_URL}/report-v2/meta`).then(async (response) => {
  if (!response.ok) throw new Error("보고서 정보를 불러오지 못했습니다.");
  return response.json();
});

export const getReportV2Plan = (payload: unknown) => apiPost("/report-v2/plan", payload);

export const generateReportV2Interview = (interviewId: string, context: unknown) =>
  apiPost(`/report-v2/interviews/${encodeURIComponent(interviewId)}`, { context });

export const generateReportV2Page = (pageId: string, payload: unknown) =>
  apiPost(`/report-v2/pages/${encodeURIComponent(pageId)}`, payload);

export async function downloadReportV2Pdf(
  pages: Record<string, ReportV2Page>,
  brandName: string,
) {
  const blob = await createReportV2PdfBlob(pages, brandName);
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `nametag_${brandName}_report.pdf`;
  anchor.click();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export async function createReportV2PdfBlob(
  pages: Record<string, ReportV2Page>,
  brandName: string,
): Promise<Blob> {
  const response = await fetch(`${BASE_URL}/pdf/generate-v2`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pages, brand_name: brandName }),
  });
  if (!response.ok) throw new Error((await response.text()) || "PDF 생성에 실패했습니다.");
  return response.blob();
}

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
    document.body.appendChild(anchor); // DOM에 붙여야 확실하게 작동하는 브라우저들 대비
    anchor.click();
    document.body.removeChild(anchor);
    
    // 💡 [수정 2] 다운로드가 시작되기도 전에 메모리에서 삭제되어버리는 버그 방지 (1초 대기 후 해제)
    setTimeout(() => {
      URL.revokeObjectURL(url);
    }, 1000);

    apiLogger.info(`💾 PDF 다운로드 완료: ${anchor.download}`);
  } catch (error) {
    apiLogger.error("PDF 생성/다운로드 중 오류", error);
    throw error;
  }
}
