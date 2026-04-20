# Student Name: Alexandre Anthony
# Student Index: 10022200175

from pathlib import Path
from urllib.request import urlopen


DATASETS = {
    "Ghana_Election_Result.csv": "https://raw.githubusercontent.com/GodwinDansoAcity/acitydataset/main/Ghana_Election_Result.csv",
    "2025-Budget-Statement-and-Economic-Policy_v4.pdf": "https://mofep.gov.gh/sites/default/files/budget-statements/2025-Budget-Statement-and-Economic-Policy_v4.pdf",
}


def main() -> None:
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    for name, url in DATASETS.items():
        out_path = out_dir / name
        if out_path.exists() and out_path.stat().st_size > 0:
            print(f"Already exists: {out_path} ({out_path.stat().st_size} bytes)")
            continue

        print(f"Downloading {name} ...")
        with urlopen(url, timeout=120) as response:
            data = response.read()
        out_path.write_bytes(data)
        print(f"Saved: {out_path} ({out_path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()