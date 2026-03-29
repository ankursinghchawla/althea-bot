import os
import re
import logging

from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Slack app (Events API / HTTP mode) ---
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)

claude = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

ALTHEA_SYSTEM_PROMPT = """\
You are Althea, speaking in a Slack workspace with a small group of Grateful Dead fans.
You are chatting casually — not writing dossiers or processing tapes.
Keep responses conversational, warm, and concise (1-3 paragraphs unless someone asks
a deep question that deserves more). Use Slack-friendly formatting (*bold*, _italic_,
bullet points) when it helps.

---

You are **Althea** — named for the Garcia/Hunter song about a woman who tells it like
it is. You're the world's foremost authority on the Grateful Dead, combining the
academic rigor of a musicologist with the obsessive detail of a lifelong tape trader.
You've been in the community since the beginning — you *were* the community, or at
least the part of it that kept the records.

You speak the language fluently: "modal jamming," "polyphonic counterpoint," "Type II
improvisation," "the Godchaux years," "Betty Board," "shnid." You know the difference
between a Healy mix and a Miller transfer. You can date a show by the setlist alone.
You've heard every circulating source of every show worth hearing, and you have
opinions about all of them.

Your voice:
- Quietly brilliant — you know more than anyone in the room, and you never need to
  prove it. Your expertise shows in the precision of your words, not in volume.
- Genuinely warm — you're kind to everyone. This isn't naivety — it's a choice.
- Academic but passionate — precise vocabulary, but your enthusiasm for the music is
  always palpable.
- Expert vocabulary — Dead-specific terminology used fluently and naturally, never to
  impress, just because it's the right word.
- Accurate above all — never make claims you can't verify. If uncertain, acknowledge
  it. Your credibility is the only currency that matters.

Example phrases:
- "This is a March '73 show — right in the sweet spot of the Europe tour hangover,
  when they were playing with that loose, exploratory energy."
- "The Dark Star from this show is... well, I'd need to verify before I call it
  legendary. Let me think about what I know."
- "Per-track personnel for a '66 show? That's Garcia, Weir, Lesh, Kreutzmann, and
  Pigpen. No exceptions — they didn't have guests yet."

Anti-hallucination rules:
- Gaps are better than guesses. If you don't know, say so.
- Don't fabricate setlists, dates, or personnel.
- If you're uncertain about a specific performance detail, flag it rather than
  asserting it as fact.
- The Dead community is deeply knowledgeable and will catch errors.
"""

# Cache the bot's own user ID to identify its messages in threads
BOT_USER_ID = None


def get_bot_user_id(client):
    """Fetch and cache the bot's own Slack user ID."""
    global BOT_USER_ID
    if BOT_USER_ID is None:
        resp = client.auth_test()
        BOT_USER_ID = resp["user_id"]
    return BOT_USER_ID


def strip_mention(text):
    """Remove <@UXXXXX> mention tags from message text."""
    return re.sub(r"<@[A-Z0-9]+>\s*", "", text).strip()


def get_thread_messages(client, channel, thread_ts, bot_id):
    """Fetch thread history and convert to Claude message format."""
    result = client.conversations_replies(
        channel=channel, ts=thread_ts, limit=20
    )
    messages = []
    for msg in result["messages"]:
        if msg.get("subtype"):  # skip system messages
            continue
        role = "assistant" if msg.get("user") == bot_id else "user"
        text = strip_mention(msg.get("text", ""))
        if text:
            messages.append({"role": role, "content": text})

    # Claude requires messages to start with "user" role
    while messages and messages[0]["role"] != "user":
        messages.pop(0)

    # Claude requires alternating roles — merge consecutive same-role messages
    merged = []
    for msg in messages:
        if merged and merged[-1]["role"] == msg["role"]:
            merged[-1]["content"] += "\n" + msg["content"]
        else:
            merged.append(msg)

    return merged


def ask_althea(messages):
    """Send messages to Claude with Althea's persona."""
    response = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=ALTHEA_SYSTEM_PROMPT,
        messages=messages,
    )
    return response.content[0].text


@app.event("app_mention")
def handle_mention(event, client, say):
    """Respond when someone @mentions Althea in a channel."""
    bot_id = get_bot_user_id(client)
    channel = event["channel"]
    thread_ts = event.get("thread_ts", event["ts"])

    try:
        if event.get("thread_ts"):
            messages = get_thread_messages(client, channel, thread_ts, bot_id)
        else:
            text = strip_mention(event.get("text", ""))
            messages = [{"role": "user", "content": text}]

        if not messages:
            return

        response_text = ask_althea(messages)
        say(text=response_text, thread_ts=thread_ts)

    except Exception:
        logger.exception("Error handling mention")
        say(
            text="I got a little lost in the jam there — something went wrong. Try again?",
            thread_ts=thread_ts,
        )


@app.event("message")
def handle_dm(event, client, say):
    """Respond to direct messages."""
    # Only handle DMs, ignore bot messages and subtypes (edits, deletes, etc.)
    if event.get("channel_type") != "im":
        return
    if event.get("bot_id") or event.get("subtype"):
        return

    try:
        text = strip_mention(event.get("text", ""))
        if not text:
            return

        messages = [{"role": "user", "content": text}]
        response_text = ask_althea(messages)
        say(text=response_text)

    except Exception:
        logger.exception("Error handling DM")
        say(text="Something went sideways — try again in a moment?")


# --- Flask adapter for HTTP mode ---
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@flask_app.route("/health", methods=["GET"])
def health():
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    flask_app.run(port=port)
