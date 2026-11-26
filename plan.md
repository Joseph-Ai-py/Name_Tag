# NAME TAG V2 implementation status

## Connected flow

- The `/generate` frontend now opens the V2 report studio.
- `backend/prompts/nametag_prompts_v2.py` defines report pages 00–24, interview prompts, dependencies, output validation, scoring helpers, and regeneration invalidation.
- `/api/report-v2/meta`, `/plan`, `/interviews/{interview_id}`, and `/pages/{page_id}` expose that flow through FastAPI.
- Interview selections, free-text answers, completed pages, and brand inputs persist in browser local storage. Changes to brand inputs clear dependent generated state.
- `/api/pdf/generate-v2` renders completed pages with the A4/A3 page layouts defined in the report design.
- V1 endpoints remain registered for compatibility; the V2 frontend does not call them.

## Verification performed

- `python -m pytest backend/tests`: 20 passed.
- `npm test -- --run`: 2 passed.
- `npm run build`: passed.
- Python `compileall` for `backend/`: passed.

## Follow-up items from the design

- Connect a research provider for sourced external market and competitor facts. The report prompts mark missing sources and do not claim that live research is available.
- Improve the generic V2 PDF page renderer with dedicated visual components for charts, persona cards, canvases, and maps. The current renderer preserves validated page content and uses the required mixed paper sizes and orientations.
- Consider server-side report persistence and cross-device recovery; current report progress is browser-local.

See [the V2 integration notes](docs/REPORT_V2_INTEGRATION.md) and [the linked design document](https://app.notion.com/p/joyosep339/NAME-TAG-V1-V2-41892d3b1eb781d6ace7fa77290a5820) for the complete contract.
