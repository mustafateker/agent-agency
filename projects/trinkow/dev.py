"""Yerel MongoDB + API + Expo. Atlas .env dosyasını değiştirmez."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import time
import urllib.request


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-app", action="store_true", help="Yalnız MongoDB ve API")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    local = root / ".local"
    local.mkdir(exist_ok=True)
    data = local / "data"
    data.mkdir(exist_ok=True)
    mongod = shutil.which("mongod") or str(local / "mongodb/bin/mongod")
    if not Path(mongod).is_file():
        raise SystemExit("MongoDB bulunamadı. app/README.md içindeki yerel kurulum adımını uygula.")
    env = dict(os.environ, MONGODB_URI="mongodb://127.0.0.1:27018", MONGODB_DB_NAME="trinkow_demo",
               TRINKOW_DEV_LOGIN="1", EXPO_PUBLIC_DEV_LOGIN="1")
    processes: list[subprocess.Popen] = []
    try:
        processes.append(subprocess.Popen([
            mongod, "--dbpath", str(data), "--port", "27018", "--bind_ip", "127.0.0.1",
            "--logpath", str(local / "mongodb.log"), "--logappend",
        ]))
        processes.append(subprocess.Popen([
            str(root / "backend/.venv/bin/python"), "-m", "uvicorn", "app.main:app",
            "--host", "0.0.0.0", "--port", "8000",
        ], cwd=root / "backend", env=env))
        for _ in range(60):
            if any(p.poll() is not None for p in processes):
                raise SystemExit("Yerel servis başlatılamadı; terminal çıktısını ve .local/mongodb.log dosyasını kontrol et.")
            try:
                with urllib.request.urlopen("http://127.0.0.1:8000/saglik", timeout=1) as response:
                    if response.status == 200:
                        break
            except OSError:
                time.sleep(0.5)
        else:
            raise SystemExit("API zamanında hazır olmadı.")
        print("Yerel API hazır. Test girişi açık; veriler .local/data içinde kalıcıdır.", flush=True)
        if not args.no_app:
            processes.append(subprocess.Popen(["npm", "start"], cwd=root / "app", env=env))
        while all(p.poll() is None for p in processes):
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        for process in reversed(processes):
            if process.poll() is None:
                process.terminate()
        for process in reversed(processes):
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    main()
