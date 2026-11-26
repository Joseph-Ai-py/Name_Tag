import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ReportPageCards } from "../ReportPageCards";

describe("Report page body emphasis", () => {
  it("renders **bold** keywords as strong text without showing markdown markers", () => {
    render(<ReportPageCards
      pages={{
        "02": {
          page_id: "02",
          title: "Brand Foundation",
          status: "complete",
          data: { brand_essence: "고객의 **시간 절약**을 돕습니다." },
          evidence_type: "ai_estimate",
          confidence: "medium",
        },
      }}
      pageIds={["02"]}
      onRegenerate={() => undefined}
    />);

    const emphasized = screen.getByText("시간 절약");
    expect(emphasized.tagName).toBe("STRONG");
    expect(screen.getByText(/고객의/).textContent).not.toContain("**");
  });
});
