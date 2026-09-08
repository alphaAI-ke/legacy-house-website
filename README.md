# legacy-house-school-website

This is a [Next.js](https://nextjs.org) project bootstrapped with [v0](https://v0.app).

## Built with v0

This repository is linked to a [v0](https://v0.app) project. You can continue developing by visiting the link below -- start new chats to make changes, and v0 will push commits directly to this repo. Every merge to `main` will automatically deploy.

[Continue working on v0 →](https://v0.app/chat/projects/prj_8vJIBGIzXY2gsm0bLh3EcwxZEQXe)

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

## Learn More

To learn more, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.
- [v0 Documentation](https://v0.app/docs) - learn about v0 and how to use it.

<a href="https://v0.app/chat/api/kiro/clone/Muchirik/legacy-house-school-website" alt="Open in Kiro"><img src="https://pdgvvgmkdvyeydso.public.blob.vercel-storage.com/open%20in%20kiro.svg?sanitize=true" /></a>

---

## New in this update

**Design**: New visual identity (warm parchment/ink/brick/marigold palette, Fraunces + Source Sans 3 type pairing, "pennant notch" section dividers) replacing the previous generic AI-template look.

**Blog & News** (`/blog`): Public blog with News/Blog filtering and support for sub-blog pages (a post can have a parent post, shown as a "Part of:" link and listed as "Related sub-pages" on the parent).

**Admin panel** (`/admin`): Password-protected. Manage blog/news posts (including sub-blog pages), and view + reply to contact/enrollment form submissions.

**AI chatbot**: Floating assistant in the bottom-right corner, answering questions about programs, activities, and enrollment using the Anthropic API.

### Setup

1. Copy `.env.local.example` to `.env.local` and fill in:
   - `ADMIN_PASSWORD` — the password for `/admin` (change from the default!)
   - `ADMIN_SESSION_SECRET` — any long random string
   - `ANTHROPIC_API_KEY` — from https://console.anthropic.com, needed for the chatbot to work
   - `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASS` / `SMTP_FROM` — optional, lets the admin panel actually send reply emails. Without these, replies are still saved and shown in the admin panel, with a "mailto" link to send manually.

2. Install and run:
   ```bash
   npm install
   npm run dev
   ```

3. Visit `/admin` and sign in with `ADMIN_PASSWORD` to add blog posts and check form submissions.

### Data storage note

Blog posts and form submissions are stored in a local SQLite file at `data/app.db`, created automatically on first run. This works well on a normal always-on Node server (a VPS, Render, Railway, etc.). If you deploy to a **serverless** host like Vercel, that file will not persist between deployments/cold starts — you'd want to swap `lib/db.ts` for a hosted database (Postgres, Supabase, Turso, etc.) at that point; every query in the app goes through that one file, so nothing else needs to change.
