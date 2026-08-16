# Recipe: Quiet Record

Use this recipe when a group wants Grill Us to observe a discussion, avoid unsolicited replies, and produce an attributed record when asked.

Minimum Grill Us version: `0.6.0`.

## Instructions for the agent

### 1. Check the host

1. Confirm which messages the host supplies, how speakers are identified, and whether unmentioned messages reach the agent.
2. Do not claim to observe messages that the host does not deliver.
3. Treat durable storage as optional. The host owns storage, retention, retrieval, and access control.

### 2. Install or verify Grill Us

If Grill Us is missing and the environment supports Agent Skills installation, run:

```bash
npx skills add monaxovdulov/grill-us --skill grill-us
```

Read the installed `SKILL.md`, verify `name: grill-us`, and require protocol version `0.6.0` or later. If installation is unavailable, report that limitation instead of claiming success.

### 3. Apply the recipe

- Use Record intervention.
- Preserve every sender supplied by the host.
- Treat ambient messages as context without a visible reply when the host supports mention-only operation.
- Reply when mentioned, directly asked, or given a checkpoint command.
- On request, show participants, attributed positions, decisions and their owners, open disagreements, and what needs to be learned.
- Use a host storage tool only after an explicit request to save the record. Do not configure or emulate durable memory.

Every record must state which conversation was considered:

- `Entire conversation` only when the host confirms complete history;
- `Messages since <time or message>` when the available boundary is known;
- `Unknown whether the beginning is available` otherwise.

### 4. Start the session

```text
Use Grill Us with the Quiet Record recipe.

Observe only the messages supplied by this host. Use Record intervention and do not reply unless mentioned or directly asked. Preserve sender provenance. When asked to show the record, include decisions, owners, open disagreements, and what needs to be learned. State which part of the conversation was considered. Save through host memory only when explicitly requested.
```
