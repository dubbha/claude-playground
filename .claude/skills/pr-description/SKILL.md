---
name: pr-description
description: Writes pull request descriptions. Use when creating a PR or when the user asks to summarize changes for a pull request.
allowed-tools: Bash(git fetch:*), Bash(git diff:*), Bash(git log:*), Bash(git status:*), Bash(git show:*), Bash(git branch:*)
model: haiku
---

When writing a PR description:

1. Run `git fetch origin main` first so you compare against the latest main. A stale main hides squash merges. Use `origin/main` (not the local `main`, which `git fetch` does not update) for every comparison below.
2. Run `git diff origin/main...HEAD` and `git log origin/main..HEAD --oneline` to see the branch's changes. Describe only what's new since the branch was last merged into main.
   - Squash merges leave the branch's old commits in the diff. Check `git log origin/main --oneline -20` for a squash commit matching earlier work on this branch (same title, `(#123)` reference, or files). If found, diff from the last merged branch commit instead: `git diff <commit>..HEAD`.
   - If unsure, use `git diff origin/main HEAD` (two dots), or ask the user where to start.
3. Write a description following this format:

## What
One sentence explaining what this PR does.

## Why
Brief context on why this change is needed.

## Changes
- Bullet points of specific changes made
- Group related changes together
- Mention any files deleted or renamed
