import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "app" / "data"
CHART_DIR = BASE_DIR / "public" / "static" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

lng = pd.read_csv(DATA_DIR / "lng_freight_proxy_comtrade.csv")
oil = pd.read_csv(DATA_DIR / "oil_freight_proxy.csv")

lng["period"] = lng["period"].astype(int)
oil["period"] = oil["period"].astype(int)

df = pd.merge(
    lng[["period", "lng_freight_proxy"]],
    oil[["period", "oil_proxy"]],
    on="period",
    how="outer"
).sort_values("period")

plt.figure(figsize=(9, 5))
plt.plot(df["period"], df["lng_freight_proxy"], marker="o", label="LNG proxy")
plt.plot(df["period"], df["oil_proxy"], marker="o", label="Oil proxy")

plt.title("Freight Proxy Comparison: LNG vs Oil")
plt.xlabel("Year")
plt.ylabel("USD per kg")
plt.legend()
plt.grid(True)
plt.tight_layout()

output_path = CHART_DIR / "freight_proxy.png"
plt.savefig(output_path, dpi=160)
plt.close()

df.to_csv(CHART_DIR / "freight_proxy_comparison.csv", index=False)

print(df)
print(f"Generated: {output_path}")
