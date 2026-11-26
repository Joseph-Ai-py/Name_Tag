import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";

const api = vi.hoisted(() => ({
  getReportV2Meta: vi.fn(),
  getReportV2Plan: vi.fn(),
  generateReportV2Interview: vi.fn(),
  generateReportV2Page: vi.fn(),
  downloadReportV2Pdf: vi.fn(),
}));
vi.mock("../../api/client", () => api);

import { ReportV2Studio } from "../ReportV2Studio";
import { useBrandStore } from "../../store/brandStore";

describe("NAME TAG V2 page generation", () => {
  beforeEach(() => {
    localStorage.clear();
    useBrandStore.getState().reset();
    api.getReportV2Meta.mockResolvedValue({ page_order: ["00"], page_specs: { "00": { title: "Cover", deps: [] } }, interviews: {} });
    api.getReportV2Plan.mockResolvedValue({ ready_page_ids: ["00"], ready_interview_ids: [] });
    api.generateReportV2Page.mockResolvedValue({
      page: { page_id: "00", title: "Cover", status: "insufficient_data", data: { brand_name: "추가 정보 필요" }, confidence: "low" },
      invalidated_page_ids: [],
    });
  });

  it("generates a ready page and stores its V2 response", async () => {
    render(<ReportV2Studio />);
    fireEvent.click(await screen.findByRole("button", { name: /다음 추천: 00 Cover/ }));

    expect(await screen.findByText("00 · Cover")).toBeTruthy();
    expect(api.generateReportV2Page).toHaveBeenCalledWith("00", expect.objectContaining({ regenerate: false }));
    expect(useBrandStore.getState().reportV2.pages["00"].page_id).toBe("00");
    expect(localStorage.getItem("nametag_report_v2")).toBeNull();
  });

  it("keeps report data while the user edits a brand draft, then explains and applies the reset", async () => {
    useBrandStore.getState().updateReportV2((previous) => ({
      ...previous,
      brand: { ...previous.brand, brand_name: "기존 이름" },
      pages: { "00": { page_id: "00", title: "Cover", status: "complete", data: {}, confidence: "high" } },
      answers: { brand: [{ question_id: 1, question_text: "Q", selected_option: "A", user_input: "" }] },
    }));
    render(<ReportV2Studio />);
    fireEvent.change(screen.getAllByLabelText("브랜드명")[0], { target: { value: "새 이름" } });

    expect(useBrandStore.getState().reportV2.pages["00"]).toBeTruthy();
    expect(useBrandStore.getState().reportV2.brand.brand_name).toBe("기존 이름");
    expect(await screen.findByText(/기존 보고서 페이지와 인터뷰 답변이 초기화/)).toBeTruthy();

    fireEvent.click(screen.getAllByRole("button", { name: "변경 적용 후 다시 시작" })[0]);
    expect(useBrandStore.getState().reportV2.brand.brand_name).toBe("새 이름");
    expect(useBrandStore.getState().reportV2.pages).toEqual({});
    expect(useBrandStore.getState().reportV2.answers).toEqual({});
  });
});
