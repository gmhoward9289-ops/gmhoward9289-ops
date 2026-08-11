# George M. Howard

I build small, sharp tools in the open — mostly terminal programs for watching
AI coding agents work, plus a few projects that exist to make a number
defensible instead of merely plausible.

Everything here is MIT, single-purpose, and installable without a build step.
Write-ups live at **[blog.swamplink.com](https://blog.swamplink.com)**.

---

## The flock — watching a fleet of coding agents

Three sibling TUIs. They share a premise: once you are running more than a
couple of agents at once, the expensive failures are the ones you cannot see —
a session about to hit its context limit, two sessions quietly destroying each
other's uncommitted work in the same checkout, a red build scrolling out of
view. All three are read-only by construction and degrade to a labelled gap
rather than an error when a data source is missing.

| | what it answers | install |
|---|---|---|
| **[roost](https://github.com/gmhoward9289-ops/roost)** | *What are the models doing?* Every live Claude Code session, its model, its context burn — and **the subagents it spawned**, which nothing that watches pids can see. | `brew install gmhoward9289-ops/tap/roost` · `pipx install roost-top` · `npm i -g roost-top` · apt |
| **[leghorn](https://github.com/gmhoward9289-ops/leghorn)** | *What are the repos doing?* Sessions joined to real git state, GitHub CI and open PRs with failures pinned until green, and a commit feed across every repo. | `brew install gmhoward9289-ops/tap/leghorn` · `pipx install leghorn` · `npm i -g leghorn` · apt |
| **[legbar](https://github.com/gmhoward9289-ops/legbar)** | *Both, on one canvas.* Live agent sessions beside GitHub CI from a single discovery layer, so the two panes can never disagree. Sees **Cursor agents** too, which write no session marker at all. | new — not yet released |
| **[git-roost](https://github.com/gmhoward9289-ops/git-roost)** | *What is actually in the trees?* Every repo and worktree on the box in one table, most actionable first. Sessions report intent; git reports what happened. | clone and run — one file, no deps |

Python 3.9+, standard library only, macOS/Linux/Windows.

## Making numbers defensible

- **[counting-chicken-wings](https://github.com/gmhoward9289-ops/counting-chicken-wings)** — how many chickens does it take to make a dozen wings? Six is a floor, not a fact; the real answer is usually close to twelve. A pooling model with an honest uncertainty band, where every input cites a primary source.
- **[xycalc](https://github.com/gmhoward9289-ops/xycalc)** — how much X does it take to run Y? Infrastructure sizing from a corpus where every number cites a source *and* names the versions it applies to.
- **[shunt-ai-power](https://github.com/gmhoward9289-ops/shunt-ai-power)** — APCAM. What local LLM inference actually costs in electricity, from measured GPU wattage rather than a spec sheet.

## Security

- **[llm-security-rules](https://github.com/gmhoward9289-ops/llm-security-rules)** — tested Semgrep rules for LLM application security, mapped to the OWASP Top 10 for LLM Applications (2025). Every rule ships with the code that should trip it and the code that should not.

## Elsewhere

- **[vanity-scout](https://github.com/gmhoward9289-ops/vanity-scout)** — FCC vanity callsign availability tracking, for the amateur radio operators who care about four specific letters.

---

Built in a Digital Swamp. Contact: **dev@swamplink.com**

*From my swamp to yours.*
