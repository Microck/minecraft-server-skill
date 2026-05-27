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

## Profiling

Use Spark:

```text
/spark profiler start
/spark profiler stop
/spark tps
```

Diagnose from actual profiles. Common causes are entities, hoppers/farms, chunk generation, plugin/mod tasks, storage I/O, and excessive simulation distance.
