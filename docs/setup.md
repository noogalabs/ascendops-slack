# Connect existing Fleet agents to Slack

[Repository overview](../README.md) · [Runtime compatibility](compatibility.md) · [Agent rules](agent-rules.md) · [Verification checklist](verification.md)

This guide connects agents you already run in Fleet to individual Slack apps. Each agent has its own bot identity, and each authorized person has a separate private conversation with that app. Shared channels can be added after a private-DM pilot works.

Fleet must supply the running agent, inbound listener, identity checks, conversation routing, durable records, messaging tools, scheduler, and action approvals. The templates in this repository configure a supported installation; they do not add missing runtime features. Check [compatibility](compatibility.md) against your installed version before copying configuration.

The public runtime reviewed in that compatibility guide has gaps in end-to-end threads, `app_mention` handling, and attachment downloads. This guide describes the intended workflow and the checks needed to reach it. Do not promise those features from the templates alone. A basic text-DM connection still needs its own startup and access tests.

## What daily use looks like

- **Private requests:** Open an agent's app conversation and send a message without an @mention. Keep follow-ups for the same issue in that issue's thread.
- **Shared status:** In an approved department channel, select the actual agent from Slack's @mention picker and ask for status. The answer stays in a thread under that question.
- **Actions and approvals:** Use the appropriate private DM case thread. The agent applies the existing business roles, spending limits, holds, and approval process.
- **Human decisions:** Agents send proactive DMs when they need a decision, approval, go-ahead, or missing information. Routine reports belong in agreed channels.

The first pilot uses one existing agent, one authorized person, and a private DM. Add channels, more people, files, and scheduled reports only after their capabilities are checked.

## 1. Inspect the installed Fleet

Identify the installation you will actually change, including its version or commit, active instance, configuration locations, running agent identifiers, and documented restart procedure. Inspect existing Slack apps and routing before creating replacements. Keep a private record of the current configuration so that a failed pilot can be rolled back.

Record the following without recording secrets:

| Item | What to establish |
|---|---|
| Pilot agent | An existing agent with an appropriate role and working Fleet process |
| Slack app | One app reserved for that agent; identify any existing listener using it |
| Workspace and people | Correct workspace ID and explicitly authorized member IDs |
| Existing transport | Current routing, listeners, and any reports already sent through other services |
| Configuration loading | Which runtime reads which files, and when changes take effect |
| Action authority | Who may request actions, approve proposals, and authorize spending |
| Recovery | How to stop only the pilot listener and restore its previous configuration |

An app shared by independent agents needs an explicit migration plan. With multiple Socket Mode connections for the same app, Slack may deliver a payload to any connection; it does not promise to copy that payload to each agent. This guide therefore uses a separate app, bot token, and app-level token for each agent. A central dispatcher would require a different design. See [Slack's connection behavior](https://docs.slack.dev/apis/events-api/using-socket-mode/#using-multiple-connections).

### Check capabilities before configuring them

Use the installed runtime's documentation or source, then verify behavior with harmless messages. A feature in another Fleet version does not establish support in yours.

| Capability | Check before relying on it |
|---|---|
| Separate app per agent | The agent loads its own app and bot credentials, and receives messages as that identity. |
| Private DMs | The listener accepts `message.im` and the person's DM conversation ID. A DM-only agent can start without adding an unrelated shared channel. |
| Restricted conversations and people | Both the conversation and the sender's workspace/member pair are checked before input reaches the agent. Establish the behavior when routing is missing, malformed, empty, or unreadable. |
| Routing format | Confirm whether this version reads `slack.json`, its exact schema, and its location. Some versions use older single-channel bindings. |
| Threads | Inbound thread identifiers reach the agent, and its actual outbound tool can send with the correct parent timestamp. A helper in source does not prove the agent's tool exposes it. |
| Channel mentions | Confirm an `app_mention` handler or a documented message-event path that recognizes the bot's Slack identity. An event subscription alone does not add a handler. |
| Quiet channels | Distinguish a behavioral instruction to stay quiet from a runtime filter that keeps ordinary channel traffic away from the model. |
| Duplicate delivery | Retries and overlapping event subscriptions result in one reply or action. Establish the scope of deduplication across listeners and restarts. |
| Attachments | A supported handler actually downloads authorized file content, with clear type/size limits and failure reporting. Receiving `file_share` metadata is insufficient. |
| Thread context | The runtime can retrieve permitted prior messages, or durable case notes supply a current summary. Thread placement alone does not load history. |
| Persistence | Routing, rules, and case-to-thread records survive the documented agent restart. |
| Reports | A real Fleet scheduler job can deliver once to the intended conversation and avoid duplicate delivery through another transport. |

If the private-DM or access restrictions required for the pilot are unsupported, resolve that compatibility gap before connecting it. Keep optional capabilities out of scope until they are supported. Do not add broad access or an unrelated public channel to work around a startup limitation.

For the public revision documented in [compatibility](compatibility.md), check these additional constraints:

- Inbound startup requires `config.json`'s `slack_watch.channel`; an environment value named `SLACK_CHANNEL` does not start the listener by itself. The primary conversation must also be permitted by routing.
- Socket Mode requires a runtime with a native WebSocket implementation; the reviewed version uses it with Node.js 22 or later. Its older polling fallback watches only the primary conversation and does not establish multi-conversation coverage.
- A separate `trusted_slack_users` handle check follows the workspace/member routing check. Configure it explicitly; an undefined or empty list in that reviewed version allows all handles through that additional gate.
- Missing **or malformed** `slack.json` can fall back to a legacy binding. Validate before restart, and verify the loaded route. Do not call that behavior a universal fail-closed policy.
- The normal message path does not preserve the inbound thread parent through to the agent, and the normal outbound API/tool does not expose the required parent timestamp. An event interface containing `thread_ts` is insufficient.
- The reviewed listener does not handle `app_mention`, and attachment events do not trigger content downloads. Adding subscriptions or scopes cannot implement those features.

Recheck these constraints against your installed version; a later runtime may differ. Any patch or adapter needed to close a gap is separate implementation work.

## 2. Define the smallest access map

Use functional roles and your existing Fleet agent IDs. Begin with just the pilot row; the other rows illustrate later expansion.

| Fleet role | Slack app | Shared channels | Authorized people | Private conversations |
|---|---|---|---|---|
| Pilot agent | Its own app | None | One pilot member | That member's DM with this app |
| Department agent | Its own app | Only its approved department channels | Designated staff for that role | A separate DM for each authorized person |
| Orchestration agent | Its own app | Private dispatch and a separate decisions channel, if needed | Explicitly chosen audiences | Separate authorized-person DMs |
| Coding agent | Its own app | None initially | Designated technical decision-makers | Separate authorized-person DMs |

Being allowed to message one agent does not grant access to every agent. A private dispatch channel and a decisions channel may have different audiences; set membership accordingly. Do not invite an orchestration app into every department channel by default.

Have the workspace owner or authorized administrator review the proposed mapping before changing access. Record the intended audience for every private channel. Keep confidential channels private and leave unrelated apps out.

## 3. Create the pilot Slack app

An authorized workspace administrator handles app installation and credentials. A setup agent can prepare the nonsecret settings, routing, and test plan.

1. Open [Your Slack apps](https://api.slack.com/apps) and create a new app in the intended workspace, using an app manifest where available.
2. Start with [dm-only-app.manifest.json](../templates/dm-only-app.manifest.json). Set the app and bot names to this agent's intended identity. Validate the manifest in Slack before installing it.
3. Keep a stable bot identity for this agent. Do not use display-name customization to simulate several independent agents behind one app.
4. Enable Socket Mode. Generate an app-level token with `connections:write` and place it in the approved secret store for this agent.
5. Under App Home, enable the Messages tab and allow people to send messages to the app. Verify that the pilot member sees a message composer.

Socket Mode connects over WebSockets and does not require a public Events API Request URL. Its app-level token is separate from the bot token. See [Slack's Socket Mode setup](https://docs.slack.dev/apis/events-api/using-socket-mode/).

The Messages settings represented in the manifest are `messages_tab_enabled: true` and `messages_tab_read_only_enabled: false`; a visible tab can still be read-only. An ordinary app-and-DM connection does not require enabling Slack's separate AI app experience. See the [app manifest reference](https://docs.slack.dev/reference/app-manifest/).

### Choose events and scopes for supported behavior

The DM pilot needs the bot event `message.im`. Subscribe under **bot events**, rather than user events. DMs are not delivered through `app_mention`, even when the message contains a mention. See [DM events](https://docs.slack.dev/reference/events/message.im/) and [app mention events](https://docs.slack.dev/reference/events/app_mention/).

The DM-only template includes `users:read` because the reviewed Fleet runtime calls `users.info` to resolve the sender's handle for its trusted-user check. Without that permission, an explicit trusted-handle list can reject otherwise authorized DMs. Keep the permission for this runtime; do not clear the trusted list to bypass the failure. See [Slack's users.info method](https://docs.slack.dev/reference/methods/users.info/).

| Permission or event | Add for |
|---|---|
| `chat:write` | Sending messages as this bot |
| `im:history` and `message.im` | Receiving the bot's private-DM messages |
| `files:read` | Supported downloading of files shared where the bot has access; omit if attachments are out of scope |
| `im:write` | A supported setup method that opens DMs programmatically |
| `app_mentions:read` and `app_mention` | Channel mentions, after confirming the runtime handles them |
| `channels:read` / `channels:history` | Public-channel discovery or history/event access required by the installed adapter |
| `groups:read` / `groups:history` | Corresponding access to private channels the app has joined |
| `message.channels` / `message.groups` | Broader public/private channel events that the chosen adapter actually requires |
| `users:read` | Member lookup required by the installed integration |
| `reactions:write` | An optional, supported status-reaction workflow |

Check the [Slack scope reference](https://docs.slack.dev/reference/scopes/) for each permission you use. Receiving attachments and sending attachments are separate capabilities; grant upload permissions only for a supported outgoing-file workflow. Do not add broad administrative, group-DM, auto-join, or unrestricted public-posting scopes by default.

### Install and save credentials

Install the app in the intended workspace and complete its administrator approval requirements. After changing OAuth scopes, reinstall or reauthorize as required so the installation has the new permissions. Recheck the saved bot events and effective scopes. See [Slack's app setup guide](https://docs.slack.dev/app-management/quickstart-app-settings/).

Store the current Bot User OAuth Token and the app-level token through your approved local secret-handling method. Never paste actual tokens into chats, issue trackers, shared documents, screenshots, or source control. Each app's tokens must be available only to the intended agent/listener and administrators who manage it.

## 4. Connect the app to the pilot agent

Use [agent.env.example](../templates/agent.env.example) as a list of example environment keys, not an instruction to replace your agent's entire configuration. Confirm which names and storage method your runtime loads. Typical Socket Mode integrations require `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN`.

For the reviewed public runtime, merge the relevant fields from [agent.config.fragment.json](../templates/agent.config.fragment.json) into the existing agent `config.json`. Preserve its other fields. Set `slack_watch.channel` to the pilot's actual primary conversation ID, and set the separate `trusted_slack_users` list to the authorized person's exact Slack handle in the format the runtime expects. These handle values are separate from the workspace/member IDs in `slack.json`. The primary conversation also belongs in the routing allowlist. Do not rely on an `SLACK_CHANNEL` environment entry as a substitute for the required watch configuration.

A primary conversation setting is not a complete access policy. A filled-in environment file also does not prove that the running process has loaded it. Follow the installed version's documented loading and restart procedure.

### Apply conversation and sender restrictions

For a version that supports the example schema, adapt [slack.example.json](../templates/slack.example.json) into the agent's documented `slack.json` location. Keep it separate from secrets. Replace every placeholder and validate its JSON.

- `allowed_channels` lists approved Slack conversation IDs, including the pilot person's actual DM ID.
- `allowed_users` lists the permitted workspace/member identity pairs in the format this runtime expects.
- `display_name`, if supported, must match the identity allowed by the installed Fleet.

Confirm the actual parser and enforcement in your version. Do not assume these example field names work everywhere. If another supported configuration format supplies equivalent restrictions, follow that format and document the mapping.

Both checks must pass: the conversation is allowed **and** the sender is allowed. Slack channel membership alone does not authorize commands. A permitted sender must also hold the business role needed for the requested action.

In the example schema, the sender list is agent-wide rather than a separate list for each conversation. Preserve private-channel audiences through channel membership as well as routing. Establish whether the installed adapter further binds each person's DM to that person, and test that isolation.

Some installations fall back to a legacy binding when `slack.json` is absent. Missing routing is not automatically a denial. Validate the loaded route and observe rejection of unauthorized input; do not infer security from the existence of a file.

### Establish the first DM

1. Have the pilot member open this app's Messages tab and send a harmless discovery message, or use an administrator-approved DM-opening method supported by your integration.
2. Obtain that exact app/person DM conversation ID using a supported discovery tool or Slack API method. A first message may be rejected until the route is allowed.
3. Add that DM ID and the pilot member's workspace/member pair to the pilot agent's routing. Do not disable restrictions globally to discover the ID.
4. Load the configuration using the documented procedure for this agent. Confirm that only the intended listener uses this app's credentials.
5. Send a fresh plain DM after routing is active. Observe a reply from the intended bot in the same conversation.

Each person has a different DM with each app. Do not reuse a DM ID from another person or another agent. Verify DM-only startup directly; a listener that still requires a shared-channel binding needs a compatibility decision before this pilot can proceed.

## 5. Persist the operating rules

Adapt [agent-rules.md](agent-rules.md) to the pilot's role and save the rules in Fleet's normal durable agent instructions. Preserve existing authority and approvals. Record an issue's conversation ID and parent message timestamp in durable case notes so replies can return to the correct person's thread after a restart.

Confirm the outbound tool actually used by the agent accepts the thread parent. If it cannot send threaded replies, record that limitation and resolve it before claiming the one-issue-per-thread workflow works. Likewise, do not promise earlier thread context unless retrieval or current durable summaries are available.

## 6. Verify the private pilot before expanding

Run the [verification checklist](verification.md) with harmless content. At minimum, observe a plain DM, a threaded follow-up, rejection of an unauthorized sender or conversation through a controlled test, and continued correct behavior after restarting the intended agent. Keep the configured state and the observed result in separate columns.

Do not treat an online indicator, successful authentication, or one outbound test message as proof of inbound routing, threads, approvals, or persistence. Record unsupported capabilities as unsupported and untested ones as untested.

## 7. Add channels, people, and optional features gradually

For department channels, start from [department-app.manifest.json](../templates/department-app.manifest.json) and remove events and scopes your chosen adapter does not need. Confirm mention handling first. Invite only the relevant app to each approved channel, add its conversation ID to routing, and verify one threaded response to a real Slack @mention.

The rule to answer only when mentioned governs agent behavior. If broad `message.channels` or `message.groups` subscriptions are enabled, ordinary messages may still reach the listener and model. A technical requirement to prevent that input needs an implemented, tested runtime filter. A subscription to `app_mention` does not repair an adapter that ignores that event. If overlapping subscriptions are required, verify one reply for the same mention.

Add a second authorized person as a separate route and test both people's DMs independently. Keep their thread records and private information separate. A shared agent memory does not become isolated merely because Slack has separate conversations.

Enable attachments only after confirming downloads and failure reporting. Add scheduled reports as actual Fleet scheduler jobs, with your chosen days, times, timezone, and audience. Reuse existing reporting work where possible and verify a normal scheduled delivery appears exactly once. Event subscriptions do not schedule reports.

## Troubleshooting

| Symptom | Check |
|---|---|
| Messages tab is visible but cannot accept a message | App Home's message-composer/read-only setting |
| Agent can send but never answers | Running listener, Socket Mode credentials, saved bot events, allowed conversation and sender |
| DMs fail while channels work | `message.im`, `im:history`, exact app/person DM ID, DM-only startup requirements |
| Channel @mention does nothing | Actual bot mention, app membership, event handler, effective scope, and both route checks |
| Replies come from the wrong agent or disappear | Shared app credentials, unintended listeners, wrong agent environment |
| Mention produces two replies | Overlapping events, retry handling, multiple listeners, deduplication scope |
| Agent answers ordinary channel chat | Durable rules and whether a technical mention filter exists |
| Reply leaves the issue thread | Parent timestamp reaches the outbound tool and durable case record |
| File caption arrives but content does not | Supported downloader, file access, effective scope, size/type limits, explicit error reporting |
| Unauthorized input is accepted | Loaded routing format, legacy fallback, identity check, and separate action authority |
| Reports repeat | Existing jobs and other transports delivering the same report |

Resolve the specific route or runtime gap instead of widening access to every person or channel. Record what is configured, what was actually observed, and what remains to be implemented in the [verification record](verification.md).
