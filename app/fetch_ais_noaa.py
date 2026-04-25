from pathlib import Path
from urllib.parse import urljoin
import zipfile
import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "app" / "data" / "ais"
DATA_DIR.mkdir(parents=True, exist_ok=True)

YEAR = 2024
DATE = "2024_01_01"
BASE_URL = f"https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{YEAR}/"
TARGET_FILE = f"AIS_{DATE}.zip"

ZIP_PATH = DATA_DIR / TARGET_FILE
CSV_PATH = DATA_DIR / f"AIS_{DATE}.csv"
OUT_PATH = BASE_DIR / "app" / "data" / "ais_signal_sample.csv"


def find_zip_url():
    print(f"Checking NOAA directory: {BASE_URL}")
    r = requests.get(BASE_URL, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a"):
        href = a.get("href")
        if href == TARGET_FILE:
            return urljoin(BASE_URL, href)

    raise FileNotFoundError(f"{TARGET_FILE} not found in {BASE_URL}")


def download_zip(url):
    if ZIP_PATH.exists():
        print(f"Already exists: {ZIP_PATH}")
        return

    print(f"Downloading: {url}")
    with requests.get(url, stream=True, timeout=300) as r:
        r.raise_for_status()
        with open(ZIP_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    print(f"Saved: {ZIP_PATH}")


def validate_zip():
    print("Validating ZIP...")
    if not zipfile.is_zipfile(ZIP_PATH):
        raise zipfile.BadZipFile(f"Not a valid ZIP: {ZIP_PATH}")

    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        bad_file = z.testzip()
        if bad_file is not None:
            raise zipfile.BadZipFile(f"Corrupt file inside ZIP: {bad_file}")

    print("ZIP is valid.")


def unzip_file():
    if CSV_PATH.exists():
        print(f"Already extracted: {CSV_PATH}")
        return

    print("Extracting...")
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(DATA_DIR)

    print("Extracted.")


def analyze_ais():
    print("Reading AIS CSV...")

    usecols = ["MMSI", "BaseDateTime", "LAT", "LON", "SOG", "VesselType"]
    df = pd.read_csv(CSV_PATH, usecols=usecols)

    df["BaseDateTime"] = pd.to_datetime(df["BaseDateTime"], errors="coerce")
    df["date"] = df["BaseDateTime"].dt.date

    tanker = df[df["VesselType"].between(80, 89, inclusive="both")].copy()

    signal = tanker.groupby("date").agg(
        vessel_count=("MMSI", "nunique"),
        ais_points=("MMSI", "count"),
        avg_speed=("SOG", "mean"),
        slow_points=("SOG", lambda x: (x < 1.0).sum()),
    ).reset_index()

    signal.to_csv(OUT_PATH, index=False)

    print(signal)
    print(f"Saved: {OUT_PATH}")


def main():
    url = find_zip_url()
    download_zip(url)
    validate_zip()
    unzip_file()
    analyze_ais()


if __name__ == "__main__":
    main()
