---
name: minecraft-server
description: End-to-end Minecraft Java server deployment, hardening, optimization, and operations on Linux VPS or dedicated hosts. Use when Codex is asked to install, upgrade, configure, optimize, secure, or operate Minecraft servers for Vanilla, Fabric, Quilt, Forge, NeoForge, Paper, Purpur, Folia, or similar server types; includes version selection, EULA handling, firewall posture, systemd service setup, mod/plugin selection, pregeneration, backups, whitelist/ops, RCON safety, and validation.
---

# Minecraft Server

Deploy Minecraft Java servers as production services, not one-off jar launches. Prefer conservative, observable defaults: dedicated user, systemd, public game port only, private admin access, backups, profiling, and explicit version compatibility checks.

## Start Workflow

1. Discover host facts before asking:
   - OS, architecture, CPU/RAM/swap/disk: `uname -m`, `nproc`, `free -h`, `df -h`.
   - Existing Java: `java -version`.
   - Existing server/service: `/opt/minecraft`, `minecraft.service`, listening ports, firewall.
   - Existing Tailscale/private network if SSH/admin access is already constrained.
2. Ask only high-impact choices not discoverable from the host:
   - When the harness exposes an AskUser/user-input tool such as `request_user_input`, use it for setup choices. Group related choices into as few prompts as practical, offer recommended defaults first, and keep free-form questions for values such as version, seed, MOTD, icon URL/path, player names, and domain names.
   - If no AskUser/user-input tool is available, ask concise plain-text questions instead and proceed with safe defaults when the user already gave enough information.
   - Minecraft version.
   - Server type: Vanilla, Fabric, Quilt, Forge, NeoForge, Paper, Purpur, Folia.
   - Public/private access: whitelist, max player slots (`max-players`), expected active player count, and view distance preference.
   - World identity and server-list presentation:
     - Seed: ask whether to use a random seed or a custom seed before first world creation.
     - Server description/MOTD: ask whether to use the default or a custom description.
     - Server icon/profile picture: ask whether to use none/default or a supplied image URL/file.
   - EULA acceptance.
   - Mod/plugin goals: performance-only, admin tools, gameplay, full modpack.
   - Optional Discord bridge:
     - Ask whether to link Minecraft chat/events to Discord.
     - For Fabric 1.21.10, recommend Discord Integration (`dcintegration`) for simple chat/event bridging.
     - Offer Discord-MC-Chat only when the user wants heavier customization, multi-server mode, console forwarding, or advanced formatting.
     - Avoid DiscordSRV unless the server type is Paper/Spigot/Purpur, because it is plugin-server oriented.
   - Optional quality-of-life rules/displays: hearts in tab, TPS/MSPT in tab footer, deaths below names, phantoms disabled, Enderman grief disabled.
   - Optional gameplay datapacks:
     - Ask whether to install BlazeandCave's Advancements Pack.
     - If yes, ask whether cooperative mode should be enabled.
     - Default BACAP configuration: item rewards off, XP rewards off, trophies on, welcome/intro message off, advancement messages on, scoreboard off.
3. Verify all version-specific downloads from official metadata or primary project APIs before installing.
   - Use `scripts/mcmeta.py` for Mojang, Fabric, and Modrinth metadata.
   - Browse official docs or project APIs when metadata is missing or stale.
4. Install as a service:
   - Dedicated `minecraft` user, usually home `/opt/minecraft`.
   - Java runtime matching the Minecraft version.
   - `/etc/systemd/system/minecraft.service`.
   - `server.properties`, `eula.txt`, `mods/` or `plugins/`.
5. Harden network exposure:
   - Public: only game port, normally `25565/tcp`.
   - Private/admin: SSH over VPN/Tailscale where possible.
   - RCON, query, web maps, panels, databases: never expose publicly unless explicitly requested and protected.
6. Validate:
   - Service active, logs show ready/done line, correct port listening.
   - Firewall matches intended exposure.
   - Whitelist/ops/admin commands work.
   - Mods/plugins loaded with no dependency errors.

## Server Type Selection

Read exactly one variant reference when implementing:

- Vanilla or baseline Mojang jar: `references/vanilla.md`
- Fabric or Quilt modded servers: `references/fabric.md`
- Forge or NeoForge modded servers: `references/forge-neoforge.md`
- Paper, Purpur, or Folia plugin servers: `references/paper.md`
- Operations, backups, Chunky, profiling, RCON: `references/operations.md`

If the user says “best/perfect server” without choosing a type, recommend:

- Fabric for vanilla-compatible performance mods and technical/private servers.
- Paper/Purpur for plugin ecosystems and public/community servers.
- Forge/NeoForge only when a required modpack needs it.
- Vanilla only when absolute Mojang behavior is required.

## Defaults

Use these unless the user chooses otherwise:

- Path: `/opt/minecraft`
- User/group: `minecraft`
- Service: `minecraft.service`
- Game mode: survival
- Difficulty: hard
- Sleeping: set `playersSleepingPercentage` to `33` after first startup unless the user chooses another value
- Online auth: `online-mode=true`
- Whitelist: enabled for private/friend servers, disabled only if public launch is explicit
- Max players: ask during setup; if omitted, use `max-players=20` for small/friend servers
- Server description/MOTD: ask; if omitted, use a concise version/type description
- Server icon/profile picture: ask; if supplied, convert to `server-icon.png`, exactly 64x64 PNG, in the server root
- Spawn protection: set `spawn-protection=0` unless the user explicitly wants protected spawn
- RCON: disabled by default; if needed, enable with strong password and firewall deny public `25575/tcp`
- Query: disabled by default
- View distance:
  - 8-10 for general public servers
  - 12 for small private servers
  - 16 for 2-4 players with pregeneration
- Simulation distance: 5-6 for most servers, lower than view distance
- Memory:
  - 4G small vanilla/Paper
  - 6-8G small Fabric/modded baseline
  - 8-12G moderate modpacks
  - Avoid allocating nearly all RAM to Java
- JVM: Java 21 for modern 1.20.5+ / 1.21+ servers unless metadata says otherwise
- Startup flags: use simple G1GC flags by default; for 6G+ heaps, consider a curated Aikar/flags.sh-style G1GC set inside the systemd `ExecStart`, but do not replace systemd with a generated shell loop unless the user asks

## Safety Rules

- Do not run the server as root.
- Do not open SSH to the public internet when private admin access exists.
- Do not disable `online-mode` unless the user explicitly understands username spoofing risk.
- Do not expose RCON publicly; use localhost, firewall, or VPN.
- Do not install C2ME/alpha performance mods by default; profile first.
- Do not start a new world before applying a requested seed.
- For existing worlds, explain that changing the seed affects future generation only; existing chunks remain unchanged unless explicitly deleted/reset.
- When applying a custom server icon/profile picture, download only from the user-provided source, convert/crop to 64x64 PNG, and set ownership so the service user can read it.
- For Discord bridges, never expose or print bot tokens. Prefer prompting for bot token, channel ID, and optional admin role IDs only after the mod is installed and its config path is known. Keep bot tokens in the mod config with restrictive file permissions where practical.
- Do not apply gameplay-changing quality-of-life rules or datapacks automatically; ask first, then document the exact commands/files used.
- Do not delete worlds, mods, configs, or backups without explicit approval.
- Stop the service before changing loader jars, mods, plugins, Java, or world-critical configs.

## Performance Baseline

For Fabric small private servers, install only compatible stable releases:

- `fabric-api`, `lithium`, `ferrite-core`, `spark`, `chunky`, `krypton`, `servercore`, `scalablelux`, `alternate-current`.
- Add `c2me` only after Spark shows chunk generation/loading as the bottleneck and the user accepts alpha/devbuild risk.

For Technical Minecraft/Fabric servers, ask before adding a TMC tooling stack:

- Practical baseline: `fabric-api`, `fabric-carpet`, `lithium`, `ferrite-core`, `servux`, `syncmatica`.
- Add-on tools when explicitly useful: `carpet-extra`, `carpet-tis-addition`.
- Performance extras to treat carefully: `krypton` is generally reasonable; `c2me` needs explicit user consent and testing on a backup first.
- Omit client-only TMC mods from server installs, including Sodium, Litematica, MiniHUD, Tweakeroo, Item Scroller, Mod Menu, and ReplayMod.

For Fabric Discord chat bridging:

- Default recommendation: Discord Integration (`dcintegration`) when compatible with the chosen Minecraft/Fabric version.
- Setup sequence:
  1. Install the compatible server-side jar in `mods/`.
  2. Start once to generate config, then stop before editing secrets.
  3. Have the user create a Discord application/bot, enable required bot intents, and invite it with bot + application command scopes.
  4. Configure `config/Discord-Integration.toml` with `botToken`, `botChannel`, and optional `adminRoleIDs`.
  5. Restart and test Minecraft-to-Discord and Discord-to-Minecraft chat.
- If the user wants transparency/auditing, enable Discord Integration's `[commandLog]` with a real channel ID instead of `"0"`; keep low-signal commands such as `list`, `help`, and `?` ignored unless the user wants absolutely everything.
- Account linking is normally `enableLinking = true`: players run `/discord link` in-game, then run the generated `/link <code>` command in Discord before the code expires.
- Replace placeholder `/discord` invite values in `[ingameCommand]` with the real Discord invite before calling setup complete.
- Alternative: Discord-MC-Chat for advanced formatting, multi-server mode, status/player-count display, console forwarding, or more complex webhook behavior.
- Treat Discord bot tokens as secrets; never commit, paste back, or log them.

For BlueMap/Xaero player visibility:

- BlueMap is the best server-side live map. If exposed publicly, document the web port and firewall posture.
- Xaero's Minimap/World Map server-side Fabric jars are optional compatibility/config helpers; they do not by themselves make every remote player globally visible in clients.
- For global BlueMap-to-Xaero player visibility, players need the client-side Map Link mod. Configure Map Link with a server entry whose `ip` exactly matches the address the client uses/detects, for example `145.241.164.73:25565`, and whose `link` points at the BlueMap URL, for example `http://host:8101/`.
- Map Link's direct config fields are `maptype`, `ip`, and `link`; for BlueMap use `maptype: "Bluemap"`. Client config is usually `.minecraft/config/maplink.json5`.

For Paper/Purpur, prefer config tuning and plugins over Fabric mods. Use Spark and Chunky equivalents where compatible.

For all server types:

- Pregenerate chunks before inviting players when view distance is high.
- After every restart during pregeneration, verify Chunky tasks resumed; if not, send `chunky continue <dimension>` via local RCON and confirm with `chunky progress`.
- Set a world border near the pregenerated radius.
- Use Spark profiles to diagnose TPS/MSPT issues.
- Treat entities, farms, chunk I/O, view distance, and bad mods/plugins as likely bottlenecks.
- Treat JVM flag generators such as `flags.sh` as references for GC tuning, not as a substitute for service management, mod/plugin compatibility checks, pregeneration, or profiling.

For optional gameplay datapacks:

- BlazeandCave's Advancements Pack is configured in-game with `/function blazeandcave:config`; use Modrinth metadata for the version compatible with the server's Minecraft version.
- Default BACAP setup when selected: `item_rewards_off`, `exp_rewards_off`, `trophies_on`, `intro_msg_off`, `msg_set_on`, and clear scoreboard display slots with `scoreboard objectives setdisplay list`, `sidebar`, and `below_name`.
- Ask before enabling BACAP cooperative mode. If enabled, run `function blazeandcave:config/coop_on`; for team-based cooperative mode, use `coop_on_team` only when the user explicitly wants team-based sharing.

## Command Pattern

Use `systemctl`, logs, and RCON/admin commands:

```bash
sudo systemctl status minecraft --no-pager
sudo journalctl -u minecraft -f
sudo systemctl restart minecraft
ss -tulpn
sudo ufw status numbered
```

If RCON is enabled, keep credentials in a root/minecraft-readable file such as `/opt/minecraft/.rcon-password`; prefer local-only command execution and firewall-deny `25575/tcp`.

Useful initial world/server commands after first successful startup:

```bash
gamerule playersSleepingPercentage 33
scoreboard objectives add health health
scoreboard objectives setdisplay list health
scoreboard objectives modify health rendertype hearts
scoreboard objectives add deaths deathCount
scoreboard objectives setdisplay below_name deaths
```

Set `difficulty=hard` and any chosen `motd=`/`level-seed=` in `server.properties` before the first full launch. Minecraft server icons must be named `server-icon.png`, placed in the server root, and be a 64x64 PNG.

## Completion Criteria

Report:

- Minecraft version, server type/loader/build, Java version.
- Installed mods/plugins and their versions.
- Service status and path.
- Game/admin ports and firewall exposure.
- Key `server.properties` values, including `max-players`, view distance, simulation distance, online mode, and whitelist.
- Whitelist/ops status.
- Pregeneration/backups/profiling state.
- Any known warnings, skipped items, or follow-up commands.
