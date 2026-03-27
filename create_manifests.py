"""
Create manifest.json and description.md in each subfolder, zip the
'textures' subfolder into Assets.zip, then remove the original textures folder.

Usage:
    python create_manifests.py                  # uses current directory
    python create_manifests.py "C:\My\Textures" # uses specified path
"""

import json
import os
import shutil
import sys
import zipfile


def build_manifest(folder_name: str) -> dict:
    display_name = folder_name.replace("_", " ").title()
    return {
        "name": display_name,
        "creator": "Quixel",
        "category": "Textures",
        "filename": "Assets.zip",
        "tags": "",
        "website": "",
        "powerplug": {
            "mode": "textures",
            "src": "textures",
        },
    }


def zip_textures(folder_path: str) -> bool:
    """Zip the 'textures' subfolder into Assets.zip and delete the original.
    Returns True if work was done, False if skipped."""
    textures_dir = os.path.join(folder_path, "textures")
    zip_path = os.path.join(folder_path, "Assets.zip")

    if not os.path.isdir(textures_dir):
        print(f"         ! No 'textures' subfolder -- skipping zip")
        return False

    if os.path.exists(zip_path):
        print(f"         ! Assets.zip already exists -- skipping zip")
        return False

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(textures_dir):
            for file in files:
                abs_path = os.path.join(root, file)
                arc_name = os.path.relpath(abs_path, folder_path)
                zf.write(abs_path, arc_name)

    shutil.rmtree(textures_dir)
    print(f"         > Zipped & removed textures/")
    return True


def create_description(folder_path: str) -> bool:
    """Create an empty description.md. Returns True if created, False if skipped."""
    desc_path = os.path.join(folder_path, "description.md")

    if os.path.exists(desc_path):
        print(f"         description.md already exists -- skip")
        return False

    with open(desc_path, "w", encoding="utf-8") as f:
        f.write("")

    print(f"         > Created description.md")
    return True


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    root = os.path.abspath(root)

    if not os.path.isdir(root):
        print(f"Error: '{root}' is not a valid directory.")
        sys.exit(1)

    manifests_created = 0
    manifests_skipped = 0
    descriptions_created = 0
    zipped = 0

    for entry in sorted(os.listdir(root)):
        folder_path = os.path.join(root, entry)
        if not os.path.isdir(folder_path):
            continue

        print(f"  [{entry}]")

        # --- manifest.json ---
        manifest_path = os.path.join(folder_path, "manifest.json")
        if os.path.exists(manifest_path):
            print(f"         manifest.json already exists -- skip")
            manifests_skipped += 1
        else:
            manifest = build_manifest(entry)
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=4, ensure_ascii=False)
            print(f"         > Created manifest.json")
            manifests_created += 1

        # --- description.md ---
        if create_description(folder_path):
            descriptions_created += 1

        # --- zip textures ---
        if zip_textures(folder_path):
            zipped += 1

    print(f"\nDone -- {manifests_created} manifests, {descriptions_created} descriptions, {zipped} zipped.")


if __name__ == "__main__":
    main()
