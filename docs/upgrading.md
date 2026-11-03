# Upgrade to the guide-compatible runtime

Use an AscendOps build containing [the Slack runtime change](https://github.com/noogalabs/ascendops/pull/77). The supported upstream baseline is **b016f1fa6544609872674fced9c40a6d9440f841**. Downloading this setup kit alone does not update your running Fleet.

## Plan the app migration first

Keep a private copy of your current configuration and identify which agent uses each Slack app. The upgraded daemon refuses a second listener with an app token already claimed by another agent. If several agents share an app today, prepare separate apps and complete credential pairs before restarting them on the new runtime. Begin with one agent and one authorized person.

Keep your existing approval roles, durable case records, and reporting workflows. Record which reports already run through another transport so Slack does not duplicate them.

## Update the installed runtime

Use the existing AscendOps update workflow for the installation you intend to change:

```bash
node --version
ascendops update --check
ascendops update
```

Routed Slack needs native WebSocket support, normally **Node.js 22 or later**. Update the Node runtime through your normal installation procedure if needed.

The updater uses your runtime checkout's configured `upstream` remote. Confirm it points to [noogalabs/ascendops](https://github.com/noogalabs/ascendops), or a maintained fork that contains this change. If it points elsewhere, have your setup agent review that installation's update source before changing it. Follow the updater's recovery guidance if it reports conflicts or a failed build; do not treat a source download as a rebuilt runtime.

After updating, check the actual checkout and available command:

```bash
git -C <YOUR_RUNTIME_CHECKOUT> merge-base --is-ancestor b016f1fa6544609872674fced9c40a6d9440f841 HEAD
cortextos bus send-slack --help
```

The ancestry command returns success when this upstream baseline is included. A separately maintained fork may implement equivalent support; its maintainer must verify that compatibility. The send command should expose `--thread-ts`.

Use your installation's normal daemon and agent restart procedure to load the rebuilt runtime and the intended agent configuration. The update command's output describes the required restarts for its installation method. Do not restart unrelated agents merely to test the pilot.

## Apply the pilot configuration

Follow [setup](setup.md), using a separate Slack app, explicit sender and conversation restrictions, and the trusted-handle list. A present routed agent secret file must contain its own complete bot/app token pair; blank or missing values do not borrow another app's ambient credentials.

The primary conversation is chosen from `slack_watch.channel`, then `SLACK_CHANNEL`, then the first allowed conversation. Update or remove a stale legacy watch override that points outside the new allowlist. Missing or malformed routing is no longer interchangeable: an absent file retains legacy behavior, while a malformed existing file blocks Slack.

The routing template enables mention-only filtering. This is an **agent-wide** setting for all allowed non-DM conversations. For an approved workflow that must monitor unmentioned posts, choose the opt-out deliberately, narrow the allowed conversations, and retain the agent's quiet-channel and escalation rules.

## Observe the result

Run the [verification checklist](verification.md). Confirm the intended bot identity, a plain DM, a threaded follow-up, rejected unauthorized input, and persistence after restart. Add channel mentions, files, a second person, and scheduled reports only as their selected paths are observed.

Automated tests exercise the runtime with fixture Slack responses. They do not install your app, verify its saved OAuth scopes, test your workspace, isolate an agent's shared memory, or prove scheduled delivery. The existing early Socket Mode acknowledgement and in-memory duplicate window also do not guarantee replay after a process crash.

Return to the [README](../README.md).
