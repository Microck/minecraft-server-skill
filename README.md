# Minecraft Server Skill

Codex skill for deploying, hardening, optimizing, and operating Minecraft Java servers on Linux VPS or dedicated hosts.

Use this skill when an agent is asked to install, upgrade, configure, optimize, secure, or operate a Minecraft Java server. It covers Vanilla, Fabric, Quilt, Forge, NeoForge, Paper, Purpur, and Folia setups, with an emphasis on treating the server like a production service instead of a one-off jar launch.

## What It Does

- Discovers host facts before asking setup questions: OS, CPU, RAM, disk, Java, existing services, ports, firewall, and private-network access.
- Guides only the high-impact choices that cannot be discovered safely, such as Minecraft version, server type, EULA acceptance, whitelist posture, seed, MOTD, icon, mods, plugins, and gameplay display tweaks.
- Verifies version-specific downloads through official metadata and project APIs before installation.
- Installs the server under a dedicated `minecraft` user, usually in `/opt/minecraft`.
- Runs the server through `systemd` with conservative JVM, restart, ownership, and logging defaults.
- Keeps public exposure narrow: normally only `25565/tcp`, with RCON, query, web maps, panels, and databases private unless explicitly requested and protected.
- Validates the finished server through service state, logs, listening ports, firewall rules, whitelist and ops state, and mod or plugin load results.

## Safety Posture

The skill defaults to conservative, observable server operations:

- Do not run the server as root.
- Do not expose RCON publicly.
- Keep `online-mode=true` unless the user explicitly accepts the username-spoofing risk.
- Do not delete worlds, mods, configs, or backups without explicit approval.
- Stop the service before changing loader jars, mods, plugins, Java, or world-critical config.
- Do not start a new world before applying a requested seed.
- Do not apply gameplay-changing rules or datapacks automatically.

## Repository Contents

- `SKILL.md` - main workflow, defaults, safety rules, performance baseline, command patterns, and completion criteria.
- `references/vanilla.md` - Mojang metadata, server jar verification, install shape, and tuning notes.
- `references/fabric.md` - Fabric and Quilt metadata, installer workflow, baseline mods, server properties, and validation.
- `references/forge-neoforge.md` - Forge and NeoForge modpack workflow, compatibility checks, and tuning notes.
- `references/paper.md` - Paper, Purpur, and Folia metadata, plugin baseline, and configuration guidance.
- `references/operations.md` - systemd, JVM flags, firewall, RCON, Chunky pregeneration, backups, whitelist, ops, optional gameplay tweaks, and Spark profiling.
- `scripts/mcmeta.py` - helper for Mojang, Fabric, and Modrinth metadata plus SHA1 checks.
- `agents/openai.yaml` - OpenAI-facing skill metadata.

## How To Use

Install or reference this skill, then invoke `$minecraft-server` when the task involves Minecraft Java server deployment or operations.

A good agent workflow is:

1. Read `SKILL.md`.
2. Read exactly one server-type reference for the requested variant.
3. Use `references/operations.md` when the task touches systemd, backups, firewall, RCON, pregeneration, profiling, whitelist, ops, or gameplay display tweaks.
4. Use `scripts/mcmeta.py` or official project APIs to verify version-specific downloads.
5. Report the Minecraft version, server type, Java version, installed mods or plugins, service status, path, ports, firewall exposure, key `server.properties` values, whitelist and ops status, backup or profiling state, and any warnings or skipped items.

## Operating Philosophy

The skill favors one clear current-state server implementation: dedicated user, explicit service management, version compatibility checks, backups, profiling, and narrow network exposure. It avoids silent compatibility guesses, public admin surfaces, and broad tuning changes that are not backed by logs or profiles.
