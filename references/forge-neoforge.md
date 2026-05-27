# Forge And NeoForge

Use Forge/NeoForge when a modpack requires it. Do not choose it for generic optimization.

## Workflow

- Identify exact Minecraft version and loader family required by the modpack.
- Use the loader's official installer or official project metadata.
- Install server files into `/opt/minecraft` as `minecraft`.
- Read generated run scripts; modern Forge/NeoForge often uses `run.sh` and argument files rather than `java -jar server.jar`.
- Make systemd call the generated server launch script or the exact documented Java invocation.

## Compatibility

- Match every mod to Minecraft version and loader family.
- Do not mix Fabric, Quilt, Forge, and NeoForge mods.
- Expect extra dependencies and config generation on first run.
- Validate by reading logs for missing mod IDs, Java mismatch, or rejected version ranges.

## Tuning

- Keep memory higher than vanilla/Fabric for large modpacks, but leave OS cache room.
- Avoid adding generic optimization mods unless the modpack documentation recommends them.
- Use Spark where compatible for profiling.
