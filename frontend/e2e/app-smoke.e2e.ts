import { test, expect } from "@playwright/test";

test("loads the home page and shows the generate flow", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByText("NameTag")).toBeVisible();
  await expect(page.getByText("브랜드 네임을 설계하는 AI 워크플로")).toBeVisible();
});

test("preview page exposes the PDF download action", async ({ page }) => {
  await page.goto("/preview");
  await expect(page.getByText("PDF 미리보기와 다운로드")).toBeVisible();
  await expect(page.getByRole("button", { name: "PDF 다운로드" })).toBeVisible();
});
