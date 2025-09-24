#!/usr/bin/env python3
"""
Tidy raw files: move raw artifacts from analysis/data/raw/** to data/raw/**

This helps centralize provenance. The script only moves files that do not
already exist at the destination (by content hash). If duplicates exist, the
source file is left in place and a message is printed.
"""

import os
import shutil
import hashlib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(ROOT, 'analysis', 'data', 'raw')
DST = os.path.join(ROOT, 'data', 'raw')


def _hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    if not os.path.isdir(SRC):
        print("No analysis/data/raw directory found; nothing to tidy.")
        return 0

    os.makedirs(DST, exist_ok=True)

    moved = 0
    skipped = 0
    for root, _, files in os.walk(SRC):
        for fn in files:
            if not (fn.lower().endswith('.json') or fn.lower().endswith('.md')):
                continue
            src_path = os.path.join(root, fn)
            rel = os.path.relpath(src_path, SRC)
            dst_path = os.path.join(DST, rel)
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)

            if os.path.exists(dst_path):
                # Compare content; if identical, keep destination and leave source (manual cleanup later)
                try:
                    if _hash(src_path) == _hash(dst_path):
                        print(f"DUPLICATE (identical): {os.path.relpath(src_path, ROOT)} == {os.path.relpath(dst_path, ROOT)}")
                        skipped += 1
                        continue
                except Exception:
                    pass

                # If different content under same name, avoid overwriting; add suffix
                base, ext = os.path.splitext(dst_path)
                suffix = 1
                while os.path.exists(f"{base}_from_analysis_{suffix}{ext}"):
                    suffix += 1
                dst_path = f"{base}_from_analysis_{suffix}{ext}"

            # Move (preserve metadata where possible)
            shutil.move(src_path, dst_path)
            print(f"MOVED -> {os.path.relpath(dst_path, ROOT)}")
            moved += 1

    print(f"Done. Moved: {moved}, Skipped (duplicates or non-raw): {skipped}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
