from pathlib import Path
import time
import requests
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "app" / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"


def fetch(reporter, partner, cmd, flow, period, max_retries=5):
    params = {
        "reporterCode": reporter,
        "partnerCode": partner,
        "cmdCode": cmd,
        "flowCode": flow,
        "period": period,
    }

    for attempt in range(max_retries):
        r = requests.get(BASE_URL, params=params, timeout=30)

        if r.status_code == 429:
            wait = 10 * (attempt + 1)
            print(f"  429 Too Many Requests. Waiting {wait} seconds...")
            time.sleep(wait)
            continue

        r.raise_for_status()
        data = r.json().get("data", [])
        return data[0] if data else None

    print(f"  Failed after retries: {params}")
    return None


def unit(value, qty):
    if value is None or qty in (None, 0):
        return None
    return value / qty


def main():
    rows = []

    for year in range(2018, 2025):
        print(f"Fetching {year}...")

        jp = fetch(392, 0, "2709", "M", str(year))
        time.sleep(3)

        au = fetch(36, 0, "2709", "X", str(year))
        time.sleep(8)

        if not jp or not au:
            print(f"  Skipped {year}: missing data")
            continue

        cif = unit(jp.get("cifvalue"), jp.get("qty"))
        fob = unit(au.get("fobvalue"), au.get("qty"))

        if cif is None or fob is None:
            print(f"  Skipped {year}: missing cif/fob/qty")
            continue

        rows.append({
            "period": year,
            "oil_cif_unit_value": cif,
            "oil_fob_unit_value": fob,
            "oil_proxy": cif - fob,
        })

    df = pd.DataFrame(rows)
    out_path = OUT_DIR / "oil_freight_proxy.csv"
    df.to_csv(out_path, index=False)

    print(df)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
