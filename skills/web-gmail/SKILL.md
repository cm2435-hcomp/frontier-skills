---
description: Drafting emails in Gmail (web UI).
name: web-gmail
url_pattern: ^https://mail\.google\.com
---

## General

When searching for emails, always use Gmail search operators to target the correct field: `from:` for sender, `to:` for recipient (e.g. `from:sender@example.com`, `to:me@example.com`). Never search by name alone — that matches anywhere in the email (subject, body, other fields), leading to false positives and accidental deletions.

## Drafting replies

Drafts are autosaved — simply reply and type. No need to explicitly save.

Sign off every draft with the user's first name, inferred from the Gmail profile icon or the "From" field.

Before drafting a reply, MUST open the conversation and read at least the latest message. Then apply these rules to decide whether to draft a reply — these rules do NOT apply to summarising or reading emails:

* If the email is automated or machine-generated — skip drafting. This includes: notifications (GitHub, CI, JIRA, Ashby, LinkedIn), calendar invites/updates, system alerts, transactional emails (receipts, shipping, reminders), marketing emails, and any sender with a `noreply` address or bot-like name.
* If the email was sent to a mailing list and the user is not in To/CC — skip drafting.
* If the greeting addresses someone else by name — skip drafting.
* If the user sent the last message — skip drafting. Do not reply to yourself.
* Only draft when a real person sent a message directly to the user expecting a response. If uncertain, skip drafting.

When summarising or digesting emails, include ALL unread conversations — automated, transactional, and human alike. The skip rules above apply exclusively to drafting replies.
