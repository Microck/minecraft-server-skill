# Vanilla

Use Vanilla when the user wants Mojang behavior with no mods/plugins.

## Metadata

Read Mojang manifest:

```text
https://launchermeta.mojang.com/mc/game/version_manifest.json
```

Then read the selected version JSON to obtain:

- `downloads.server.url`
- `downloads.server.sha1`
- `javaVersion.majorVersion`

Download `server.jar` from the version JSON and verify SHA1 when feasible.

## Install Shape

- Install the required Java major version.
- Store jar as `/opt/minecraft/server.jar`.
- Start with:

```bash
java -Xms4G -Xmx4G -jar /opt/minecraft/server.jar nogui
```

Adjust memory for player count and world size. Vanilla has no mod/plugin dependency validation, so operational validation is mostly logs, port, and gameplay settings.

## Tuning

Vanilla has fewer server-side optimization options. Keep view/simulation distances conservative, pregenerate manually only with external tooling if needed, and consider Fabric or Paper if the user wants optimization or admin tooling.
