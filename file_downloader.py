import os
import requests
def download_file(url: str, dest_path: str) -> bool:
    print(f"Downloading file {url}...")
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        return True
    try:
        resp = requests.get(url, stream=True, timeout=30)
        resp.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except requests.RequestException as e:
        print(f"Failed to download {url}: {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return False