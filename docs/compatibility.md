# Check your runtime first

The Slack app and Fleet runtime must both support the behavior you want. This kit supplies configuration templates and operating rules. It does not add missing event handlers, threading, file downloads, or scheduler jobs to your installation.

Record your installed Fleet revision, Node version, agent directory, current communication settings, and available send tools. Compare them with the requirements below before creating apps or changing access.

## Public runtime reference

The public [AscendOps source](https://github.com/noogalabs/ascendops/tree/95baa58d5b0755b1add8f536ec57070b04d1eae8) was reviewed on November 3, 2026 at commit `95baa58d5b0755b1add8f536ec57070b04d1eae8`. These findings describe that snapshot, not every Fleet installation or future release. Your installed build and its loaded configuration remain the source of truth for your setup.

| Requirement | Reviewed public source | What to do before relying on it |
|---|---|---|
| Separate Slack apps | Configurable per agent; duplicate app-token ownership only warns. | Give each agent a different app and credentials. Check the identity of actual replies. |
| Sender and conversation routing | A valid `slack.json` gates both `allowed_channels` and `allowed_users`. | Use explicit allowlists, validate the JSON, and verify permitted and denied routes. |
| Missing or malformed routing | Falls back to the legacy single-conversation binding. | Do not interpret a broken or missing file as denial. Confirm the running configuration loaded. |
| Listener startup | Requires `config.json` → `slack_watch.channel`. Tokens, `SLACK_CHANNEL`, and `slack.json` alone do not start inbound delivery. | Merge the startup fragment into the existing agent configuration and verify the listener starts. |
| Socket Mode | Uses native `WebSocket`, documented for Node 22+. Node 20/21 use single-conversation polling fallback. | Check the runtime actually has native WebSocket support. Polling a primary conversation does not verify all listed conversations. |
| Private DMs | Routing accepts a listed `D...` conversation ID. | Verify DM-only startup and real inbound/outbound delivery for this app/person pair. |
| Additional sender trust | `trusted_slack_users` uses Slack **handles**, separately from routing IDs. The lookup calls `users.info` and requires `users:read`. An empty or omitted list is open at this later gate. | Keep `users:read` in the DM profile and an explicit handle list as well as the routing allowlist. Test the installed identity resolution. |
| Channel mentions | The Socket Mode filter accepts message events; it does not handle `app_mention`. No technical mention-only gate was found. | Add supported mention handling before claiming that profile works. A behavior instruction can limit replies but does not prevent model delivery. |
| Issue threads | The inbound listener omits the parent `thread_ts` from the agent inbox. Normal `send-slack` and `SlackAPI.postMessage` do not expose a thread argument. | Complete and verify the inbound-to-outbound thread path. A separate thread helper exists but is not the ordinary reply path. |
| Incoming files | File events may be delivered, but the reviewed listener renders text and has no file downloader. | Enable file permissions only for a runtime with verified authenticated downloading and explicit failure reporting. |
| Duplicate events | Per-agent deduplication windows and reservations exist. | Verify one answer for overlapping mention/message delivery in your installation. |
| Restart persistence | Credentials and routing load at startup. | Use your normal restart procedure and retest. Do not assume hot reload. |
| Scheduled briefings | Require scheduler jobs and a supported send path. | Observe a normal scheduled run; app subscriptions do not create reports. |

**This snapshot cannot reproduce the complete guide without runtime work.** A basic text-DM experiment can establish partial connectivity. The finished arrangement also requires correct issue threads, intended channel behavior, enforced access, and every other capability you select in the [verification checklist](verification.md).

## Configuration layers

The examples describe the reviewed runtime. Check your version's schema before using them. Keep real configuration in your private installation.

1. [agent.env.example](../templates/agent.env.example): each agent's bot and app-level tokens, stored through your approved secret procedure.
2. [agent.config.fragment.json](../templates/agent.config.fragment.json): the startup conversation and explicit Slack handles. **Merge these keys into the existing `config.json`; do not replace the whole file.**
3. [slack.example.json](../templates/slack.example.json): conversation IDs and sender IDs, saved as the installed runtime's per-agent `slack.json`.
4. [Agent rules](agent-rules.md): behavior, case-thread records, and business authority. These complement runtime enforcement.

The primary `slack_watch.channel` conversation must also be in `allowed_channels`. For a DM-only setup, use the actual app/person DM ID only when your runtime supports it; verify startup rather than creating an extra public channel to satisfy a setting.

`allowed_users` entries use `<WORKSPACE_ID>:<MEMBER_ID>`. `trusted_slack_users` entries use the corresponding Slack handle. They are different fields for different checks; do not copy one representation into the other.

The reviewed routing schema supports optional `display_name`, `icon_emoji`, and `icon_url`, plus the two string-array allowlists. A valid empty allowlist denies routing; malformed JSON or a malformed schema can trigger the legacy fallback instead. Avoid unverified identity overrides and keep required lists explicit.

## Source references

- [Runtime setup runbook](https://github.com/noogalabs/ascendops/blob/95baa58d5b0755b1add8f536ec57070b04d1eae8/docs/architecture/slack-adapter-setup.md)
- [Routing schema and validation](https://github.com/noogalabs/ascendops/blob/95baa58d5b0755b1add8f536ec57070b04d1eae8/src/slack/slack-routing.ts)
- [Agent startup](https://github.com/noogalabs/ascendops/blob/95baa58d5b0755b1add8f536ec57070b04d1eae8/src/daemon/agent-manager.ts)
- [Socket/polling selection](https://github.com/noogalabs/ascendops/blob/95baa58d5b0755b1add8f536ec57070b04d1eae8/src/daemon/slack-inbound-mode.ts)
- [Socket event filtering](https://github.com/noogalabs/ascendops/blob/95baa58d5b0755b1add8f536ec57070b04d1eae8/src/slack/slack-socket.ts)
- [Inbound inbox rendering](https://github.com/noogalabs/ascendops/blob/95baa58d5b0755b1add8f536ec57070b04d1eae8/src/daemon/slack-socket-listener.ts)
- [Outbound bus commands](https://github.com/noogalabs/ascendops/blob/95baa58d5b0755b1add8f536ec57070b04d1eae8/src/cli/bus.ts)
- [Slack handle trust resolution](https://github.com/noogalabs/ascendops/blob/95baa58d5b0755b1add8f536ec57070b04d1eae8/src/slack/slack-identity.ts)

Return to the [README](../README.md) or continue with [setup](setup.md).
