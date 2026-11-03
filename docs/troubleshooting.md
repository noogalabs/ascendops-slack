# Troubleshooting

Start with [compatibility](compatibility.md). Separate Slack app settings, installed OAuth permissions, Fleet routing, and the running listener when diagnosing a failure.

| Symptom | Check |
|---|---|
| “Sending messages to this app has been turned off.” | Enable the Messages tab and allow users to message the app; check that it is not read-only. |
| The agent sends messages but never answers. | Check Socket Mode, the app-level token, event subscriptions, the installed listener, and the actual runtime startup setting. |
| DMs fail while channels work. | Check `message.im`, installed `im:history`, this person's DM ID for this app, sender routing, and DM support in your runtime. |
| A channel mention gets no response. | Check the actual app mention, membership, installed scope, subscribed event, and whether the adapter handles that event. |
| A private channel fails. | An authorized member must add the app. Check private-channel events/scopes and the allowed channel ID. |
| Replies appear under the wrong identity or messages disappear intermittently. | Check for shared app credentials, competing listeners, and the wrong agent environment. Use one app per agent for this arrangement. |
| A mention gets two answers. | Check overlapping message and mention events, duplicate listeners, and runtime deduplication. |
| The agent answers ordinary conversation. | Check its durable rules and whether the adapter actually enforces a technical mention filter. A prompt alone does not stop event delivery. |
| Replies become new top-level messages. | Confirm that inbound parent timestamps reach the agent and its outbound tool accepts and uses the parent timestamp. |
| Permission errors follow a scope change. | Reinstall the app and verify its effective installed scopes and current token. |
| A file caption arrives without its contents. | Check `files:read`, the runtime's authenticated downloader, access to the file, supported types, and size limits. A file event alone is not a download. |
| An excluded sender or conversation is accepted. | Confirm the routing file was parsed and loaded. Investigate any legacy fallback and keep business authority checks separate from transport access. |
| Reports appear more than once. | Check existing scheduler jobs and duplicate delivery across transports. |

Keep the scope of a fix narrow. Identify the missing permission, ID, event handler, or runtime capability rather than allowing every user or channel. Preserve redacted evidence of the result in your private verification record.

Return to the [setup guide](setup.md) or [README](../README.md).
