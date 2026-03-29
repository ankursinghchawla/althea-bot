# Althea Bot

A Slack bot powered by Claude that channels **Althea** — a Grateful Dead specialist archivist with deep knowledge of shows, recordings, setlists, and Dead history.

Built for a small friend-group Slack workspace. Hosted free on Render.

## Commands

- `/heady [song]` — Top community-ranked versions from HeadyVersion
- `/song [title]` — Song dossier: origins, meaning, evolution
- `/show [date]` — Show dossier: setlist, context, highlights
- `/deep-dive [question]` — Sourced research across Dead archives
- `/shows [region]` — Upcoming Dead-related shows near you
- `/help` — List all commands

Commands work anywhere in the message. Or just chat with her — she's a conversationalist too.

## Architecture

- **Python** — slack_bolt, Flask, anthropic SDK, gunicorn
- **Claude Sonnet** with web search + web fetch tools
- **Skills** — each lives in `skills/[name]/SKILL.md` with optional `FORMAT.md`
- **Render free tier** — kept alive via UptimeRobot ping

## Setup

### 1. Create the Slack App

1. Go to https://api.slack.com/apps → "Create New App" → "From scratch"
2. Name: **Althea** | Workspace: yours
3. **OAuth & Permissions** → add these Bot Token Scopes:
   - `app_mentions:read`
   - `chat:write`
   - `channels:history`
   - `groups:history`
   - `im:history`
   - `im:read`
   - `im:write`
4. Click **Install to Workspace** and authorize
5. Copy the **Bot User OAuth Token** (`xoxb-...`) from the OAuth page
6. Go to **Basic Information** → copy the **Signing Secret**

### 2. Deploy to Render

1. Push this repo to GitHub
2. Go to https://render.com → New → **Web Service**
3. Connect your GitHub repo
4. Settings:
   - Runtime: **Python**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:flask_app --bind 0.0.0.0:$PORT`
   - Plan: **Free**
5. Add environment variables:
   - `SLACK_BOT_TOKEN` = your `xoxb-` token
   - `SLACK_SIGNING_SECRET` = your signing secret
   - `ANTHROPIC_API_KEY` = your Claude API key
6. Deploy and note the URL

### 3. Connect Slack Events

1. Back in Slack App settings → **Event Subscriptions** → toggle ON
2. Request URL: `https://YOUR-RENDER-URL/slack/events`
   - If it fails to verify, wait 60s for Render to wake up and retry
3. **Subscribe to bot events**:
   - `app_mention`
   - `message.im`
4. Save → Reinstall app if prompted

### 4. Keep-Alive (recommended)

1. Sign up at https://uptimerobot.com (free)
2. Add HTTP monitor → `https://YOUR-RENDER-URL/health` → every 5 minutes

## Adding Skills

Create a new directory in `skills/` with a `SKILL.md`:

```
skills/my-new-skill/
  SKILL.md      # frontmatter (name, slash_command, triggers, max_tokens) + instructions
  FORMAT.md     # optional output template
```

The bot loads skills on startup. Redeploy to pick up changes.

The `/help` skill output is hardcoded in `skills/help/SKILL.md` — update it manually when adding or changing skills.

## Environment Variables

| Variable | Source |
|---|---|
| `SLACK_BOT_TOKEN` | Slack App → OAuth & Permissions → Bot User OAuth Token |
| `SLACK_SIGNING_SECRET` | Slack App → Basic Information → Signing Secret |
| `ANTHROPIC_API_KEY` | console.anthropic.com → API Keys |

## Cost

- Render: $0 (free tier)
- Claude API: <$1/month at casual usage
- Web search + web fetch: $10 per 1,000 uses each (negligible at this scale)
- Slack: included in your existing workspace
- UptimeRobot: $0 (free tier)
