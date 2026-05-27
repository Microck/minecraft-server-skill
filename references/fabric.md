# Fabric And Quilt

Use Fabric for lightweight vanilla-compatible optimization and modded private servers. Quilt is similar operationally, but verify loader and mod compatibility separately.

## Metadata

- Fabric loader versions: `https://meta.fabricmc.net/v2/versions/loader/<minecraft-version>`
- Fabric installer versions: `https://meta.fabricmc.net/v2/versions/installer`
- Installer command pattern:

```bash
java -jar fabric-installer.jar server -mcversion <mc> -loader <loader> -dir /opt/minecraft -downloadMinecraft
```

Prefer the latest stable loader supporting the requested Minecraft version. Use the latest stable installer unless the installer metadata says otherwise.

## Install Shape

- Install Java matching Mojang metadata.
- Create `/opt/minecraft/mods`.
- Run the Fabric installer as the `minecraft` user.
- Start with `fabric-server-launch.jar`.
- Keep `server.jar`, libraries, `versions/`, `mods/`, and configs owned by `minecraft:minecraft`.

## Baseline Mods

For a stable performance/admin baseline, query Modrinth for exact compatible files before downloading:

- Performance: `fabric-api`, `lithium`, `ferrite-core`, `spark`, `chunky`, `krypton`, `servercore`, `scalablelux`, `alternate-current`.
- Admin/maintenance: `ledger`, `fabric-language-kotlin` if Ledger requires it, `carpet`, `tabtps`, a backup mod with direct target-version support.

Do not assume version strings from memory. Use Modrinth API by project slug with `loaders=["fabric"]` and `game_versions=["<mc>"]`.

## Server Properties

Good private-server baseline:

```properties
online-mode=true
white-list=true
enforce-whitelist=true
enable-rcon=false
enable-query=false
view-distance=12
simulation-distance=5
sync-chunk-writes=false
network-compression-threshold=256
max-tick-time=60000
```

For 2-4 players on good hardware, `view-distance=16` is acceptable with pregeneration and `simulation-distance=5`.

Set `pause-when-empty-seconds=0` while unattended Chunky pregeneration is running; otherwise the server may pause with no players online.

## Validation

Check logs for:

- `Loading Minecraft <version> with Fabric Loader <version>`
- all expected mods listed
- `Done (...)! For help, type "help"`
- no hard dependency failures

If Fabric reports missing dependencies, install the exact dependency it recommends, or remove the dependent mod.
