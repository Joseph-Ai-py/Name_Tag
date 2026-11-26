import type { ReportV2Page } from "../../api/client";
import { ReportPageCards } from "./ReportPageCards";

export function SectionDEResult({ pages, onRegenerate }: { pages: Record<string, ReportV2Page>; onRegenerate: (pageId: string) => void }) {
  return <ReportPageCards pages={pages} pageIds={["19", "20", "21", "22"]} onRegenerate={onRegenerate} />;
}
