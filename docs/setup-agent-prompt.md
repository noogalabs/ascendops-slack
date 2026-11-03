# Instructions for your setup agent

Copy and adapt this prompt after reading [compatibility](compatibility.md):

```text
Help me connect my existing Fleet agents to Slack using this setup kit.

First inspect my installed runtime version, agent directories, existing Slack
apps, channel bindings, routing, message tools, and approval roles. Do not
assume that Slack permissions enable unsupported runtime features.

Show me a non-secret mapping of existing agent roles to separate Slack apps,
approved conversations, and authorized people before changing access. Use my
existing agent identifiers. Do not deploy dormant agents just to fill a role.

Start with one existing agent and one authorized person. Each agent needs its
own app, bot token, and app-level Socket Mode token. Prepare non-secret app
settings and routing. Let me or my authorized Slack administrator handle
credentials and any required installation approval. Never ask me to paste
tokens into chat, source control, or shared notes.

Confirm how my installed version starts its listener for a DM-only connection.
Do not invent an unnecessary public channel or broaden access to make it start.
Check both conversation and sender restrictions, including malformed-routing
behavior. Validate configuration before the normal restart procedure.

Persist the channel mention rule, private-DM rules, one-thread-per-issue rule,
and notification limits in the agents' durable operating instructions. Check
that the runtime carries inbound thread context and can send into that thread.

Keep department channels for shared status and approved briefings. Actions and
approvals belong in the appropriate private case thread. Keep dispatch and
decisions separate if they have different intended audiences. Preserve all
business approval roles, spending limits, holds, and privacy requirements.

Use the verification checklist. Distinguish configured, observed, unsupported,
and not-yet-tested behavior. Report gaps before calling the rollout complete.
Expand only after the first connection's required behavior is verified.
Choose briefing times and timezone with me and reuse existing scheduler jobs
where possible. Do not claim a scheduled run or another person's access is
verified until that exact path has been observed.
```

Return to the [README](../README.md).
