import { beforeEach, describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";

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

const interview = {
  required_question_count: 5,
  reasoning: "필요한 브랜드 정보를 묻습니다.",
  questions: Array.from({ length: 5 }, (_, index) => ({
    question_id: index + 1,
    question_text: `브랜드 질문 ${index + 1}`,
    options: ["A 선택", "B 선택", "C 선택", "D 선택"],
  })),
};

describe("NAME TAG V2 interview flow", () => {
  beforeEach(() => {
    localStorage.clear();
    useBrandStore.getState().reset();
    api.getReportV2Meta.mockResolvedValue({ page_order: ["00"], page_specs: { "00": { title: "Cover", deps: [] } }, interviews: { brand: { title: "Initial Brand Interview" } } });
    api.getReportV2Plan.mockResolvedValue({ ready_page_ids: ["00"], ready_interview_ids: ["brand"] });
    api.generateReportV2Interview.mockResolvedValue(interview);
  });

  it("generates a V2 interview with five questions and collects free text", async () => {
    render(<ReportV2Studio />);
    const generateButton = await screen.findByRole("button", { name: "질문 생성" });
    await waitFor(() => expect(generateButton.hasAttribute("disabled")).toBe(false));
    fireEvent.click(generateButton);

    expect(await screen.findByText(/브랜드 질문 1/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "다음" }).hasAttribute("disabled")).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "직접 입력" }));
    fireEvent.change(screen.getByPlaceholderText("직접 입력할 답변을 작성하세요"), { target: { value: "우리 브랜드의 방향" } });
    fireEvent.click(screen.getByRole("button", { name: "저장" }));
    fireEvent.click(screen.getByRole("button", { name: "다음" }));
    for (let index = 1; index < 5; index += 1) {
      fireEvent.click(screen.getAllByRole("button", { name: "A 선택" })[0]);
      fireEvent.click(screen.getByRole("button", { name: index === 4 ? "인터뷰 완료" : "다음" }));
    }

    await waitFor(() => expect(useBrandStore.getState().reportV2.answers.brand).toHaveLength(5));
    expect(useBrandStore.getState().reportV2.answers.brand[0].user_input).toBe("우리 브랜드의 방향");
    expect(localStorage.getItem("nametag_report_v2")).toBeNull();
  });
});
