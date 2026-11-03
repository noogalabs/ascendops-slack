# AscendOps Slack Setup

Connect your existing Fleet agents to Slack with separate bot identities, private conversations, and department channels.

This member setup kit contains a guide, reusable Slack app manifests, configuration examples, and verification steps. Run the agents with your existing [AscendOps installation](https://github.com/noogalabs/ascendops). This repository does not include an agent runtime or install a Slack adapter.

**Start with the [runtime compatibility check](docs/compatibility.md).** Slack permissions alone cannot add missing runtime features. The public runtime snapshot reviewed for this kit needs additional support to reproduce the full thread and mention behavior below.

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

1. **Check your runtime.** Follow [compatibility](docs/compatibility.md) and identify your installed version, agent directories, startup settings, routing, and supported message features.
2. **Choose one existing agent and one person.** An internal coding or research agent is a useful first candidate. Record the intended agent, Slack app, person, and allowed conversations before changing access.
3. **Create that agent's Slack app.** Start with the [DM-only manifest](templates/dm-only-app.manifest.json), enable Socket Mode, and generate its separate app-level token. Follow the [setup guide](docs/setup.md).
4. **Configure secrets, startup, and routing locally.** Use [agent.env.example](templates/agent.env.example), merge [agent.config.fragment.json](templates/agent.config.fragment.json) into the existing agent configuration, and adapt [slack.example.json](templates/slack.example.json). Replace placeholders only in your private installation, using the schema supported by your version.
5. **Give the agent durable communication rules.** Adapt [agent-rules.md](docs/agent-rules.md) to its role and existing approval requirements.
6. **Verify what actually works.** Use the [verification checklist](docs/verification.md). Record configuration separately from observed behavior. Complete the necessary runtime work before claiming that threads or channel mentions work.
7. **Expand from the verified pattern.** Add a department channel, then more agents and authorized people. The [department manifest](templates/department-app.manifest.json) is a starting profile; remove unused events and permissions.

Your Slack administrator may need to approve app installation. Keep bot and app-level tokens in your installation's private secret configuration. Do not put tokens, private DM IDs, or member records into GitHub issues, commits, or shared setup notes.

## Included

| Resource | Purpose |
|---|---|
| [Setup guide](docs/setup.md) | App settings, permissions, routing, private DMs, channels, and reporting. |
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
