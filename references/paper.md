# Paper, Purpur, And Folia

Use Paper/Purpur for plugin servers, public/community servers, and admin-heavy setups. Use Folia only when plugin compatibility is confirmed.

## Metadata

Use official PaperMC API rather than scraping:

```text
https://api.papermc.io/v2/projects/paper
https://api.papermc.io/v2/projects/paper/versions/<mc>
https://api.papermc.io/v2/projects/paper/versions/<mc>/builds/<build>/downloads/<filename>
```

For Purpur, use official Purpur API/downloads. For Folia, use PaperMC project metadata for `folia`.

## Install Shape

- Store jar as `/opt/minecraft/server.jar`.
- Start with `java ... -jar /opt/minecraft/server.jar nogui`.
- Use plugins in `/opt/minecraft/plugins`, not Fabric mods.

## Baseline Plugins

Install only when compatible with the selected server and version:

- Spark for profiling.
- Chunky for pregeneration.
- LuckPerms for permissions on public/plugin servers.
- CoreProtect or Ledger-equivalent block logging where supported.
- A maintained backup plugin or system-level backup plan.

## Configuration

Paper/Purpur exposes many config files. Do not apply random internet tuning packs blindly. Prefer:

- Conservative view/simulation distance.
- Pregeneration and world border.
- Entity/farm controls based on observed Spark data.
- Plugin compatibility checks before Folia.
