# Verify the Slack connection

[Repository overview](../README.md) · [Setup guide](setup.md) · [Runtime compatibility](compatibility.md) · [Agent rules](agent-rules.md)

Begin with one agent, one authorized person, and a private DM. Use harmless test content and the installed runtime's supported tools. Coordinate any negative-access tests with the administrator and test participants; use no sensitive information.

Read [compatibility](compatibility.md) first. The reviewed public runtime does not provide the intended thread workflow, `app_mention` handler, or attachment downloader. Mark those capabilities **unsupported** unless your installed version or a separately implemented adapter closes the gaps and passes the checks below.

Record the Fleet version, app/agent mapping, test date, and who performed the checks in your own private setup record. Keep tokens and private conversation content out of the public repository. A connected indicator or a successful outbound send proves only that particular step.

## Private-DM pilot

- [ ] This agent has its own app credentials, and only its intended listener uses them.
- [ ] The required primary watch conversation and explicit trusted-handle list are configured for the installed runtime. The primary conversation is also permitted by routing; its startup does not depend on an unrelated shared channel.
- [ ] Socket Mode or the documented polling path actually covers every conversation you intend to support. A single-primary-conversation polling fallback does not verify additional DMs or channels.
- [ ] An authorized plain DM receives a reply from the intended bot in that same DM, without an @mention.
- [ ] A follow-up stays under the correct parent message. A separate issue uses its own parent.
- [ ] A controlled unauthorized-sender test is denied; an unapproved conversation is also denied. Observe the routing outcome rather than inferring denial from silence.
- [ ] Routing validates before restart and the runtime confirms it loaded. Check the installed version's missing/malformed-file behavior instead of assuming a denial; the reviewed version can fall back to a legacy binding.
- [ ] The existing action-approval path still applies in the DM. Do not perform a real consequential action just to test it.
- [ ] Restarting only the intended agent preserves routing, durable rules, and correct case-thread replies.

If the runtime cannot support the pilot's DM, restrictions, or thread workflow, record the limitation and resolve it before expanding.

## Expansion checks

- [ ] A real channel @mention receives one threaded status answer; mentioning another agent produces no response from this one.
- [ ] Ordinary channel chat produces no unsolicited reply. Separately record whether a runtime filter blocks that input or the agent merely follows a behavior rule.
- [ ] A channel action request is redirected to the proper private DM and approval path.
- [ ] A second authorized person's DM works independently. Replies, thread records, and private context remain with the correct person.
- [ ] Duplicate delivery or overlapping subscriptions produce one reply/action in a controlled test.
- [ ] If attachments are promised, a small supported file is actually downloaded and understood; a failed download is reported accurately.
- [ ] If reports are promised, a normal scheduled run appears once in the intended channel at the agreed time and timezone.

## Keep configuration separate from observation

Fill this table in your private setup record. Use **yes**, **no**, **unsupported**, or **not tested**; include a short nonsecret observation or test reference. “Configured” alone is not a pass.

| Capability | Configured? | Actually observed? | Evidence or remaining gap |
|---|---|---|---|
| Separate app and intended listener | | | |
| Plain authorized DM | | | |
| Conversation and sender restrictions | | | |
| Correct case-thread replies | | | |
| Existing approval controls | | | |
| Persistence after restart | | | |
| Channel mention response | | | |
| Quiet ordinary channel behavior | | | |
| Technical filtering of unmentioned channel input | | | |
| Separate second-person DM and context | | | |
| Duplicate-event handling | | | |
| Attachment content download | | | |
| Normal scheduled delivery | | | |

Summarize the result as: **configured**, **observed working**, **unsupported**, and **still untested**. Name the audience and capabilities actually tested. Expand from the verified pilot rather than declaring every agent ready from one successful connection.
