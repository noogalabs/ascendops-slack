# Connect existing Fleet agents to Slack

[Repository overview](../README.md) · [Runtime compatibility](compatibility.md) · [Agent rules](agent-rules.md) · [Verification checklist](verification.md)

Give each existing Fleet agent its own Slack app and each authorized person a separate private conversation with that app. Start with one agent and one person in a private DM, then expand from a verified connection.

Install a runtime containing the changes in [commit `b016f1f`](https://github.com/noogalabs/ascendops/tree/b016f1fa6544609872674fced9c40a6d9440f841), submitted in [PR #77](https://github.com/noogalabs/ascendops/pull/77), and complete the [compatibility checks](compatibility.md). This kit provides configuration examples; it does not install those changes or prove live Slack access works.

## Daily use

- **Private requests:** DM the agent without an @mention. Keep each issue's questions, proposals, approvals, and follow-ups in its own thread.
- **Shared status:** Select the actual agent from Slack's @mention picker in an approved department channel. Its status answer stays in that message's thread.
- **Actions and approvals:** Use the appropriate private DM case thread. Existing business roles, spending limits, holds, and approvals still apply.
- **Notifications:** Agents proactively DM for decisions, approvals, go-aheads, or missing information. Agreed routine reports belong in channels.

## 1. Inventory and map access

Identify the installed revision, Node.js version, active Fleet instance, existing agent IDs, configuration locations, and normal restart procedure. Routed Slack requires native WebSocket support, normally Node.js 22 or later. Preserve the previous configuration for rollback.

Inspect existing apps, listeners, and reports before creating replacements. Use a separate app, bot token, and app-level token for each agent. Slack can distribute an app's payloads among its open connections instead of copying them to every agent. The runtime blocks a second same-daemon listener using an already claimed app token. Migrate shared credentials before enabling the new workflow; coordinate separate daemon instances yourself. See [Slack's connection behavior](https://docs.slack.dev/apis/events-api/using-socket-mode/#using-multiple-connections).

Record a private, nonsecret map:

| Fleet role | Slack app | Authorized people | Approved conversations |
|---|---|---|---|
| Pilot agent | Its own app | One pilot member | That app/person DM |
| Department agent, later | Its own app | Designated staff | Its department channels and separate person/app DMs |
| Orchestration agent, later | Its own app | Explicitly chosen audiences | Private dispatch, separate decisions channel, and authorized DMs |

Use existing agent IDs and have the authorized owner review the map before changing access. Access to one agent does not grant access to every agent. Keep different private-channel audiences separate and leave unrelated apps out of confidential channels.

## 2. Create the pilot Slack app

An authorized workspace administrator handles installation and credentials. A setup agent can prepare the nonsecret manifest, routing, and tests.

1. Open [Your Slack apps](https://api.slack.com/apps), select the intended workspace, and create an app from [dm-only-app.manifest.json](../templates/dm-only-app.manifest.json). Change the app and bot names to this agent's stable functional identity. Validate the manifest in Slack.
2. Enable **Socket Mode**. Generate a separate app-level token with `connections:write`; this permission is not a bot OAuth scope.
3. Under **App Home**, enable the Messages tab and let people send messages. Confirm the pilot member has a composer, rather than a read-only tab.
4. Subscribe to the bot event `message.im` and keep `chat:write`, `im:history`, and `users:read` bot scopes. The runtime uses `users.info` to resolve the trusted handle.
5. Install the app and save its current bot token through the approved secret procedure. Reinstall or reauthorize after scope changes, then check saved events and effective scopes.

DMs arrive through `message.im`, without needing a mention. Socket Mode needs no public Events API Request URL. See [Socket Mode setup](https://docs.slack.dev/apis/events-api/using-socket-mode/), [DM events](https://docs.slack.dev/reference/events/message.im/), [Messages settings](https://docs.slack.dev/reference/app-manifest/), and [users.info permissions](https://docs.slack.dev/reference/methods/users.info/).

Add `files:read` only when receiving attachments is in scope. Add `im:write` only if a supported setup tool needs to open DMs programmatically. Outgoing file uploads and reactions are separate capabilities. Do not grant broad administrative, group-DM, unrestricted public-posting, or auto-join permissions by default.

## 3. Store credentials and choose the primary conversation

Use [agent.env.example](../templates/agent.env.example) with your runtime's private secret-loading method. Never paste real tokens into chats, issues, shared documents, screenshots, or source control.

For a routed agent with a present per-agent `.env`, store its own complete, nonblank `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` pair there. Missing/blank keys do not borrow ambient credentials, and an unreadable file refuses Slack startup. Only a genuinely absent per-agent file may use a complete approved pair from the process environment. Keep both tokens associated with the same agent's app.

The runtime chooses the primary conversation in this order:

1. Existing `config.json` → `slack_watch.channel`, if set.
2. `SLACK_CHANNEL` from the agent environment, if set.
3. The first allowed conversation in valid `slack.json`.

Every explicit primary must also be allowed by routing. A DM-only route can start from its DM ID without an unrelated shared channel or synthetic watch block. Routed mode requires both tokens and native WebSocket support; it refuses a single-conversation polling downgrade. Only a separate legacy binding with no `slack.json` retains legacy polling.

Merge applicable fields from [agent.config.fragment.json](../templates/agent.config.fragment.json) into the existing agent configuration; preserve its other settings. A watch conversation is an optional explicit primary. Keep `trusted_slack_users` set to the authorized person's exact Slack handle. These handles are separate from the workspace/member identities below; retain `users:read` instead of clearing the trusted list to bypass lookup failures.

## 4. Restrict conversations and people

Adapt [slack.example.json](../templates/slack.example.json) in the installed agent's documented `slack.json` location. Replace placeholders only in your private installation and validate the schema before restart.

| Field | Meaning |
|---|---|
| `allowed_channels` | Approved conversation IDs, including each app/person DM ID |
| `allowed_users` | Authorized `<WORKSPACE_ID>:<MEMBER_ID>` identities |
| `channel_mentions_only` | Defaults to `true`; requires mentions in all allowed non-DM conversations for this agent |
| `display_name`, if used | Must match the agent's permitted functional identity |

Both the conversation and sender checks must pass before delivery. Empty or omitted allowlists deny input. An existing malformed or unreadable routing file refuses Slack startup and routed CLI sends; it does not widen access through legacy fallback. No routing file at all retains a separate legacy binding, so do not omit the file as an access-denial strategy.

The sender allowlist is agent-wide. Preserve intended private-channel audiences through channel membership too. A person allowed to message an agent still needs the proper business authority for any requested action.

### Establish the pilot DM

1. Have the pilot member open the app's Messages tab and send a harmless discovery message, or use an approved supported DM-opening method.
2. Obtain that exact app/person DM ID through a supported discovery tool or Slack API method. Initial discovery may be denied until the route is allowed.
3. Add the DM ID, workspace/member identity, and separate trusted handle to the pilot's configuration. Never disable routing globally to discover an ID.
4. Restart only the intended agent through the documented procedure and confirm its routing loaded.
5. Send a fresh plain DM. Observe a reply from the intended bot in that same conversation.

Each person has a different DM with each app. Never reuse another person's or another agent's DM ID.

## 5. Persist rules and thread records

Adapt [agent-rules.md](agent-rules.md) into the durable instructions Fleet actually loads. Keep existing authority, approvals, and privacy rules. Record the person, case identifier, conversation ID, and parent timestamp together in durable case notes.

Routed inbound messages preserve the reply parent. In the intended agent's configured context, reply using:

```bash
cortextos bus send-slack '<CONVERSATION_ID>' '<REPLY_TEXT>' --thread-ts '<PARENT_TIMESTAMP>'
```

A send without `--thread-ts` creates a new parent. The JSON success receipt includes `channel`, `ts`, `thread_ts`, and `new_parent`. For a new proactive case, save the returned `ts` as its parent before follow-ups. For a threaded reply, retain the existing parent. Use exact allowed conversation IDs; the CLI checks routed destinations. Do not invent a timestamp if a receipt is incomplete.

Keep one issue thread per person's DM. Thread placement does not automatically load earlier Slack history; use a current durable summary or supported authorized retrieval. Separate DMs do not automatically isolate an agent's shared model memory. Do not disclose another person's private conversation to a different audience.

## 6. Add channels and approved monitoring

After the private pilot passes [verification](verification.md), adapt [department-app.manifest.json](../templates/department-app.manifest.json). Remove unused permissions and events. For channels, use `app_mention` with `app_mentions:read`; add public/private message events and history/discovery scopes only as needed by the selected workflow. See [Slack's mention event](https://docs.slack.dev/reference/events/app_mention/) and [scope reference](https://docs.slack.dev/reference/scopes/).

Invite only the relevant app to each approved channel and add its ID to routing. Verify one threaded answer to a real mention. With the default `channel_mentions_only: true`, ordinary non-DM input is filtered before model delivery; direct DMs do not require a mention. Durable rules still keep shared responses to status/clarification and route actions or approvals to private case threads.

Filtering also excludes unmentioned urgent posts. If an approved monitoring or emergency workflow needs those messages, deliberately set `channel_mentions_only: false` and retain quiet-channel and escalation rules. This setting is per agent and affects **all** its allowed non-DM conversations, so narrow access accordingly. Do not assume an agent can react to filtered input.

Add a second authorized person as a separate DM and test that person's route and thread records independently. Add agents and channels gradually from the verified pattern.

## 7. Files, reports, and delivery limits

Incoming attachments require `files:read` and successful access checks. The downloader permits four files per message, 10 MiB per file, and 20 MiB total, using approved HTTPS `files.slack.com` URLs. It writes generated files in private state storage and reports local paths or explicit errors to the inbox. External or unsupported download URLs remain unavailable. Verify actual content; a caption or file event alone is insufficient.

Successful downloads persist. The installation owns retention and cleanup; this kit sets no automatic expiry. Choose an appropriate private retention policy before expanding file use. Outgoing uploads remain separate.

Reports need real Fleet scheduler jobs with agreed days, times, timezone, and audience. Reuse existing reporting work and check for duplicate delivery through other transports. Observe a normal scheduled run before promising it.

Socket envelopes are acknowledged before identity lookup, downloads, and durable inbox completion. A later failure or process crash can lose input without Slack replay. Deduplication is bounded and in memory, so it does not guarantee crash recovery or exactly-once actions. Reconcile unresolved work with business records and preserve action approvals on retries.

Complete [verification](verification.md), recording configured state separately from actual observations. Template validation cannot verify live app settings, loaded credentials, message delivery, or scheduled reports. Use [troubleshooting](troubleshooting.md) for a failing path.
