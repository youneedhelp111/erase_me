<div align="right">

English | **[中文](README.md)**

</div>

<div align="center">

# erase-me.skill

**Make your AI forget you. No deleting, just sanding the details off.**

Your AI assistant may remember everything you ever told it. erase-me works inside your own account: it rewrites the details you'd rather not have remembered into vague, still-true statements that no longer reveal the original, then dilutes the memory with rounds of neutral topics.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-Compatible-blueviolet)](https://skills.sh)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![Darwin Optimized](https://img.shields.io/badge/Darwin.skill-Optimized-orange)](https://github.com/alchaincyf/darwin-skill)
[![No Fabrication](https://img.shields.io/badge/rewrites-generalize%2C_never_invent-lightgrey)](#five-principles)

```
npx skills add youneedhelp111/erase_me
```

</div>

---

> [!IMPORTANT]
> **The honest part first: dilution is not deletion.** Server logs, backups and any chats you haven't deleted are still there, and the platform decides what it finally remembers. erase-me rewrites memory entries and dilutes context; it does its best, with no guarantee. For real deletion, also delete chats and memories in the platform's settings, or file a request under the provider's privacy policy.

---

## At a glance

```
read memory → rate each entry → you confirm → rewrite, never delete → neutral dilution → keyword check → comparison sheet
```

| Before (only in your own comparison sheet) | After (what the AI remembers) |
|:---|:---|
| Asked late at night about testing for a specific condition, and said why | Asked a health-related question |
| Anxious personality, keeps double-checking | Fairly careful |
| Earns about 300k a year | Has a work income |

What goes: the condition, the reason, the time, the psychological label, the amount. Every sentence that stays is still true.

---

## Why this exists

Most AI assistants now have "memory". A question you asked one night, an income you mentioned in passing, something you said at a low point: any of it may be remembered and come back in later conversations.

Platforms usually give you two choices: keep everything, or delete entries one by one by hand. Deleted entries leave gaps, and the AI may still infer the original from what's left around them.

erase-me takes a third path: **rewrite, don't delete.** It generalizes specific details into vague statements, then dilutes the memory with topics that have nothing to do with you, until the original is no longer recognizable.

---

## Two scopes

| Scope | What it does | Good for |
|:---|:---|:---|
| **A. Blur everything** | Every memory becomes a vague statement | Leaving this AI, or lowering how much it knows overall |
| **B. Only the sensitive ones** | Highly private entries are rewritten, moderate ones are your call, the rest stay as they are | Dealing with one or two specific things |

Before starting it asks three questions at once: the scope, how many dilution rounds (default 10, max 100, 0 for none), and whether to create the Excel comparison sheet. You can also just say "you decide".

---

## Five principles

| # | Principle | What it means |
|:---|:---|:---|
| 01 | **Rewrite, never delete** | Sensitive entries are changed with "update", not deleted; if a platform can only delete, it asks you first |
| 02 | **Generalize, never invent** | Every rewritten sentence must still be true; no new facts, no fake identity |
| 03 | **Never repeat** | In the list it shows you, highly private originals appear only as "(not repeated)" |
| 04 | **Nothing changes until you confirm** | Reading memory is read-only; nothing is edited until you say "confirm" |
| 05 | **No impersonation, no overreach** | Dilution rounds are written in the assistant's own voice, never yours; no instructions are written into memory; if the AI refuses a step, it stops and tells you why instead of working around it |

---

## The full flow: 7 steps

| Step | What happens | Key point |
|:---|:---|:---|
| 1 | Gather needs | Scope, dilution rounds, comparison sheet; if your wording already says it, it just confirms |
| 2 | Check where it runs | Only works in a web / app chat with memory on; in a command line it tells you to move |
| 3 | Read memory, list it | Read-only; each entry numbered, categorized and rated (highly private / moderate / none) |
| 4 | Write the rewrite plan, confirm | Rewrites may not contain the original's keywords, people, times or places |
| 4.5 | First write to the sheet | Before rewriting, the original memories go into Excel |
| 5 | Rewrite | With a memory tool, each entry is updated and then re-checked |
| 6 | Neutral dilution | Astronomy, cooking, history, math puzzles… never about you, never touching the rewritten topics; in chat, each reply runs a batch of 5–10 rounds and you send "continue" for the next |
| 7 | Verify and wrap up | Keywords from each original are searched in memory and in the AI's self-description; second write to the sheet |

---

## Excel comparison sheet (optional)

Written twice to the same file, with 4 sheets: **original memories**, **modified memories**, **comparison** (original and rewrite side by side) and **checks** (whether each keyword is still there).

- You choose where it's saved, and it can be password-protected (automatic if `msoffcrypto-tool` is installed, otherwise it tells you how to set one in Excel)
- `scripts/memory_report.py` uses only Python's standard library, reads data from stdin and leaves no temp files

> [!WARNING]
> **The sheet itself is a plaintext record of the original content.** However clean the cloud gets, anyone who finds this file on your computer can read it. Skip it if you don't need it; if you do, add a password, keep it somewhere only you know, and delete it (and empty the Recycle Bin) right after reading.

---

## What it can and can't do

| | ✅ Can | ❌ Can't |
|:---|:---|:---|
| Account memory | Rewrite entries directly when the platform offers a memory-editing tool | Without one, it can only tell you how to edit them in settings |
| Neutral dilution | Add more content unrelated to you | Delete chat history, server logs or backups |
| Where it runs | Web / app chats with memory on | Command-line or editor agents (those sessions don't reach account memory) |
| Cost | You set the rounds, and it stops there | Run for free: each dilution round costs a few hundred tokens |

### Why do you have to send "continue"?

A chat AI can only answer one message at a time; it can't keep replying on its own. So erase-me runs one batch (5–10 rounds) per reply and ends with a progress line such as `batch 3/10 done`. Send "continue" and it runs the next batch.

- **Rewriting is the main lever**: when the platform has a memory-editing tool, the sensitive entries are fixed in one pass and dilution is only a supplement; 0–5 rounds is usually enough
- **Agent environments** (e.g. Claude Code with an account-memory tool) can run every round in one reply through tool calls
- No scripts, no API, no extra accounts, and no automation sending "continue" for you: those break the platform's terms

---

## Quick start

**Claude web / app**: zip the repo and upload it as a skill under Settings → Capabilities (your plan needs to support custom skills).

**Command-line tools** (Claude Code, Codex, etc.):

```bash
npx skills add youneedhelp111/erase_me
```

**Platforms without skills** (e.g. ChatGPT): open a new chat, paste the full `SKILL.md`, and say "follow this".

Then, in a chat with memory on, say:

- "Erase me"
- "Blur that thing I asked last week, then dilute 10 rounds"
- "Forget me"

When it's done, delete that conversation too.

**Haven't deleted the chats yet?** Optional, the skill runs either way: in Claude, sidebar "…" → Delete, and Settings → Privacy / Memory; in ChatGPT, sidebar "…" → Delete (check archived chats too), and Settings → Personalization → Memory → Manage. Chat titles can give things away on their own.

---

## Evolved with Darwin

This skill was refined with the [Darwin.skill](https://github.com/alchaincyf/darwin-skill) process:

- Real scenarios run in a sandbox on fake memory, compared against a control run without the skill
- Every change was blind-compared before vs after by **3 independent judges**, and kept only on a majority
- Every kept round passed 3:0 or 2:0; after each change of requirements, the sandbox tests were re-run

The full log is in [darwin/results.tsv](darwin/results.tsv) and the test cases are in [test-prompts.json](test-prompts.json).

---

## License

MIT

---

<div align="center">

**You can't take back what you said,<br>but you can make it stop being specific.**

<br>

If it helps, a ⭐ helps others find it.

</div>
