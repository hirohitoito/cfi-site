import matplotlib
matplotlib.use("Agg")

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "app" / "data" / "freight_proxy_sample.csv"
CHART_DIR = BASE_DIR / "public" / "static" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"])

# CIF - FOB = freight + insurance proxy
df["lng_freight_proxy"] = df["lng_cif"] - df["lng_fob"]
df["oil_freight_proxy"] = df["oil_cif"] - df["oil_fob"]

plt.figure(figsize=(9, 5))
plt.plot(df["date"], df["lng_freight_proxy"], marker="o", label="LNG CIF-FOB proxy")
plt.plot(df["date"], df["oil_freight_proxy"], marker="o", label="Oil CIF-FOB proxy")
plt.title("Freight Proxy: CIF - FOB")
plt.xlabel("Date")
plt.ylabel("Proxy value")
plt.legend()
plt.grid(True)
plt.tight_layout()

output_path = CHART_DIR / "freight_proxy.png"
plt.savefig(output_path, dpi=160)
plt.close()

# Save processed data as CSV
processed_path = BASE_DIR / "public" / "static" / "charts" / "freight_proxy_processed.csv"
df.to_csv(processed_path, index=False)

print(f"Generated: {output_path}")
