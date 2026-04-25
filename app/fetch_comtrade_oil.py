from pathlib import Path
import time
import requests
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "app" / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"


def fetch(reporter, partner, cmd, flow, period):
    params = {
        "reporterCode": reporter,
        "partnerCode": partner,
        "cmdCode": cmd,
        "flowCode": flow,
        "period": period,
    }
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    data = r.json().get("data", [])
    return data[0] if data else None


def unit(v, q):
    if v is None or q in (None, 0):
        return None
    return v / q


rows = []
for year in range(2018, 2025):
    print(f"Fetching {year}...")
    
    jp = fetch(392, 0, "2709", "M", str(year))
    au = fetch(36, 0, "2709", "X", str(year))

    if not jp or not au:
        continue

    cif = unit(jp.get("cifvalue"), jp.get("qty"))
    fob = unit(au.get("fobvalue"), au.get("qty"))

    if cif and fob:
        rows.append({
            "period": year,
            "oil_proxy": cif - fob
        })

    time.sleep(1)

df = pd.DataFrame(rows)
df.to_csv(OUT_DIR / "oil_freight_proxy.csv", index=False)
print(df)
