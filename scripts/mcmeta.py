#!/usr/bin/env python3
"""Query Minecraft/Fabric/Modrinth metadata for server setup."""

import argparse
import hashlib
import json
import sys
import urllib.parse
import urllib.request


def get_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def minecraft_version(version: str):
    manifest = get_json("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    matches = [v for v in manifest["versions"] if v["id"] == version]
    if not matches:
        raise SystemExit(f"Minecraft version not found: {version}")
    data = get_json(matches[0]["url"])
    server = data.get("downloads", {}).get("server")
    print(json.dumps({
        "id": data["id"],
        "type": data["type"],
        "java_major": data.get("javaVersion", {}).get("majorVersion"),
        "server_url": server.get("url") if server else None,
        "server_sha1": server.get("sha1") if server else None,
        "server_size": server.get("size") if server else None,
    }, indent=2))


def fabric_loader(version: str):
    data = get_json(f"https://meta.fabricmc.net/v2/versions/loader/{urllib.parse.quote(version)}")
    stable = [x for x in data if x.get("loader", {}).get("stable")]
    selected = stable[0] if stable else data[0]
    print(json.dumps({
        "minecraft": version,
        "loader": selected["loader"]["version"],
        "loader_maven": selected["loader"]["maven"],
        "intermediary": selected["intermediary"]["version"],
    }, indent=2))


def fabric_installer():
    data = get_json("https://meta.fabricmc.net/v2/versions/installer")
    stable = [x for x in data if x.get("stable")]
    selected = stable[0] if stable else data[0]
    print(json.dumps(selected, indent=2))


def modrinth(slug: str, version: str, loader: str):
    query = urllib.parse.urlencode({
        "loaders": json.dumps([loader]),
        "game_versions": json.dumps([version]),
    })
    data = get_json(f"https://api.modrinth.com/v2/project/{urllib.parse.quote(slug)}/version?{query}")
    if not data:
        raise SystemExit(f"No Modrinth match for slug={slug} loader={loader} version={version}")
    selected = data[0]
    files = [f for f in selected["files"] if f.get("primary")] or selected["files"]
    file_info = files[0]
    print(json.dumps({
        "slug": slug,
        "name": selected["name"],
        "version_number": selected["version_number"],
        "version_type": selected["version_type"],
        "filename": file_info["filename"],
        "url": file_info["url"],
        "hashes": file_info.get("hashes", {}),
    }, indent=2))


def sha1(path: str):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    print(h.hexdigest())


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("minecraft-version")
    p.add_argument("version")
    sub.add_parser("fabric-installer")
    p = sub.add_parser("fabric-loader")
    p.add_argument("version")
    p = sub.add_parser("modrinth")
    p.add_argument("slug")
    p.add_argument("version")
    p.add_argument("--loader", default="fabric")
    p = sub.add_parser("sha1")
    p.add_argument("path")
    args = parser.parse_args()
    if args.cmd == "minecraft-version":
        minecraft_version(args.version)
    elif args.cmd == "fabric-installer":
        fabric_installer()
    elif args.cmd == "fabric-loader":
        fabric_loader(args.version)
    elif args.cmd == "modrinth":
        modrinth(args.slug, args.version, args.loader)
    elif args.cmd == "sha1":
        sha1(args.path)


if __name__ == "__main__":
    main()
