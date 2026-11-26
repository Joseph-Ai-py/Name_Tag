import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { CandidateSelector } from "../CandidateSelector";

const candidates = Array.from({ length: 4 }, (_, index) => ({
  id: index + 1,
  brand_name: `이름 ${index + 1}`,
  brand_name_en: `Name ${index + 1}`,
  name_meaning: `의미 ${index + 1}`,
  slogan: `슬로건 ${index + 1}`,
  story_summary: `스토리 ${index + 1}`,
  seed_color: `#00000${index}`,
  seed_color_reason: `컬러 이유 ${index + 1}`,
}));

describe("Brand candidate combination", () => {
  it("applies the chosen name, meaning, slogan, story, and color after all five choices", async () => {
    const onComplete = vi.fn();
    render(<CandidateSelector candidates={candidates} onComplete={onComplete} />);

    expect(screen.getByRole("status").textContent).toContain("0 / 5");
    fireEvent.click(screen.getByRole("button", { name: "이름 2 (Name 2)" }));
    fireEvent.click(screen.getByRole("button", { name: "의미 3" }));
    fireEvent.click(screen.getByRole("button", { name: "슬로건 1" }));
    fireEvent.click(screen.getByRole("button", { name: "스토리 4" }));
    fireEvent.click(screen.getByRole("button", { name: "#000003 · 컬러 이유 4" }));

    await waitFor(() => expect(onComplete).toHaveBeenCalledTimes(1));
    expect(onComplete).toHaveBeenCalledWith(expect.objectContaining({
      brand_name: "이름 2",
      name_meaning: "의미 3",
      slogan: "슬로건 1",
      story_summary: "스토리 4",
      seed_color: "#000003",
    }));
    expect(screen.getByRole("status").textContent).toContain("5 / 5");
  });
});
