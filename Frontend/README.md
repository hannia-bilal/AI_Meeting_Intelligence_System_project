# Confer — AI Meeting Intelligence (Frontend)

A React + Tailwind CSS frontend for the AI Meeting Intelligence System: upload
or record a meeting and get a structured, actionable report — summary,
decisions (with rationale), prioritized action items, detected deadlines,
speaker contribution metrics, and a chat interface that answers questions
about that specific meeting.

This is the **frontend only**. It runs entirely on mock data
(`src/data/mockData.js`), shaped to match the real backend's response
contract, so every screen is clickable without a backend. Swap that data
source for real calls through `src/api/client.js` once the FastAPI backend
described in the project spec is live — see "Connecting the real backend"
below.

## Screens

| Route              | Page              | Purpose                                                          |
|---------------------|-------------------|--------------------------------------------------------------------|
| `/login`            | Login             | Split-panel sign-in with the product illustration                  |
| `/register`         | Register          | Create an account (name, email, role, team, password)              |
| `/dashboard`         | Dashboard         | Stats, recent meetings, upcoming deadlines panel, quick upload      |
| `/upload`            | New Meeting       | Upload a file **or** record from the mic, with live status         |
| `/meetings`          | All Meetings      | Full list with status filters                                       |
| `/meetings/:id`      | Meeting Details   | Tabs: Overview, Transcript, AI Insights, Ask AI                     |
| `/search?q=`         | Search Results    | Search across meetings, decisions, participants                     |
| `/profile`           | Profile           | Personal info, password, theme, notification preferences            |

## What's implemented against the project spec

- Upload **and** in-browser recording (`RecordMeeting.jsx` uses the
  MediaRecorder + Web Audio API for a live level meter — a real recorder,
  not a mockup).
- Speaker-wise transcript with clickable timestamps that jump the player,
  plus a **speaking time & contribution** panel (per-speaker seconds spoken,
  contribution %, turn count, and the SPEAKER_XX → real-name mapping) —
  matches the diarization/contribution-metrics part of the AI module.
- Short/Detailed summary toggle, timestamped key discussion points, and a
  **numeric sentiment score** (-1.0 to +1.0) alongside the category and a
  qualitative tone summary.
- **Decisions with rationale and a timestamp**, not just plain text.
- **Action items** with task/owner/deadline **and priority**.
- **Deadlines detected** — shows the original spoken phrase next to the
  normalized ISO date (e.g. "by Friday" → `2026-09-05`).
- **Unresolved issues with an urgency rating**, and **follow-up items** as
  their own section with a recommended owner and timeframe (spec treats
  these as two distinct categories, not one merged list).
- Meeting-scoped "Ask AI" chat that cites a timestamp with its answer.
- Dashboard: recent meetings, processing status per meeting, action item /
  decision / deadline counts, an upcoming-deadlines panel, and search.
- Full search results page and a filterable all-meetings list.
- Auth (login/register with role/team), a fuller profile page (personal
  info, password, appearance, notifications), and empty/error states
  throughout.

## Design

- **Theme**: light and dark, toggle in the top bar (sun/moon icon) and also
  in Profile → Appearance. Respects system preference on first load, choice
  persisted in `localStorage`. Dark mode swaps to a deep espresso-brown
  background (not slate, not pure black) — stays in the same warm family
  instead of jumping to a cold theme.
- **How theming works**: every themeable color (`paper`, `sidebar`,
  `surface`, `ink`, `line`, and the accent scales) is a CSS variable
  defined once in `src/index.css` under `:root` and `.dark`. Components
  just use ordinary Tailwind classes like `bg-paper` or `text-ink-soft` —
  nothing is duplicated per-component.
- **Palette**: "Warm Walnut & Muted Sand" — a mid-tone editorial palette,
  no harsh blacks or clinical whites, grounded in earthy hues. Canvas is
  `#EAE4DC`, sidebar/nav is `#DDD4C8`, cards are `#F5F0EB`, text is
  `#2D241E` / `#6F6358`, borders are `#C5B9AA`.
- **Color roles** (each accent is scoped to a specific meaning, not reused
  generically):
  - **Walnut** `#78350F` — primary brand, buttons, links, speaker tags
  - **Caramel** `#B45309` — AI/Insights (key discussion points, Ask AI, follow-ups)
  - **Tobacco** `#854D0E` — action items / active status
  - **Olive** `#4D7C0F` — decisions / completed
  - **Ochre** `#A16207` — unresolved issues / warnings
  - **Oxblood** `#9F1239` — deadlines / urgency / failed / destructive
  Dark mode brightens each accent for contrast on a deep-espresso
  background.
- **Type**: Sora for headings, Inter for body/UI text, JetBrains Mono for
  timestamps and dates — actual data gets a data-style typeface, nothing
  else does.
- **Logo**: an original mark — a voice waveform resolving into a checkmark
  (`components/ui/Logo.jsx`), used in the sidebar, favicon, and auth screens.
- **Illustrations**: hand-built SVG, not stock art — `BriefingIllustration`
  (auth screens) and `PipelineDiagram` (upload screen, mirrors the spec's
  Audio → Transcript → Speakers → LLM → Structured Data → Q&A pipeline).
- Participant initials render as colored `Avatar` chips instead of a plain
  count, used in meeting rows, Overview, and the speaker metrics panel.

## Folder structure

```
src/
├── api/                 → fetch wrapper for the real backend (client.js),
│                           with JSDoc types mirroring the AI module's
│                           Pydantic schemas (TimestampReference, Decision,
│                           ActionItem, SpeakerMetric, Sentiment, etc.)
├── components/
│   ├── auth/            → AuthCard (split-panel shell for Login/Register)
│   ├── illustrations/   → BriefingIllustration, PipelineDiagram (hand-built SVG)
│   ├── layout/          → Sidebar, Topbar (search + theme toggle + user menu)
│   ├── meetings/        → UploadDropzone, RecordMeeting, ProcessingStages,
│   │                       AudioPlayer, MeetingRow, SpeakerMetrics, and the
│   │                       4 meeting-detail tabs (Overview / Transcript /
│   │                       Insights / Ask AI)
│   └── ui/               → Avatar, Logo, Button, Input, StatCard, StatusBadge,
│                            Tabs, EmptyState
├── context/              → AuthContext (mock auth + profile), ThemeContext
├── data/                 → mockData.js — sample meetings matching the real
│                            backend's response shape
├── layouts/              → AppLayout (sidebar + topbar shell for logged-in pages)
├── pages/                → one file per route, listed above
├── routes/               → ProtectedRoute (redirects to /login if signed out)
├── App.jsx               → route definitions
├── main.jsx              → app entry point (wraps App in Theme + Auth providers)
└── index.css             → Tailwind entry + light/dark CSS variables
```

## Getting started

```bash
npm install
npm run dev       # http://localhost:5173
```

Any email/password on the Login or Register screen works — auth is mocked in
`AuthContext.jsx` and stored in `localStorage` under `mi_user`. Recording
requires microphone permission in the browser.

## Build for production

```bash
npm run build      # outputs to dist/
npm run preview    # preview the production build locally
```

## Connecting the real backend

1. Copy `.env.example` to `.env` and set `VITE_API_BASE_URL` (defaults to
   `http://localhost:8000/api/v1`, matching the FastAPI example in the spec).
2. `src/api/client.js` already targets the described endpoints:
   `POST /auth/login`, `POST /auth/register`, `GET/PATCH /auth/me`,
   `GET /meetings`, `GET /meetings/:id`, `POST /meetings/upload`,
   `POST /meetings/:id/analyze` (returns a `MeetingIntelligenceReport` —
   see the JSDoc typedefs at the top of the file), `POST /meetings/:id/ask`,
   `GET /meetings/:id/conversation`, and `GET /meetings/search?q=`.
3. Replace the `mockData.js` imports in `Dashboard.jsx`, `AllMeetings.jsx`,
   `MeetingDetails.jsx`, and `SearchResults.jsx` with calls through `api`.
   The mock objects are already field-for-field shaped like the real
   `MeetingIntelligenceReport`, so this should mostly be a data-source swap,
   not a component rewrite.
4. In `UploadMeeting.jsx`, replace the fake stage timer with real polling
   against `getProcessingStatus(id)`.
5. In `AudioPlayer.jsx`, replace the placeholder transport with a real
   `<audio>`/`<video>` element pointed at the processed file URL, and wire
   `jumpTo` to actually seek the media (needed for the clickable timestamps
   in the Transcript, Insights, and Ask AI tabs).

## Tech stack

- React 18 + React Router 6
- Vite
- Tailwind CSS (CSS-variable-driven light/dark theme)
- lucide-react (icons)

> Note: the project spec's tech table recommends TypeScript. This build is
> JavaScript for now to keep the diff small while the data contract was
> still changing; converting is mostly mechanical (`.jsx` → `.tsx` plus
> typing props) and can be done as a follow-up once the API shape is final.
