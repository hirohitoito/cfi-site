from pathlib import Path
import time
import requests
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "app" / "data"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"


def fetch_comtrade(reporter_code, partner_code, cmd_code, flow_code, period, max_retries=5):
    params = {
        "reporterCode": reporter_code,
        "partnerCode": partner_code,
        "cmdCode": cmd_code,
        "flowCode": flow_code,
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
        return r.json().get("data", [])

    print(f"  Failed after retries: {params}")
    return []


def first_record(data):
    return data[0] if data else None


def safe_unit(value, qty):
    if value is None or qty in (None, 0):
        return None
    return value / qty


def main():
    years = range(2018, 2025)
    cmd_code = "271111"  # LNG
    rows = []

    for year in years:
        period = str(year)
        print(f"Fetching {period}...")

        japan_import = first_record(
            fetch_comtrade(
                reporter_code=392,
                partner_code=0,
                cmd_code=cmd_code,
                flow_code="M",
                period=period,
            )
        )

        time.sleep(3)

        australia_export = first_record(
            fetch_comtrade(
                reporter_code=36,
                partner_code=0,
                cmd_code=cmd_code,
                flow_code="X",
                period=period,
            )
        )

        time.sleep(8)

        if japan_import is None or australia_export is None:
            print(f"  Skipped {period}: missing data")
            continue

        japan_cif_value = japan_import.get("cifvalue")
        japan_qty = japan_import.get("qty")
        australia_fob_value = australia_export.get("fobvalue")
        australia_qty = australia_export.get("qty")

        japan_cif_unit = safe_unit(japan_cif_value, japan_qty)
        australia_fob_unit = safe_unit(australia_fob_value, australia_qty)

        if japan_cif_unit is None or australia_fob_unit is None:
            print(f"  Skipped {period}: missing value or quantity")
            continue

        rows.append(
            {
                "period": period,
                "commodity": "LNG",
                "cmd_code": cmd_code,
                "japan_import_cif_value": japan_cif_value,
                "japan_import_qty": japan_qty,
                "japan_cif_unit_value": japan_cif_unit,
                "australia_export_fob_value": australia_fob_value,
                "australia_export_qty": australia_qty,
                "australia_fob_unit_value": australia_fob_unit,
                "lng_freight_proxy": japan_cif_unit - australia_fob_unit,
            }
        )

    result = pd.DataFrame(rows)
    out_path = OUT_DIR / "lng_freight_proxy_comtrade.csv"
    result.to_csv(out_path, index=False)

    print(result)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
