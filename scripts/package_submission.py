#!/usr/bin/env python3
import os
import zipfile
from pathlib import Path

def package_project():
    root_dir = Path(__file__).resolve().parent.parent
    zip_path = root_dir / "darukaa_earth_ai_biodiversity.zip"
    exclude = {'.git', 'node_modules', 'dist', '.aistudio', '__pycache__', '.pytest_cache'}
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in exclude]
            for f in files:
                if f.endswith('.zip') or f.endswith('.pyc'):
                    continue
                p = Path(root) / f
                rel = p.relative_to(root_dir)
                z.write(p, Path("darukaa_earth_ai_biodiversity") / rel)

    print(f"Successfully packaged project into: {zip_path} ({zip_path.stat().st_size} bytes)")

if __name__ == "__main__":
    package_project()
