import type { ReportV2Page } from "../../api/client";
import { ReportPageCards } from "./ReportPageCards";

export function SectionBResult({ pages, onRegenerate }: { pages: Record<string, ReportV2Page>; onRegenerate: (pageId: string) => void }) {
  return <ReportPageCards pages={pages} pageIds={["07", "08", "09", "10", "18"]} onRegenerate={onRegenerate} />;
}
