# Troubleshooting

Start with [compatibility](compatibility.md) and confirm the installed build contains the [runtime changes](https://github.com/noogalabs/ascendops/tree/b016f1fa6544609872674fced9c40a6d9440f841) submitted in [PR #77](https://github.com/noogalabs/ascendops/pull/77). Separate app settings, OAuth scopes, secret loading, routing, and observed delivery when diagnosing a failure.

| Symptom | Check |
|---|---|
| Messages tab cannot accept input | Enable the App Home Messages tab and disable its read-only setting. |
| Routed Slack startup is blocked | Check native WebSocket support, both app credentials, valid routing, and an allowed primary conversation. Routed mode requires Socket Mode and does not silently poll one conversation. |
| Credentials exist globally but startup is still blocked | A present routed-agent `.env` needs its own complete nonblank pair. Fix missing keys or the unreadable file; ambient values do not fill gaps. |
| Listener starts for the wrong conversation | Primary precedence is `slack_watch.channel`, then `SLACK_CHANNEL`, then the first allowed routing conversation. Remove stale explicit overrides and keep the selected ID allowed. |
| A second agent's listener is blocked | Give it a separate Slack app and credentials. Same-daemon app-token ownership refuses a second listener; coordinate other daemon instances separately. |
| Agent can send but never answers | Check Socket Mode, `message.im`, saved subscriptions/scopes, routing load, workspace/member identity, and the separate trusted handle. |
| DMs fail while channels work | Check `message.im`, `im:history`, that exact app/person DM ID, route membership, and `users:read` for handle resolution. |
| A channel mention gets no response | Select the actual app mention; check app membership, `app_mention` and `app_mentions:read`, route/trust checks, and the intended bot identity. |
| An unmentioned urgent post is not seen | Default mention-only filtering excludes it before the model. An approved monitoring workflow needs a deliberate agent-wide opt-out and narrow conversation access; durable emergency rules cannot act on filtered input. |
| Ordinary channel chat reaches the agent | Check `channel_mentions_only`; `false` is an explicit opt-out affecting all this agent's allowed non-DM conversations. Keep its quiet-channel rules in place. |
| A private channel fails | An authorized member must invite this app. Check private-channel scopes/events and its allowed conversation ID. |
| Replies start new top-level messages | Use the preserved parent with `send-slack --thread-ts`. Save the new-parent `ts` from a proactive send receipt with the correct person/case/conversation. |
| Reply uses the wrong person's case | Check the durable person/conversation/parent mapping. Separate DMs do not automatically isolate shared model memory. |
| Permission error follows a scope change | Reinstall or reauthorize and verify effective scopes and the current app's token. |
| File caption arrives without content | Check `files:read`, authorized access, approved HTTPS `files.slack.com` URL, and explicit inbox errors. Limits are four files, 10 MiB each, 20 MiB total. External URLs are not fetched. |
| Old downloaded files remain | Successful downloads persist in private state storage. Apply the installation's retention policy; this kit supplies no automatic expiry. |
| Malformed routing stops Slack | Fix and validate the policy, then restart. An invalid existing file refuses startup/sends; do not remove it to recover less restricted legacy access. |
| An excluded route is accepted | Confirm the intended agent/build and loaded policy. Check both workspace/member and conversation restrictions, plus separate business authority. |
| Mention gets duplicate replies | Check overlapping subscriptions, multiple daemon instances, and the bounded deduplication window. Cross-restart exactly-once behavior is not guaranteed. |
| A message disappears after a failure or crash | Envelopes are acknowledged before durable inbox completion; no guaranteed crash replay exists. Reconcile the case with business records before controlled retries. |
| Reports repeat | Check duplicate scheduler jobs and delivery through other transports. Observe a normal scheduled run after the fix. |

Fix the specific failed setting or capability instead of allowing every person or channel. Keep redacted observations in the private [verification record](verification.md), then retest the affected path.

Return to [setup](setup.md) or the [README](../README.md).
