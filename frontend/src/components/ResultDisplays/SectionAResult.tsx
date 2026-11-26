import type { ReportV2Page } from "../../api/client";
import { ReportPageCards } from "./ReportPageCards";

export function SectionAResult({ pages, onRegenerate }: { pages: Record<string, ReportV2Page>; onRegenerate: (pageId: string) => void }) {
  return <ReportPageCards pages={pages} pageIds={["05", "06"]} onRegenerate={onRegenerate} />;
}
