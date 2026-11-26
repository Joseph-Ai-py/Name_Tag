# NAME TAG V2 integration

## Source of the report contract

`backend/prompts/nametag_prompts_v2.py` owns the V2 page IDs, page dependencies, interview definitions, generation prompts, validation, scoring helpers, and regeneration invalidation rules. The Notion page lists IDs `00` through `24`; the application therefore exposes all 25 listed entries. Pages 17 (Lean Canvas) and 21 (Character Identity) are conditional.

The prompt module's interview sample and validator both use 5–10 questions, exactly four options per question, unique integer IDs, and a matching `required_question_count`.

## API flow

1. `GET /api/report-v2/meta` returns page order, page contracts, interview definitions, and required interview mapping.
2. `POST /api/report-v2/plan` accepts `{ "context": { "brand": {}, "pages": {}, "interview_answers": {} }, "skipped_page_ids": [], "conditional_decisions": { "17": false, "21": false } }` and returns ready page and interview IDs.
3. `POST /api/report-v2/interviews/{interview_id}` accepts `{ "context": ... }` and returns the validated interview.
4. The browser records selected options and optional free-text answers by interview ID.
5. `POST /api/report-v2/pages/{page_id}` accepts `{ "context": ..., "regenerate": false, "conditional_decisions": ... }`. The response contains the validated page and IDs invalidated by regeneration.
6. `POST /api/pdf/generate-v2` accepts `{ "pages": { "00": ... }, "brand_name": "...", "page_layouts": [] }` and returns a PDF. The renderer supplies the design defaults when no page-specific overrides are provided.

The API is stateless for report progress. The browser persists brand input, interviews, answers, and completed pages in `localStorage`; every generation call sends the current state. Changing brand inputs clears dependent local results. Changing saved interview answers clears generated pages so stale analysis cannot be exported accidentally.

## PDF page layout defaults

- A4 portrait: cover, executive summary, brand foundation, identity, story, business overview, visual identity, logo identity, character identity, research evidence.
- A4 landscape: positioning, personas, persona comparison, market analysis, market size, competitor analysis, SWOT, TOWS, customer journey, brand applications, validation roadmap.
- A3 landscape: value proposition, Business Model Canvas, and optional Lean Canvas.

`page_layouts` can override these defaults with A4/A3, portrait/landscape, and margins in millimeters.

## Compatibility

The web app routes to the V2 report studio. The FastAPI app mounts the V2 report and V2 PDF routes; V1 section source files and notebook examples are retained as reference but are not registered in the active app. `past.zip` contains the pre-change repository snapshot, including files deleted from the current working tree in the existing worktree state.
