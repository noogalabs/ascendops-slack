# AscendOps Slack Setup

Connect your existing Fleet agents to Slack with separate bot identities, private conversations, and department channels.

This member setup kit contains a guide, reusable Slack app manifests, configuration examples, and verification steps. Run the agents with your existing [AscendOps installation](https://github.com/noogalabs/ascendops). This repository does not include an agent runtime or install a Slack adapter.

**Requires Node 22+ and an AscendOps runtime containing [the Slack guide update in PR #77](https://github.com/noogalabs/ascendops/pull/77).** Follow [upgrading](docs/upgrading.md) and the [runtime compatibility check](docs/compatibility.md) before connecting an agent. The updated runtime supports routed private DMs, channel mentions, threaded replies, and bounded attachment downloads. Verify each enabled capability in your own Slack workspace before expanding access.

## What the finished setup looks like

| Where | How you use it |
|---|---|
| An agent's private DM | Ask for work, provide missing information, and handle approvals. No mention required. |
| An issue's DM thread | Keep the proposal, decisions, and follow-ups together, with one parent per issue. |
| A department channel | Mention the relevant agent for shared status; receive a threaded answer. |
| A briefing channel | Read approved scheduled reports. |
| An internal Fleet bus | Coordinate agents without filling human channels with agent chatter. |

Give every agent its **own Slack app and credentials**. Keep each person's private DM separate. Preserve your existing approval roles and spending limits. Slack access does not grant business authority.

## Start here

1. **Update and check your runtime.** Follow [upgrading](docs/upgrading.md) and [compatibility](docs/compatibility.md). Confirm Node 22+ with native WebSocket support and a runtime containing PR #77. Identify your agent directories and current Slack settings.
2. **Choose one existing agent and one person.** An internal coding or research agent is a useful first candidate. Record the intended agent, Slack app, person, and allowed conversations before changing access.
3. **Create that agent's Slack app.** Start with the [DM-only manifest](templates/dm-only-app.manifest.json), enable Socket Mode, and generate its separate app-level token. Follow the [setup guide](docs/setup.md).
4. **Configure secrets, startup, and routing locally.** Adapt [agent.env.example](templates/agent.env.example) and [slack.example.json](templates/slack.example.json). A present per-agent secret file must contain that app's complete bot/app token pair; missing keys do not borrow ambient credentials. Merge the approved Slack handle list from [agent.config.fragment.json](templates/agent.config.fragment.json) into the existing agent configuration. Its `slack_watch.channel` is an optional explicit primary conversation: startup chooses that value first, then `SLACK_CHANNEL`, then the first allowed conversation. The selected primary must also be allowed by routing. Replace placeholders only in your private installation.
5. **Give the agent durable communication rules.** Adapt [agent-rules.md](docs/agent-rules.md) to its role and existing approval requirements.
6. **Verify what actually works.** Use the [verification checklist](docs/verification.md). Record configuration separately from observed behavior. Observe plain DMs, thread replies, denied routes, and restart behavior. Verify channel mentions and attachment handling when those capabilities are enabled.
7. **Expand from the verified pattern.** Add a department channel, then more agents and authorized people. The [department manifest](templates/department-app.manifest.json) is a starting profile; remove unused events and permissions.

Your Slack administrator may need to approve app installation. Keep bot and app-level tokens in your installation's private secret configuration. Do not put tokens, private DM IDs, or member records into GitHub issues, commits, or shared setup notes.

## Threads and case records

The updated listener includes the original parent timestamp in its reply command. Keep that parent when replying with `cortextos bus send-slack ... --thread-ts <PARENT_TIMESTAMP>`.

When an agent starts a new issue with `send-slack`, the command returns JSON containing the posted message's `ts`. Save that timestamp together with the conversation ID and case ID in the installation's private, durable case notes. Use the original parent for follow-ups; each reply's own timestamp does not replace it. Slack threading does not automatically load all earlier context into the model.

## Included

| Resource | Purpose |
|---|---|
| [Setup guide](docs/setup.md) | App settings, permissions, routing, private DMs, channels, and reporting. |
| [Upgrading](docs/upgrading.md) | Install the runtime update required by this setup kit. |
| [Compatibility](docs/compatibility.md) | Check the runtime before selecting a setup profile. |
| [Agent rules](docs/agent-rules.md) | Durable instructions for channels, DMs, approvals, and notifications. |
| [Verification](docs/verification.md) | Record what was configured and what was observed. |
| [Troubleshooting](docs/troubleshooting.md) | Common symptoms and the settings or capabilities to inspect. |
| [Setup-agent prompt](docs/setup-agent-prompt.md) | Copyable instructions for an agent helping with your installation. |
| [Templates](templates/) | Two Slack app profiles, private routing, and an environment example. |

## Contributing

Open an issue or pull request with a proposed improvement. Include your runtime version and a redacted description of the behavior. Use placeholders for workspace, member, channel, and conversation IDs. Describe an observed result accurately; a connected indicator or successful outbound message does not prove the inbound route works.

For template changes, validate the manifest in Slack before installation and run the repository checks:

```bash
python3 tools/validate.py
```

The checks validate the published templates and local document links. They do not connect to Slack, inspect your credentials, or verify a live installation.

## References

Slack's official documentation: [app manifests](https://docs.slack.dev/reference/app-manifest/), [App Home and messages](https://docs.slack.dev/surfaces/app-home/), [Socket Mode](https://docs.slack.dev/apis/events-api/using-socket-mode/), and [OAuth installation](https://docs.slack.dev/authentication/installing-with-oauth/).

Licensed under [MIT](LICENSE).
