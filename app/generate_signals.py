import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "app" / "data"
CHART_DIR = BASE_DIR / "public" / "static" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

# Freight proxy data
lng = pd.read_csv(DATA_DIR / "lng_freight_proxy_comtrade.csv")
oil = pd.read_csv(DATA_DIR / "oil_freight_proxy.csv")
vessel = pd.read_csv(DATA_DIR / "lng_vessel_signal_sample.csv")

lng["period"] = lng["period"].astype(int)
oil["period"] = oil["period"].astype(int)
vessel["period"] = vessel["period"].astype(int)

# LNG vs Oil comparison
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

# LNG freight proxy + vessel dwell time
combined = pd.merge(
    lng[["period", "lng_freight_proxy"]],
    vessel[["period", "lng_port_calls", "avg_dwell_hours", "avg_voyage_days"]],
    on="period",
    how="inner"
).sort_values("period")

fig, ax1 = plt.subplots(figsize=(9, 5))

ax1.plot(
    combined["period"],
    combined["lng_freight_proxy"],
    marker="o",
    label="LNG freight proxy"
)
ax1.set_xlabel("Year")
ax1.set_ylabel("LNG freight proxy (USD/kg)")
ax1.grid(True)

ax2 = ax1.twinx()
ax2.plot(
    combined["period"],
    combined["avg_dwell_hours"],
    marker="s",
    linestyle="--",
    label="Avg dwell hours"
)
ax2.set_ylabel("Average dwell time (hours)")

plt.title("LNG Freight Proxy and Vessel Dwell Time")

lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="upper left")

plt.tight_layout()
plt.savefig(CHART_DIR / "lng_freight_vessel_signal.png", dpi=160)
plt.close()

combined.to_csv(CHART_DIR / "lng_freight_vessel_signal.csv", index=False)

print("Generated:")
print(f"- {CHART_DIR / 'freight_proxy.png'}")
print(f"- {CHART_DIR / 'lng_freight_vessel_signal.png'}")
