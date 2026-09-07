# Message release review handoff

Release/version: ____  Owner: ____  Reviewer: ____  Date: ____

Actual application/template engine and version: ____

Source locale: ____  Target locales: ____  Formats: ____

## Before running checks

- [ ] Confirm permission to process the exported material.
- [ ] Replace real recipients, secrets, order data and internal URLs with synthetic equivalents.
- [ ] Confirm the checker's placeholder syntax matches the actual renderer.
- [ ] Record expected required keys, optional keys and fallback behavior.
- [ ] Record sample-data field names and types.

## Review results

- [ ] Compare required keys across locales.
- [ ] Compare variables, including spelling and repeated occurrences.
- [ ] Check template variables against the declared sample schema.
- [ ] Render representative samples using the actual application renderer.
- [ ] Inspect links and visible output without sending to real recipients.
- [ ] Separate multiple rule findings caused by the same defect.
- [ ] Have a qualified content owner review meaning and translation quality separately.

## Close the handoff

| File/key | Actual output | Expected output | Correction | Rerun evidence | Remaining limit |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

- [ ] Retest after changes; do not hide defects by changing severity or approval state.
- [ ] Record unresolved checks and unsupported formats.
- [ ] Keep delivery testing, client rendering compatibility and live URL checks separate.

This checklist is a process aid, not compliance certification or a guarantee of error-free messages.
