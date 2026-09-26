# davebben-skills

My personal collection of agent skills, one plugin per area of life. Public, so take what's useful.

The skills are plain Markdown (`SKILL.md`) and work with any skills-compatible agent: Claude Code, Codex, Cursor, and 70+ others. Nothing to build or compile. Claude Code users get a first-class plugin install where each area is its own installable plugin; everyone else installs individual skills with the `skills` CLI.

## Plugins

| Plugin | What it does | Status |
|---|---|---|
| [SDLC](plugins/SDLC/) | Take an engineering change from a vague ask to a verified production change: define the outcome, slice it into stories, write each story's criteria as it starts, write failing tests first, build, review in three passes, ship and log. Nine skills. | live |
| [context](plugins/context/) | Manage an agent session's context across boundaries. Hands a session over when context fills or work stops partway, recording the dead ends. One skill. | live |
| [meals](plugins/meals/) | Eat to numbers without cooking from a spreadsheet. Turns a recipe you already make into a reusable meal template that hits a calorie ceiling and protein and fiber floors, verified against USDA values, then plans days of meals from those templates into the meal planner with a shopping list. Two skills. | live |

Open a plugin's folder for its own README and the detail behind it.

## Installing

### Claude Code

Add the marketplace once, then install whichever plugins you want. Each install pulls in only that area's skills, so `SDLC` never loads finance or fitness triggers.

```bash
/plugin marketplace add DaveBben/davebben-skills
/plugin install SDLC@davebben-skills
```

Future plugins install the same way: `/plugin install <plugin>@davebben-skills`.

### Any other agent (Codex, Cursor, Windsurf, and more)

Use the [`skills` CLI](https://github.com/vercel-labs/skills), which installs plain `SKILL.md` files into whichever agent you point it at.

```bash
# see everything on offer, grouped by area
npx skills add DaveBben/davebben-skills --list

# install one skill (the nine SDLC skills call each other by name: install all nine together)
npx skills add DaveBben/davebben-skills --skill deliver

# install everything
npx skills add DaveBben/davebben-skills --all
```

The CLI installs by individual skill or all at once; it has no per-area selector, so the plugin boundary that Claude Code enforces is only a visual grouping here. Pick the skills you want by name.

### Manual

Every skill is a self-contained directory under [skills/](skills/). Copy the one you want into your agent's skills folder.

## Layout

Skills live once, at the repo root, and are grouped by area:

```
skills/<area>/<skill>/SKILL.md      canonical, what every agent reads
plugins/<area>/                     Claude Code plugin wrapper
  .claude-plugin/plugin.json
  skills -> ../../skills/<area>      symlink, so there is one source of truth
.claude-plugin/marketplace.json     the Claude Code marketplace
```

The `skills/` tree is what the `skills` CLI discovers. Each Claude Code plugin points at the same files through a symlink, so nothing is duplicated and nothing drifts.

## Adding a plugin (note to self)

Each life area is one plugin, backed by one folder of canonical skills.

1. Create the canonical skills at `skills/<area>/<skill>/SKILL.md`, references one level deep in `references/` beside each.
2. Create the Claude Code wrapper at `plugins/<area>/`:
   - `.claude-plugin/plugin.json` — `name` (the slash-command prefix, so skills invoke as `/<area>:<skill>`), `version`, `description`, `license`, `author`.
   - `skills` as a symlink to `../../skills/<area>` (`ln -s ../../skills/<area> skills` from inside `plugins/<area>/`).
   - `README.md` for that plugin's detail.
3. Append one entry to the `plugins` array in [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json): `name`, `source: "./plugins/<area>"`, `description`, `version`, `license`, a `skills` array of `./skills/<skill>` paths (relative to `source`, resolved through the symlink; no `..` — the plugin schema forbids it), and `author`.
4. The plugin `name` in `plugin.json`, its `marketplace.json` entry, and the `plugins/<area>/` directory must all match; versions in `plugin.json` and `marketplace.json` bump together.
5. Add a row to the Plugins table above.

Keep plugins independent. A Claude Code user who installs `finance` should never load `SDLC`'s triggers, and vice versa. That trigger isolation is the whole reason these are separate plugins.

MIT.
