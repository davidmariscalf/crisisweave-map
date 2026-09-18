#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import tarfile
import urllib.request
from pathlib import Path

MAPLIBRE_VERSION = "5.6.1"
PACKAGE_URL = f"https://registry.npmjs.org/maplibre-gl/-/maplibre-gl-{MAPLIBRE_VERSION}.tgz"
PACKAGE_SHA512 = "TTSfoTaF7RqKUR9wR5qDxCHH2J1XfZ1E85luiLOx0h8r50T/LnwAwwfV0WVNh9o8dA7rwt57Ucivf1emyeukXg=="
FILES = {
    "package/dist/maplibre-gl.js": "maplibre-gl.js",
    "package/dist/maplibre-gl.css": "maplibre-gl.css",
    "package/LICENSE.txt": "MAPLIBRE_LICENSE.txt",
}

def _download() -> bytes:
    request = urllib.request.Request(PACKAGE_URL, headers={"User-Agent": "CrisisWeave field package builder"})
    with urllib.request.urlopen(request, timeout=60) as response:
        if response.status != 200:
            raise RuntimeError(f"MapLibre package download failed with HTTP {response.status}")
        data = response.read()
    actual = base64.b64encode(hashlib.sha512(data).digest()).decode("ascii")
    if actual != PACKAGE_SHA512:
        raise RuntimeError("MapLibre package integrity check failed")
    return data

def package_maplibre(destination: Path) -> list[Path]:
    destination.mkdir(parents=True, exist_ok=True)
    data = _download()
    written: list[Path] = []
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
        members = {member.name: member for member in archive.getmembers()}
        for source_name, output_name in FILES.items():
            member = members.get(source_name)
            if member is None or not member.isfile():
                raise RuntimeError(f"MapLibre package is missing {source_name}")
            source = archive.extractfile(member)
            if source is None:
                raise RuntimeError(f"Could not read {source_name} from MapLibre package")
            output = destination / output_name
            output.write_bytes(source.read())
            written.append(output)
    return written

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Package pinned MapLibre assets for CrisisWeave")
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    for path in package_maplibre(args.destination):
        print(path)
