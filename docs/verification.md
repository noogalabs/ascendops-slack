# Verify the Slack connection

[Repository overview](../README.md) · [Setup guide](setup.md) · [Runtime compatibility](compatibility.md) · [Agent rules](agent-rules.md)

Begin with one agent, one authorized person, and a private DM. Confirm the installed build contains the [runtime implementation](https://github.com/noogalabs/ascendops/tree/b016f1fa6544609872674fced9c40a6d9440f841) from [PR #77](https://github.com/noogalabs/ascendops/pull/77), then perform these checks with harmless content. Coordinate negative-access tests with the administrator and participants.

Keep the installed revision, Node version, app/agent mapping, test date, and observations in a private setup record. Templates and automated tests do not verify your live Slack installation. Keep tokens, private conversations, and member records out of the public repository.

## Private-DM pilot

- [ ] The intended agent runs routed Socket Mode with native WebSocket support, normally Node.js 22 or later; its actual reply has the correct app identity.
- [ ] The app has its own complete credentials. A present per-agent secret file does not borrow missing/blank keys from ambient credentials.
- [ ] The selected primary is the actual app/person DM ID and is allowed by routing. No unrelated channel is required. Keep the separate trusted-handle list explicit.
- [ ] Routing validates and loads. Controlled invalid/unreadable policy fixtures refuse legacy fallback; permitted and denied sender/conversation routes behave as intended.
- [ ] A plain authorized DM gets a reply without a mention; a follow-up stays under its correct parent.
- [ ] A new proactive case produces a JSON send receipt. Its returned `ts`, conversation, person, and case ID are saved and reused for a later `--thread-ts` reply.
- [ ] Existing action-approval controls still apply. Use a harmless proposal rather than performing a consequential action just to test them.
- [ ] A normal restart preserves routing, durable instructions, and correct case-thread destinations. This does not prove replay of messages lost during a crash.

Resolve a failed required path before expanding.

## Expansion checks

- [ ] A real channel mention gets one threaded status answer; mentioning another agent does not invoke this one.
- [ ] Default mention-only filtering keeps ordinary channel input away from the model. If monitoring needs an explicit opt-out, record its agent-wide scope and test the approved quiet-channel/emergency behavior, including unmentioned urgent posts.
- [ ] Channel action requests are redirected to private case threads and the normal approval path.
- [ ] A second person's DM, replies, and case records stay separate from the first person's. Do not infer shared-memory isolation from Slack conversation separation.
- [ ] Controlled overlapping events/retries produce one reply within the listener's deduplication window. Do not claim exactly-once behavior across restarts.
- [ ] A small supported attachment is actually downloaded; a denied or oversized file produces an accurate error. Confirm the private retention/cleanup policy.
- [ ] A normal scheduled briefing arrives once at the agreed time, timezone, and audience.

## Record configuration separately from observation

Use **yes**, **no**, **unsupported**, or **not tested**, with a short nonsecret observation or test reference. “Configured” alone is not a pass.

| Capability | Configured? | Actually observed? | Evidence or remaining gap |
|---|---|---|---|
| Separate app, credentials, and native Socket Mode | | | |
| Plain authorized DM | | | |
| Conversation and sender restrictions | | | |
| Correct thread replies and saved proactive parent receipt | | | |
| Existing approval controls | | | |
| Configuration and case records after restart | | | |
| Channel mention response and technical input filtering | | | |
| Approved monitoring opt-out, if selected | | | |
| Separate second-person DM and context | | | |
| Bounded duplicate-event handling | | | |
| File content download and retention policy | | | |
| Normal scheduled delivery | | | |

Name the audiences and capabilities actually tested. The transport acknowledges before durable inbox completion and has no guaranteed crash replay; reconcile unresolved cases with business records. Expand from the verified pilot instead of declaring every agent ready from one connection.
