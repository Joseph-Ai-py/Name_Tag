import type { ReportV2Page } from "../../api/client";
import { ReportPageCards } from "./ReportPageCards";

export function SectionCResult({ pages, onRegenerate }: { pages: Record<string, ReportV2Page>; onRegenerate: (pageId: string) => void }) {
  return <ReportPageCards pages={pages} pageIds={["11", "12", "13", "14", "15", "16", "17", "23", "24"]} onRegenerate={onRegenerate} />;
}
