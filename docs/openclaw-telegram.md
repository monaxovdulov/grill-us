# OpenClaw + Telegram room mode

This setup gives two or more people one attributed product conversation in Telegram. OpenClaw keeps the group in one session, supplies sender metadata, and records ordinary room chatter as quiet context. Grill Us uses that context to preserve who observed, assumed, preferred, or decided what.

The configuration follows the current OpenClaw documentation for [skills](https://docs.openclaw.ai/tools/skills), [Telegram](https://docs.openclaw.ai/channels/telegram), and [ambient room events](https://docs.openclaw.ai/channels/ambient-room-events).

## 1. Install Grill Us

Install the nested skill through OpenClaw's skills.sh resolver:

```bash
openclaw skills install skills-sh:monaxovdulov/grill-us/grill-us
openclaw skills check
```

The resolver pins the synchronized GitHub commit. A direct `git:monaxovdulov/grill-us` install is unsuitable for this repository because OpenClaw's Git installer expects `SKILL.md` at the repository root.

For a local checkout:

```bash
git clone https://github.com/monaxovdulov/grill-us.git
openclaw skills install ./grill-us/skills/grill-us --as grill-us
```

Start a new OpenClaw session after installation if the active session does not refresh its skill snapshot.

## 2. Let the Telegram bot see the room

Telegram Privacy Mode hides most unmentioned group messages from bots. For an always-on Grill Us room, either:

- disable Privacy Mode with BotFather `/setprivacy`; or
- make the bot a group administrator.

After changing Privacy Mode, remove and re-add the bot so Telegram applies the setting.

Find each participant's numeric Telegram user ID and the negative group ID. `openclaw logs --follow` shows both. Once the group is allowed, `/whoami@<bot_username>` confirms them.

## 3. Configure an attributed quiet room

Merge the following into `openclaw.json`. Keep any existing provider, model, workspace, and gateway settings.

```json5
{
  messages: {
    groupChat: {
      historyLimit: 50,
      unmentionedInbound: "room_event",
      visibleReplies: "message_tool",
    },
  },
  channels: {
    telegram: {
      enabled: true,
      botToken: "YOUR_TELEGRAM_BOT_TOKEN",
      groupPolicy: "allowlist",
      groupAllowFrom: [
        "FIRST_PARTICIPANT_TELEGRAM_ID",
        "SECOND_PARTICIPANT_TELEGRAM_ID",
      ],
      groups: {
        "-1001234567890": {
          requireMention: false,
        },
      },
    },
  },
}
```

This produces two inbound paths:

- an ordinary allowed message becomes a quiet `room_event` with its sender identity;
- a mention, reply to the bot, or command remains a direct user request.

Room events do not post final model text automatically. OpenClaw requires `message(action=send)` for a visible room reply. If the selected agent uses the `minimal` or `coding` tool profile, allow the message tool explicitly:

```json5
{
  agents: {
    entries: {
      main: {
        tools: {
          alsoAllow: ["message"],
        },
      },
    },
  },
}
```

## 4. Start the product session

Mention the bot once with the skill reference:

```text
@bot $grill-us Start a product session for this room.

First establish our names, roles, firsthand knowledge, and decision authority.
Then help us decide what to build and why. Keep every claim tied to its speaker,
preserve disagreement, and ask us questions by name. We may answer in any order.
```

After the roster is confirmed, participants can write naturally. OpenClaw supplies sender identity; Grill Us binds that identity to the roster and maintains the attribution ledger.

## 5. Verify the behavior

Run a short check with two accounts:

1. Participant A posts an observation without mentioning the bot.
2. Participant B posts a conflicting assumption without mentioning the bot.
3. Mention the bot and ask for the current evidence and disagreement.
4. Confirm that the response names the correct source for each claim and does not invent consensus.

Useful diagnostics:

```bash
openclaw skills info grill-us
openclaw skills check
openclaw channels status --probe
openclaw logs --follow
```

If the bot cannot see unmentioned messages, check `requireMention`, Telegram Privacy Mode, group allowlists, and whether the bot was re-added after the Privacy Mode change. If it sees messages but never posts, check that the agent has the `message` tool.
