# CLAUDE.md

> Workspace for a **HeyGen Builder interview**. Language/stack is decided live during
> the interview. This file orients you to the host machine (NixOS) so you don't reach
> for tools that aren't there or try to install things the wrong way.

## The machine is NixOS — read this first

- **Nothing is installed imperatively or globally.** There is no `apt`/`dnf`/`brew`,
  and `pip install`/`npm i -g`/`cargo install`/`go install` into the user profile are
  off the table. Don't suggest them.
- **Non-FHS layout.** There is no global `/usr/lib`. A prebuilt binary downloaded from
  the internet (a pip wheel's bundled binary, a `curl | sh` installer, etc.) will often
  fail to exec. Prefer Nix-provided binaries. If something dies with "cannot execute"
  or a missing `.so`, that's the non-FHS issue, not a real bug.
- **Don't touch system config.** No `nixos-rebuild`, `home-manager switch`, or `sudo`.
  That's the user's machine (`~/lumino`), unrelated to this project, and needs a TTY
  you don't have.

## Project dev environment: a Nix flake devShell + direnv

This project's tools live in a **per-project flake devShell**, not on the global PATH.

The user scaffolds it with their own helper, **`finit <lang>`** — e.g. `finit python`,
`finit node`, `finit go`, `finit rust`. That runs
`nix flake init --template ~/lumino/modules/dev-shells#<lang>` and `direnv allow`,
dropping a `flake.nix`, a `.envrc` (`use flake`), and a `.gitignore` into the repo.
**The user runs `finit` and `git init` themselves during the interview** — do not run
them for the user, and don't assume the flake or git repo exists yet. If you need the
devShell and it isn't there, say so and wait.

Once it exists, **direnv** auto-loads the shell on `cd` (in interactive shells).

## Running project commands

Your Bash shell is non-interactive, so direnv may not be active in it. Wrap project
commands so they get the devShell:

```bash
nix develop -c <cmd>      # e.g. nix develop -c pytest
# or
direnv exec . <cmd>       # if direnv has already allowed this dir
```

Run the language's own tooling **inside** that shell (see dependency tier 1 below).

## Adding dependencies — three tiers, keep them separate

The single most important distinction on this machine:

**1. Project library/code dependencies** (packages the code actually imports) → the
project's **package manager manifest**, committed and locked. Add them *through the
package manager, inside the devShell* — never hand-edit the flake for these, never `,`,
never global:

| Stack             | Add a dep             | Lands in                                              |
|-------------------|-----------------------|-------------------------------------------------------|
| Python + **uv**   | `uv add <pkg>`        | `pyproject.toml` + `uv.lock`                          |
| Python + **poetry**| `poetry add <pkg>`   | `pyproject.toml` + `poetry.lock`                      |
| Python + pip      | `pip install <pkg>`   | `.venv` (record in `pyproject.toml` / `requirements.txt`) |
| Node              | `npm add <pkg>`       | `package.json` + lockfile                             |
| Go                | `go get <pkg>`        | `go.mod` / `go.sum`                                   |
| Rust              | `cargo add <pkg>`     | `Cargo.toml` / `Cargo.lock`                           |

So if this project uses **uv or poetry**, project dependencies go in `pyproject.toml`
via `uv add` / `poetry add`. Do not put them in the flake, and do not run them with `,`.

**2. The toolchain itself** — interpreter, the package-manager binary (`uv`, `poetry`,
`pnpm`, ...), compilers, and system libraries the code links against → the
`packages` / `buildInputs` list in `flake.nix`, then `direnv reload` (or re-enter
`nix develop`). The stock `python` template ships `pip` + a `.venv` (Python 3.13); if
the project wants `uv` or `poetry`, add it here (or scaffold with `finit python-poetry`).
Templates leave commented examples in that list to follow.

**3. A throwaway one-off CLI tool** that isn't a project dependency at all → **`,`
(comma)**, which runs a nixpkgs program on the spot, installing nothing:

```bash
, jq .                    # run jq without adding it anywhere
, http GET example.com    # httpie, one-off
```

Equivalents: `nix run nixpkgs#<pkg>` or `nix shell nixpkgs#<pkg>`.

## Hard rules

- **Nix-first, right tier for each dependency:** project library deps → the package
  manager's manifest (`uv add` / `poetry add` → `pyproject.toml`); toolchain + system
  libs → `flake.nix`; throwaway one-off tools → `,` (comma). Never install globally.
- Don't assume a tool is on PATH — check, and if it's missing reach for the devShell or
  `,` rather than an OS package manager.
- Don't run `finit`, `git init`, system rebuilds, or `sudo`.
- Keep changes scoped to this folder.
