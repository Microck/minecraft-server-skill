# Operations

## Systemd

Use a dedicated unit:

```ini
[Unit]
Description=Minecraft Server
After=network.target

[Service]
User=minecraft
Group=minecraft
WorkingDirectory=/opt/minecraft
ExecStart=/usr/bin/java -Xms8G -Xmx8G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -jar /opt/minecraft/fabric-server-launch.jar nogui
Restart=on-failure
RestartSec=10
SuccessExitStatus=0 130 143

[Install]
WantedBy=multi-user.target
```

Adjust `ExecStart` for Vanilla/Paper/Forge.

## JVM Flags

Keep service management in systemd. Do not replace the unit with a generated restart shell script unless the user explicitly wants that deployment style.

For modern Java 21 servers with 6G+ heap, a curated Aikar/flags.sh-style G1GC command is a good default:

```bash
/usr/bin/java -Xms8G -Xmx8G -XX:+UseG1GC -XX:+ParallelRefProcEnabled -XX:MaxGCPauseMillis=200 -XX:+UnlockExperimentalVMOptions -XX:+DisableExplicitGC -XX:+AlwaysPreTouch -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:InitiatingHeapOccupancyPercent=15 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:SurvivorRatio=32 -XX:+PerfDisableSharedMem -XX:MaxTenuringThreshold=1 -jar /opt/minecraft/fabric-server-launch.jar nogui
```

Adjust heap size to the host and workload. Prefer equal `-Xms`/`-Xmx` for dedicated servers. Leave memory for OS cache, native memory, backups, and monitoring. Do not tune flags blindly if Spark shows entities, chunk I/O, or a specific mod/plugin as the bottleneck.

## Firewall

Recommended UFW posture:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 25565/tcp
sudo ufw deny 25575/tcp
```

Keep SSH restricted to VPN/Tailscale/private admin ranges when possible.

## RCON

Use RCON only for local automation or trusted private networks:

```properties
enable-rcon=true
rcon.port=25575
rcon.password=<strong random>
```

Store the password in `/opt/minecraft/.rcon-password` with mode `600`, and firewall-deny public `25575/tcp`.

## Chunky

For high view distances, pregenerate before inviting players:

```text
/chunky world world
/chunky shape square
/chunky center 0 0
/chunky radius 6000
/chunky start
/worldborder center 0 0
/worldborder set 12000
```

Use smaller dimensions:

- Nether: radius `1000-2500`
- End: radius `2000-4000`

Chunky may run multiple dimension tasks simultaneously, but doing so can slow Overworld generation. Check with `/chunky progress`.

## Backups

Use one of:

- Maintained backup mod/plugin matching the server version.
- System-level backups using `tar`/`rsync` while the server is stopped or after `save-off`, `save-all flush`, backup, then `save-on`.

Keep backups outside the world folder when possible. Test restore instructions before trusting backups.

## Whitelist And Ops

For private servers:

```text
/whitelist on
/whitelist add <player>
/op <admin>
```

Keep `enforce-whitelist=true` so currently connected non-whitelisted players are removed when whitelist changes.

## Optional Gameplay And Display Tweaks

Ask before applying any of these. They are common private-server quality-of-life choices, but they change visible UI or gameplay behavior.

### Hearts In Tab And Deaths Below Names

Use vanilla scoreboards when the user asks for hearts in tab/player list or deaths below names:

```text
/scoreboard objectives add health health
/scoreboard objectives modify health rendertype hearts
/scoreboard objectives setdisplay list health
/scoreboard objectives add deaths deathCount Deaths
/scoreboard objectives setdisplay below_name deaths
```

On current 1.21.x command syntax, the below-name slot is `below_name`, not old `belowName` spellings. The `list` slot is the player-list/tab overlay. Clear accidental sidebars with:

```text
/scoreboard objectives setdisplay sidebar
```

### TPS/MSPT In Tab Footer

If TabTPS is installed and the user wants TPS/MSPT in the lower tab area, make the default display permission-free and enable tab footer on login:

```hocon
permission=""
tab-settings {
    allow=true
    enable-on-login=true
    header-modules=""
    footer-modules="tps,mspt"
}
```

Restart the server or use the mod's reload command if available after editing TabTPS config.

### Disable Phantoms

If the user wants phantoms disabled, prefer the targeted vanilla gamerule:

```text
/gamerule doInsomnia false
```

This disables phantom spawning from insomnia without affecting other mob behavior.

### Disable Enderman Grief Only

Do not use broad `mobGriefing=false` just to stop Endermen unless the user explicitly wants all mob griefing disabled. Broad `mobGriefing=false` also affects creepers, villager farming, and other mechanics.

For targeted Enderman grief prevention:

1. Keep or restore:

```text
/gamerule mobGriefing true
```

2. Install a compatible No Enderman Grief datapack/mod for the selected Minecraft version. For datapacks, put the `.zip` in:

```text
/opt/minecraft/world/datapacks/
```

3. Run:

```text
/reload
/datapack list enabled
```

Verify the datapack appears in the enabled list.

## Profiling

Use Spark:

```text
/spark profiler start
/spark profiler stop
/spark tps
```

Diagnose from actual profiles. Common causes are entities, hoppers/farms, chunk generation, plugin/mod tasks, storage I/O, and excessive simulation distance.
