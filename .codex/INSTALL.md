# Installing Apple Agent Kit for Codex

Enable Apple Agent Kit's Skills in Codex via native skill discovery, or via Codex's
plugin marketplace. Both paths load the same `skills/` directory Claude Code uses —
there is no separate Codex build of this content.

## Option A: Plugin marketplace

Inside a Codex CLI session:

```
/plugin marketplace add caglarbaranbora/Apple-Agent-Kit
```

Then install the `apple-agent-kit` plugin from that marketplace and restart Codex.
Codex's own plugin update mechanism keeps a marketplace install current — no manual
`git pull` step applies to this path.

## Option B: Manual clone + symlink

### Prerequisites

- Git

### Installation

1. **Clone this repository:**
   ```bash
   git clone https://github.com/caglarbaranbora/Apple-Agent-Kit.git ~/.codex/apple-agent-kit
   ```

2. **Create the skills symlink:**
   ```bash
   mkdir -p ~/.agents/skills
   ln -s ~/.codex/apple-agent-kit/skills ~/.agents/skills/apple-agent-kit
   ```

   **Windows (PowerShell):**
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.agents\skills"
   cmd /c mklink /J "$env:USERPROFILE\.agents\skills\apple-agent-kit" "$env:USERPROFILE\.codex\apple-agent-kit\skills"
   ```

3. **Restart Codex** (quit and relaunch the CLI) to discover the skills.

### Verify

```bash
ls -la ~/.agents/skills/apple-agent-kit
```

**Windows (PowerShell):**
```powershell
Get-Item "$env:USERPROFILE\.agents\skills\apple-agent-kit"
```

You should see a symlink (or junction on Windows) pointing at this repo's `skills/`
directory.

### Updating

```bash
cd ~/.codex/apple-agent-kit && git pull
```

Skills update instantly through the symlink.

### Uninstalling

```bash
rm ~/.agents/skills/apple-agent-kit
```

Optionally delete the clone: `rm -rf ~/.codex/apple-agent-kit`.

**Windows (PowerShell):**
```powershell
Remove-Item "$env:USERPROFILE\.agents\skills\apple-agent-kit"
```

Do not add `-Recurse` — this must remove only the junction itself, not follow into the
linked directory. Optionally delete the clone:
`Remove-Item -Recurse "$env:USERPROFILE\.codex\apple-agent-kit"`.
