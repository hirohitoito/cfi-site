import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "app" / "data"
CHART_DIR = BASE_DIR / "public" / "static" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# 1. Freight proxy: LNG vs Oil
lng = pd.read_csv(DATA_DIR / "lng_freight_proxy_comtrade.csv")
oil = pd.read_csv(DATA_DIR / "oil_freight_proxy.csv")

lng["period"] = lng["period"].astype(int)
oil["period"] = oil["period"].astype(int)

freight = pd.merge(
    lng[["period", "lng_freight_proxy"]],
    oil[["period", "oil_proxy"]],
    on="period",
    how="outer"
).sort_values("period")

plt.figure(figsize=(9, 5))
plt.plot(freight["period"], freight["lng_freight_proxy"], marker="o", label="LNG proxy")
plt.plot(freight["period"], freight["oil_proxy"], marker="o", label="Oil proxy")
plt.title("Freight Proxy Comparison: LNG vs Oil")
plt.xlabel("Year")
plt.ylabel("USD per kg")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(CHART_DIR / "freight_proxy.png", dpi=160)
plt.close()

freight.to_csv(CHART_DIR / "freight_proxy_comparison.csv", index=False)

# 2. AIS real signal: tanker movement
ais = pd.read_csv(DATA_DIR / "ais_signal_sample.csv")

plt.figure(figsize=(9, 5))
plt.bar(ais["date"].astype(str), ais["vessel_count"])
plt.title("AIS Tanker Signal: Vessel Count")
plt.xlabel("Date")
plt.ylabel("Unique tanker vessels")
plt.tight_layout()
plt.savefig(CHART_DIR / "ais_tanker_vessel_count.png", dpi=160)
plt.close()

plt.figure(figsize=(9, 5))
plt.bar(ais["date"].astype(str), ais["slow_points"])
plt.title("AIS Tanker Signal: Slow-Speed Points")
plt.xlabel("Date")
plt.ylabel("AIS points with SOG < 1 knot")
plt.tight_layout()
plt.savefig(CHART_DIR / "ais_tanker_slow_points.png", dpi=160)
plt.close()

ais.to_csv(CHART_DIR / "ais_signal_sample.csv", index=False)

print("Generated:")
print(f"- {CHART_DIR / 'freight_proxy.png'}")
print(f"- {CHART_DIR / 'ais_tanker_vessel_count.png'}")
print(f"- {CHART_DIR / 'ais_tanker_slow_points.png'}")
