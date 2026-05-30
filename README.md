# Minecraft Server Skill

Codex skill for deploying, hardening, optimizing, and operating Minecraft Java servers on Linux VPS or dedicated hosts.

Use this skill when an agent is asked to install, upgrade, configure, optimize, secure, or operate a Minecraft Java server. Covers Vanilla, Fabric, Quilt, Forge, NeoForge, Paper, Purpur, and Folia setups, treating the server as a production service instead of a one-off jar launch.

## Features

- **Host discovery** - OS, CPU, RAM, disk, Java, existing services, ports, firewall, private-network access
- **Guided setup** - Asks only high-impact choices: version, server type, EULA, whitelist, max player slots, seed, MOTD, icon, mods/plugins, datapacks, quality-of-life tweaks
- **Verified downloads** - Mojang, Fabric, PaperMC, and Modrinth metadata APIs with SHA1 checks
- **Service management** - Dedicated `minecraft` user, systemd unit, conservative JVM flags, restart/logging defaults
- **Network hardening** - Public only `25565/tcp`; RCON, query, web maps, panels stay private by default
- **Discord bridge** - Discord Integration (`dcintegration`) for Fabric, Discord-MC-Chat for advanced setups, DiscordSRV for Paper/Spigot
- **Live mapping** - BlueMap server-side live map with optional Xaero's/Map Link client-side player visibility
- **Gameplay datapacks** - Optional BlazeandCave's Advancements Pack install with conservative reward/message/scoreboard defaults and explicit co-op choice
- **Technical Minecraft tooling** - Optional TMC stack: Carpet, Servux, Syncmatica, carpet-extra, carpet-tis-addition
- **Pregeneration & profiling** - Chunky chunk pregeneration, Spark TPS/MSPT profiling, world border enforcement
- **Backups** - Backup policy prompts and Just Enough Backups defaults for frequency, retention, warnings, and free-space reserve
- **Client onboarding** - Server invite text and client mod/export guidance for players
- **Quality-of-life tweaks** - Hearts in tab, deaths below names, sleep percentage, phantom/Enderman grief control, TPS in tab footer
- **Validation** - Service state, logs, listening ports, firewall rules, whitelist/ops, mod/plugin load results

## Server Type Recommendations

| Use Case | Recommended Type |
|---|---|
| Vanilla-compatible performance mods, technical/private servers | Fabric |
| Plugin ecosystems, public/community servers | Paper / Purpur |
| Specific modpack that requires it | Forge / NeoForge |
| Absolute Mojang behavior required | Vanilla |
| Region-based multithreading (experimental) | Folia |

## Installation

Clone into your Codex skills directory:

```bash
git clone https://github.com/Microck/minecraft-server-skill ~/.codex/skills/minecraft-server
```

Or clone elsewhere and symlink:

```bash
git clone https://github.com/Microck/minecraft-server-skill.git
ln -s "$(pwd)/minecraft-server-skill" ~/.codex/skills/minecraft-server
```

Invoke with `$minecraft-server` when the task involves Minecraft Java server deployment or operations.

## Repository Structure

| Path | Description |
|---|---|
| `SKILL.md` | Main workflow, defaults, safety rules, performance baselines, command patterns, completion criteria |
| `references/vanilla.md` | Mojang metadata, server jar verification, install shape, tuning notes |
| `references/fabric.md` | Fabric and Quilt metadata, installer workflow, baseline mods, server properties, validation |
| `references/forge-neoforge.md` | Forge and NeoForge modpack workflow, compatibility checks, tuning notes |
| `references/paper.md` | Paper, Purpur, and Folia metadata, plugin baseline, configuration guidance |
| `references/operations.md` | systemd, JVM flags, firewall, RCON, Chunky pregeneration, backups, whitelist, ops, gameplay tweaks, Spark profiling |
| `scripts/mcmeta.py` | CLI helper for Mojang, Fabric, and Modrinth metadata plus SHA1 verification |
| `agents/openai.yaml` | OpenAI-facing skill metadata |

## `mcmeta.py` Command Reference

```bash
# Mojang server metadata and download URL
python3 scripts/mcmeta.py minecraft-version 1.21.4

# Fabric loader version for a Minecraft version
python3 scripts/mcmeta.py fabric-loader 1.21.4

# Latest Fabric installer metadata
python3 scripts/mcmeta.py fabric-installer

# Modrinth project version lookup
python3 scripts/mcmeta.py modrinth lithium 1.21.4 --loader fabric

# SHA1 hash of a local file
python3 scripts/mcmeta.py sha1 /opt/minecraft/server.jar
```

## Agent Workflow

1. Read `SKILL.md`.
2. Read exactly one server-type reference for the requested variant.
3. Use `references/operations.md` for systemd, backups, firewall, RCON, pregeneration, profiling, whitelist, ops, or gameplay tweaks.
4. Use `scripts/mcmeta.py` or official project APIs to verify version-specific downloads.
5. Report: Minecraft version, server type, Java version, installed mods/plugins, service status, path, ports, firewall exposure, key `server.properties` values, whitelist/ops status, backup/profiling state, and any warnings or skipped items.

## Defaults

| Setting | Default |
|---|---|
| Path | `/opt/minecraft` |
| User/group | `minecraft` |
| Service | `minecraft.service` |
| Game mode | survival |
| Difficulty | hard |
| Sleep percentage | 33 |
| Online auth | `online-mode=true` |
| Whitelist | Enabled (private); disabled only if public launch is explicit |
| Max players | Ask during setup; `20` for small/friend servers if omitted |
| Spawn protection | `0` |
| RCON | Disabled; if enabled, localhost-only with strong password |
| View distance | 8-10 (public), 12 (small private), 16 (2-4 players + pregen) |
| Simulation distance | 5-6 |
| Memory | 4G vanilla/Paper, 6-8G Fabric baseline, 8-12G modpacks |
| JVM | Java 21 for 1.20.5+ / 1.21+ |
| GC | G1GC; curated Aikar-style flags for 6G+ heaps |

## Optional Datapacks

For BlazeandCave's Advancements Pack, the skill asks before installing and asks separately whether cooperative mode should be enabled.

Default BACAP configuration when selected:

| Option | Default |
|---|---|
| Item rewards | Off |
| XP rewards | Off |
| Trophies | On |
| Welcome/intro message | Off |
| Advancement messages | On |
| Scoreboard display | Off |
| Cooperative mode | Ask |

## Backups

The skill asks for backup frequency, retention, whether to backup with no players online, backup-on-stop/start behavior, and free-space reserve.

Default Just Enough Backups policy for small/friend servers:

| Setting | Default |
|---|---|
| Mode | Full backups |
| Automatic interval | 360 minutes |
| Pause without players | No |
| Backup on start | No |
| Backup on stop | Yes |
| Warning | 5 minutes |
| Integrity | Strict |
| Summary file | Enabled |
| Free-space reserve | 10 GB |
| Retention | 14 full backups |
| Total backup cap | 50 GB |

## Client Onboarding

When setup changes affect players, the skill can emit:

- Server invite/onboarding text with address, Minecraft version, BlueMap URL, whitelist and Discord linking notes
- Client mod list grouped as required, recommended, optional, and client-only
- Map Link config values for BlueMap/Xaero player visibility

## Safety Posture

- Do not run the server as root.
- Do not expose RCON publicly.
- Keep `online-mode=true` unless the user explicitly accepts username-spoofing risk.
- Do not delete worlds, mods, configs, or backups without explicit approval.
- Stop the service before changing loader jars, mods, plugins, Java, or world-critical config.
- Do not start a new world before applying a requested seed.
- Do not apply gameplay-changing rules or datapacks automatically.
- Discord bot tokens are secrets - never commit, paste, or log them.

## Performance Baselines

**Fabric (private/performance):**
`fabric-api`, `lithium`, `ferrite-core`, `spark`, `chunky`, `krypton`, `servercore`, `scalablelux`, `alternate-current`

**Fabric (Technical Minecraft):**
`fabric-api`, `fabric-carpet`, `lithium`, `ferrite-core`, `servux`, `syncmatica`, with optional `carpet-extra`, `carpet-tis-addition`

**Paper/Purpur:**
Config tuning + plugins: Spark, Chunky, LuckPerms, CoreProtect

## Operating Philosophy

The skill favors one clear current-state server implementation: dedicated user, explicit service management, version compatibility checks, backups, profiling, and narrow network exposure. It avoids silent compatibility guesses, public admin surfaces, and broad tuning changes not backed by logs or profiles.
