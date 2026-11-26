import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { ProgressBar } from "../ProgressBar";

const steps = [
  { label: "01", title: "브랜드 기초" },
  { label: "02", title: "사업·포지셔닝" },
  { label: "03", title: "고객·가치" },
  { label: "04", title: "시장·사업 모델" },
  { label: "05", title: "시각 정체성" },
  { label: "06", title: "검토·PDF" },
];

describe("Report progress navigation", () => {
  it("moves to the step the user selects and exposes saved page counts", () => {
    const onStepChange = vi.fn();
    render(<ProgressBar currentStep={0} steps={steps} stepDetails={["1페이지 저장"]} onStepChange={onStepChange} />);

    const stepButton = screen.getByRole("button", { name: "02 사업·포지셔닝 단계로 이동" });
    fireEvent.click(stepButton);

    expect(onStepChange).toHaveBeenCalledWith(1);
    expect(screen.getByText("1페이지 저장")).toBeTruthy();
    expect(screen.getByRole("navigation", { name: "보고서 진행 단계" })).toBeTruthy();
  });
});
