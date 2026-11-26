# NAME TAG V2

NAME TAG V2 turns brand inputs, interview answers, and completed analysis pages into a connected brand and business strategy report. The current `/generate` screen uses the page contracts in `backend/prompts/nametag_prompts_v2.py` and can export completed pages as a mixed-size PDF.

## Run locally

1. Set `GEMINI_API_KEY` in `backend/.env` using `backend/.env.example` as a guide.
2. Start the API from the repository root:

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

3. Start the web app in another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The frontend proxies `/api` to `http://localhost:8000` in development. For Docker, run `docker compose up --build` and open `http://localhost:3000`.

## V2 flow

- Enter brand name, industry, target, tone, and keywords.
- Generate a ready interview, answer its 5–10 questions, and save selected options and optional free text.
- Generate whichever report pages are ready. Each page uses the prior pages, interview answers, stable IDs, and source context required by its prompt contract.
- Enable Lean Canvas (page 17) and Character Identity (page 21) only when they apply.
- Regenerate a page when needed; dependent pages are marked for regeneration.
- Download a PDF of the pages completed so far. Default A4/A3 sizes and orientations follow the report design.

Progress is stored in this browser's `localStorage` under `nametag_report_v2`. It is not synced across browsers or devices.

## V2 API

- `GET /api/report-v2/meta`
- `POST /api/report-v2/plan`
- `POST /api/report-v2/interviews/{interview_id}`
- `POST /api/report-v2/pages/{page_id}`
- `POST /api/pdf/generate-v2`
- `GET /health`

V1 source modules are retained in the repository for reference, but the FastAPI app mounts the V2 report flow and V2 PDF endpoint as its generation API.

## Verify

```bash
python -m pytest backend/tests
cd frontend
npm test -- --run
npm run build
```

See [V2 integration notes](docs/REPORT_V2_INTEGRATION.md) for the request payloads, page dependency flow, and PDF layout mapping.
