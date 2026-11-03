#!/usr/bin/env python3
"""Check the published setup kit without connecting to a member's installation."""

import json
import re
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parent.parent
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


def read_json(relative):
    try:
        return json.loads((ROOT / relative).read_text())
    except (OSError, ValueError) as exc:
        errors.append(f"{relative}: {exc}")
        return {}


for profile in ("department", "dm-only"):
    relative = f"templates/{profile}-app.manifest.json"
    manifest = read_json(relative)
    home = manifest.get("features", {}).get("app_home", {})
    require(home.get("messages_tab_enabled") is True, f"{relative}: Messages tab must be enabled")
    require(home.get("messages_tab_read_only_enabled") is False, f"{relative}: Messages tab must accept messages")
    settings = manifest.get("settings", {})
    require(settings.get("socket_mode_enabled") is True, f"{relative}: Socket Mode must be enabled")
    events = set(settings.get("event_subscriptions", {}).get("bot_events", []))
    scopes = set(manifest.get("oauth_config", {}).get("scopes", {}).get("bot", []))
    require("message.im" in events, f"{relative}: missing message.im")
    require({"chat:write", "im:history"} <= scopes, f"{relative}: missing basic DM scopes")
    require("connections:write" not in scopes, f"{relative}: connections:write is an app-level token permission")
    require(not ({"chat:write.public", "channels:join", "admin"} & scopes), f"{relative}: unexpected broad permission")
    if profile == "dm-only":
        require(events == {"message.im"}, f"{relative}: DM pilot should subscribe only to message.im")
        require(scopes == {"chat:write", "im:history", "users:read"}, f"{relative}: DM pilot needs messaging and runtime identity-lookup scopes only")
    else:
        require({"app_mention", "message.channels", "message.groups"} <= events, f"{relative}: incomplete department events")
        require({"app_mentions:read", "channels:history", "groups:history", "files:read"} <= scopes, f"{relative}: incomplete department permissions")

routing = read_json("templates/slack.example.json")
for key in ("allowed_channels", "allowed_users"):
    values = routing.get(key)
    require(isinstance(values, list) and bool(values), f"slack.example.json: {key} must be explicit and nonempty")
    if isinstance(values, list):
        require(all(isinstance(value, str) and "<" in value and ">" in value for value in values), f"slack.example.json: {key} must contain placeholders only")
        require(len(values) == len(set(values)), f"slack.example.json: duplicate entries in {key}")

config = read_json("templates/agent.config.fragment.json")
primary = config.get("slack_watch", {}).get("channel", "")
require(isinstance(primary, str) and primary.startswith("<") and primary.endswith(">"), "config fragment: primary conversation must be a placeholder")
handles = config.get("trusted_slack_users", [])
require(isinstance(handles, list) and bool(handles) and all(isinstance(item, str) and item.startswith("<") and item.endswith(">") for item in handles), "config fragment: explicit placeholder Slack handles required")

for path in sorted(ROOT.rglob("*.md")):
    if ".git" in path.relative_to(ROOT).parts:
        continue
    text = path.read_text()
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip().strip("<>").split("#", 1)[0]
        if not target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            continue
        destination = (path.parent / unquote(target)).resolve()
        require(destination.is_relative_to(ROOT), f"{path.relative_to(ROOT)}: link leaves repository: {target}")
        require(destination.exists(), f"{path.relative_to(ROOT)}: missing link target: {target}")

env_path = ROOT / "templates/agent.env.example"
if env_path.exists():
    for line in env_path.read_text().splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition("=")
        require(bool(separator) and re.fullmatch(r"REPLACE_WITH_[A-Z0-9_]+", value) is not None, f"agent.env.example: {key} must have a REPLACE_WITH placeholder value")
else:
    errors.append("Missing templates/agent.env.example")

if errors:
    print("Setup kit validation failed:")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("Setup kit validation passed: manifests, routing/config placeholders, environment example, and local document links.")
print("Live Slack settings, credentials, routing, and delivery were not tested.")
