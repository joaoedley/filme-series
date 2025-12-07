import os
import urllib.request
import urllib.error
from pathlib import Path

STORAGE_ZONE = os.getenv("BUNNY_STORAGE_ZONE", "")
STORAGE_KEY = os.getenv("BUNNY_STORAGE_KEY", "")  # Storage Password (not API key)
PULL_HOST = os.getenv("BUNNY_CDN_PULL_ZONE_HOSTNAME", "")


def upload_to_bunny(local_path: str, remote_path: str) -> str:
    """
    Envia um arquivo local para Bunny Storage usando HTTP PUT e retorna a URL pública na CDN.

    remote_path: caminho relativo (sem barra inicial), ex.: "covers/filme-x.jpg"
    """
    if not STORAGE_ZONE or not STORAGE_KEY or not PULL_HOST:
        raise RuntimeError("Configure BUNNY_STORAGE_ZONE, BUNNY_STORAGE_KEY e BUNNY_CDN_PULL_ZONE_HOSTNAME no .env")

    url = f"https://storage.bunnycdn.com/{STORAGE_ZONE}/{remote_path}"
    data = Path(local_path).read_bytes()
    req = urllib.request.Request(url, method="PUT", data=data)
    req.add_header("AccessKey", STORAGE_KEY)
    # opcional: content-type pode ser inferido pelo Bunny; não é obrigatório
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            if resp.status not in (200, 201):
                raise RuntimeError(f"Bunny upload falhou: HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Bunny upload HTTPError: {e.code} {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Bunny upload URLError: {e.reason}") from e

    return f"https://{PULL_HOST}/{remote_path}"
