# Frontend — Next.js 14

## Setup

```bash
npm install
cp .env.local.example .env.local
# Edit .env.local — set NEXT_PUBLIC_API_URL to your backend URL
```

## Run

```bash
npm run dev
```

App: http://localhost:3000

## Pages

| Route | Description |
|-------|-------------|
| `/` | Browse & filter all tracked AI laws |
| `/laws/[id]` | Full law detail with compliance checklist |
| `/search` | Semantic search across laws |
| `/compliance` | AI compliance analyzer — enter your company profile |

## Build

```bash
npm run build
npm start
```
