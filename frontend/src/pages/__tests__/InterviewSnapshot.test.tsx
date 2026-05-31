import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, fireEvent, screen } from "@testing-library/react";
import { InterviewCard } from "../..//components/InterviewCard";

const questions = [
  { question_text: "Q1", options: ["1. A", "2. B"] },
  { question_text: "Q2", options: ["1. X", "2. Y"] },
];

describe("InterviewCard snapshot user_inputs", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("saves and restores user_inputs in snapshot", async () => {
    const onComplete = vi.fn();
    render(<InterviewCard questions={questions} reasoning={"r"} onComplete={onComplete} sectionKey={"TEST"} />);

    // Click direct input
    const directBtn = screen.getByText("직접 입력 (내 답변 입력)");
    fireEvent.click(directBtn);
    const textarea = screen.getByPlaceholderText("직접 입력할 답변을 작성하세요");
    fireEvent.change(textarea, { target: { value: "my answer" } });
    const saveBtn = screen.getByText("저장");
    fireEvent.click(saveBtn);

    // Move next
    const nextBtn = screen.getByText("다음");
    fireEvent.click(nextBtn);

    // Simulate remount by rendering anew
    render(<InterviewCard questions={questions} reasoning={"r"} onComplete={onComplete} sectionKey={"TEST"} />);

    // The current snapshot should restore answer
    expect(localStorage.getItem("nametag_interviewSnapshots")).toBeTruthy();
    const stored = JSON.parse(localStorage.getItem("nametag_interviewSnapshots") || "{}");
    expect(stored.TEST.user_inputs).toBeTruthy();
    expect(stored.TEST.user_inputs["0"]).toBe("my answer");
  });
});
