# Check your runtime first

The routed workflow in this kit requires the implementation in [runtime commit `b016f1f`](https://github.com/noogalabs/ascendops/tree/b016f1fa6544609872674fced9c40a6d9440f841), submitted in [runtime PR #77](https://github.com/noogalabs/ascendops/pull/77). Confirm that your installed build contains these changes; a link to source does not upgrade a running installation.

This repository supplies setup documents and templates. It does not install the runtime, create Slack apps, load credentials, or verify live delivery. Record your installed revision, Node version, active instance, agent IDs, and restart procedure before following [setup](setup.md).

## Required behavior and acceptance checks

| Requirement | Runtime behavior | Check in your installation |
|---|---|---|
| Separate app per agent | A second Socket Mode listener cannot claim an app token already held by another agent in the same daemon. | Give each agent its own app and complete credential pair. Confirm actual reply identities. Coordinate ownership across separate daemon instances yourself. |
| Native WebSocket | Routed mode requires an app token and native WebSocket support, normally Node.js 22 or later. It refuses a partial single-conversation polling downgrade. | Check the installed Node process and observe a working Socket Mode connection. Legacy polling does not satisfy this guide. |
| Complete credentials | A present routed-agent `.env` must contain its own nonblank bot/app pair. Missing keys or unreadable files do not borrow ambient credentials. | Use one app's pair in the approved secret store. A genuinely absent per-agent file may use a complete approved process-environment pair. |
| DM-only startup | Primary conversation precedence is `slack_watch.channel`, then `SLACK_CHANNEL`, then the first allowed routing conversation. | Use the actual app/person DM ID. An explicit primary must be allowed; no unrelated public channel is needed. |
| Sender and conversation restrictions | `allowed_channels` and workspace/member `allowed_users` must both pass. Empty or omitted allowlists deny input. | Test one permitted route and controlled denied sender/conversation routes. |
| Invalid routing | An existing malformed or unreadable `slack.json` refuses Slack startup and routed CLI sends. It does not become legacy mode. | Validate the file before restart and confirm the loaded policy. No file at all retains the separate legacy binding. |
| Additional sender trust | `trusted_slack_users` checks Slack handles after routing. Identity lookup needs `users:read`; an empty handle list is open at this additional gate. | Keep an explicit handle list and the scope, alongside the workspace/member allowlist. |
| Channel mentions | `app_mention` is handled. Routed non-DM input requires a mention by default; direct DMs do not. | Verify an actual mention reaches the model and ordinary channel input is filtered. Document any deliberate monitoring opt-out. |
| Issue threads | Inbox messages preserve the reply parent; `send-slack --thread-ts` sends to it. JSON send receipts expose the new message timestamp. | Observe both a threaded reply and a new proactive case, saving the returned parent timestamp. |
| Incoming files | Downloads run after access/mention checks, with private generated paths and bounded requests. | Test actual content with `files:read`, plus accurate failure reporting. Caption-only delivery is insufficient. |
| Restart and reports | Configuration loads at startup. Reports need actual scheduler jobs. | Restart the pilot and retest; observe a normal scheduled run before promising reports. |

An existing fleet sharing app tokens needs a migration to separate apps before enabling this workflow. Only the first same-daemon listener can claim a shared token; weakening that check would reintroduce split delivery.

## Configuration layers

1. [agent.env.example](../templates/agent.env.example): the agent's own bot/app token pair, stored privately.
2. [agent.config.fragment.json](../templates/agent.config.fragment.json): merge the applicable keys into existing `config.json`. Its watch conversation is an optional explicit primary; a route-only DM can use the first allowed conversation. Keep the trusted-handle list explicit.
3. [slack.example.json](../templates/slack.example.json): approved conversation IDs, workspace/member identities, and `channel_mentions_only`, saved as the installed agent's `slack.json`.
4. [Agent rules](agent-rules.md): case records, privacy, channel behavior, and business approvals. These complement runtime checks.

`allowed_users` values use `<WORKSPACE_ID>:<MEMBER_ID>`. `trusted_slack_users` uses handles. The two representations serve different checks. Keep each person's app DM and case-thread records separate; routing does not automatically isolate shared model memory.

`channel_mentions_only` defaults to `true` and applies to every allowed non-DM conversation for this agent. It also filters out unmentioned urgent posts. Set it to `false` only for a deliberately approved monitoring workflow, with narrow conversation access and durable quiet-channel/emergency rules. It is not a per-channel switch.

## Limits that still apply

- Thread placement does not load previous Slack history into the model. Use a current case summary or supported authorized retrieval.
- Incoming downloads allow four files per message, 10 MiB each, 20 MiB total, and approved HTTPS `files.slack.com` URLs only. Successful files remain in private state storage; the installation owns retention and cleanup. Outgoing uploads are separate.
- Socket envelopes are acknowledged before identity lookup, downloads, and durable inbox completion. A later failure or process crash can lose a message without Slack replay. Deduplication is bounded and in memory; it does not guarantee crash recovery or exactly-once actions.
- Template validation and automated runtime tests do not establish that your Slack app, scopes, routing, approvals, or scheduled deliveries work live. Use [verification](verification.md).

## Source reference

The pinned [runtime runbook](https://github.com/noogalabs/ascendops/blob/b016f1fa6544609872674fced9c40a6d9440f841/docs/architecture/slack-adapter-setup.md) describes the implementation. Relevant code: [startup](https://github.com/noogalabs/ascendops/blob/b016f1fa6544609872674fced9c40a6d9440f841/src/daemon/slack-startup.ts), [routing](https://github.com/noogalabs/ascendops/blob/b016f1fa6544609872674fced9c40a6d9440f841/src/slack/slack-routing.ts), [inbound delivery](https://github.com/noogalabs/ascendops/blob/b016f1fa6544609872674fced9c40a6d9440f841/src/daemon/slack-socket-listener.ts), [file downloads](https://github.com/noogalabs/ascendops/blob/b016f1fa6544609872674fced9c40a6d9440f841/src/slack/slack-files.ts), and [CLI sends](https://github.com/noogalabs/ascendops/blob/b016f1fa6544609872674fced9c40a6d9440f841/src/cli/bus.ts).

Return to the [README](../README.md) or continue with [setup](setup.md).
