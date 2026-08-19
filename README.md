# George M. Howard

I build small, sharp tools in the open — mostly terminal programs for watching
AI coding agents work, plus a few projects that exist to make a number
defensible instead of merely plausible.

Everything here is single-purpose and installable without a build step, mostly
Apache 2.0 (a couple are still MIT — check each repo). Write-ups live at
**[blog.swamplink.com](https://blog.swamplink.com)**.

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
| **[leghorn](https://github.com/gmhoward9289-ops/leghorn)** | *What did this agent actually do?* A session reports intent; git reports what landed. Sessions joined to real git state, GitHub CI and open PRs with failures pinned until green, and a commit feed across every repo. | `brew install gmhoward9289-ops/tap/leghorn` · `pipx install leghorn` · `npm i -g leghorn` · apt |
| **[legbar](https://github.com/gmhoward9289-ops/legbar)** | *Both, on one canvas.* Live agent sessions beside GitHub CI from a single discovery layer, so the two panes can never disagree. Sees **Cursor agents** too, which write no session marker at all. | `pipx install legbar` |
| **[git-roost](https://github.com/gmhoward9289-ops/git-roost)** *(archived)* | *What is actually in the trees?* Every repo and worktree on the box in one table, most actionable first. Sessions report intent; git reports what happened. Superseded by the git pane in leghorn and legbar — kept around, unmaintained, as a standalone single-file option. | clone and run — one file, no deps |

Python 3.9+, macOS/Linux/Windows. Standard library only on macOS and Linux;
Windows pulls in `windows-curses`, because `curses` is the one thing not
already in the stdlib there.

Questions in the open go in Discussions:
**[roost](https://github.com/gmhoward9289-ops/roost/discussions)** ·
**[leghorn](https://github.com/gmhoward9289-ops/leghorn/discussions)** ·
**[legbar](https://github.com/gmhoward9289-ops/legbar/discussions)**.

<p>
  <img src="https://raw.githubusercontent.com/gmhoward9289-ops/roost/main/demo/roost-demo.gif" alt="roost: live Claude Code sessions, buckets, subagents, and the advice panel in a terminal UI" width="720"><br>
  <sub><b>roost</b> — buckets, subagents, the advice panel, and a cancelled stop.</sub>
</p>
<p>
  <img src="https://raw.githubusercontent.com/gmhoward9289-ops/leghorn/main/demo/leghorn-demo.gif" alt="leghorn: Claude Code sessions joined to git state and GitHub CI" width="720"><br>
  <sub><b>leghorn</b> — contested sessions, red CI, a session detail overlay, and the git toggle.</sub>
</p>
<p>
  <img src="https://raw.githubusercontent.com/gmhoward9289-ops/legbar/main/demo/legbar-demo.gif" alt="legbar: agent sessions and GitHub CI on one canvas" width="720"><br>
  <sub><b>legbar</b> — two contested trees, sessions waiting on a human, and red CI that cannot scroll away.</sub>
</p>

## Making numbers defensible

- **[counting-chicken-wings](https://github.com/gmhoward9289-ops/counting-chicken-wings)** — how many chickens does it take to make a dozen wings? Six is a floor, not a fact; the real answer is usually close to twelve. A pooling model with an honest uncertainty band, where every input cites a primary source.
- **[xycalc](https://github.com/gmhoward9289-ops/xycalc)** — how much X does it take to run Y? Infrastructure sizing from a corpus where every number cites a source *and* names the versions it applies to.
- **[apcam-ai-power-meter](https://github.com/gmhoward9289-ops/apcam-ai-power-meter)** — APCAM. What local LLM inference actually costs in electricity, from measured GPU wattage rather than a spec sheet.
- **[trust-but-anchor](https://github.com/gmhoward9289-ops/trust-but-anchor)** — models misquote sources 27–36% of the time even when told to be verbatim. Letting code locate a model-proposed anchor instead of trusting its quote recovers near-total coverage, with every span a real substring by construction.
- **[foundation-cosmetics-calculator](https://github.com/gmhoward9289-ops/foundation-cosmetics-calculator)** — sourced research on the cosmetics industry, at **[foundation.swamplink.com](https://foundation.swamplink.com)**.

## Security

- **[llm-security-rules](https://github.com/gmhoward9289-ops/llm-security-rules)** — tested Semgrep rules for LLM application security, mapped to the OWASP Top 10 for LLM Applications (2025). Every rule ships with the code that should trip it and the code that should not.

## Elsewhere

- **[awesome-tuis](https://github.com/gmhoward9289-ops/awesome-tuis)** — a curated list of terminal user interface projects.

---

Built in a Digital Swamp. Contact: **dev@swamplink.com**

*From my swamp to yours.*
