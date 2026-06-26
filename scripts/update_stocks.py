from pathlib import Path
import pandas as pd

NASDAQ_URL = "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"
OTHER_URL = "https://www.nasdaqtrader.com/dynamic/symdir/otherlisted.txt"
NSE_URL = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "stocks.csv"


def load_nasdaq():
    df = pd.read_csv(NASDAQ_URL, sep="|")

    df = df[df["Symbol"] != "File Creation Time:"]

    df = df.rename(
        columns={
            "Symbol": "Ticker",
            "Security Name": "Company"
        }
    )

    df["Exchange"] = "NASDAQ"
    df["Country"] = "USA"

    return df[["Company", "Ticker", "Exchange", "Country"]]


def load_other():
    df = pd.read_csv(OTHER_URL, sep="|")

    df = df[df["ACT Symbol"] != "File Creation Time:"]

    df = df.rename(
        columns={
            "ACT Symbol": "Ticker",
            "Security Name": "Company"
        }
    )

    exchange_map = {
        "N": "NYSE",
        "A": "NYSE American",
        "P": "NYSE Arca",
        "Z": "BATS",
        "V": "IEX"
    }

    df["Exchange"] = df["Exchange"].map(exchange_map)
    df["Country"] = "USA"

    return df[["Company", "Ticker", "Exchange", "Country"]]


def load_nse():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    df = pd.read_csv(
        NSE_URL,
        storage_options=headers
    )

    df = df.rename(
        columns={
            "SYMBOL": "Ticker",
            "NAME OF COMPANY": "Company"
        }
    )

    df["Ticker"] = df["Ticker"] + ".NS"
    df["Exchange"] = "NSE"
    df["Country"] = "India"

    return df[["Company", "Ticker", "Exchange", "Country"]]


def clean(df):
    df["Company"] = (
        df["Company"]
        .astype(str)
        .str.strip()
    )

    df["Ticker"] = (
        df["Ticker"]
        .astype(str)
        .str.strip()
    )

    df = df.drop_duplicates(subset="Ticker")
    df = df.dropna()

    df = df.sort_values("Company")

    df["Search"] = (
        df["Company"].str.lower()
        + " "
        + df["Ticker"].str.lower()
    )

    return df


def main():
    print("Downloading US stocks...")

    us1 = load_nasdaq()
    us2 = load_other()

    print("Downloading Indian stocks...")

    india = load_nse()

    stocks = pd.concat(
        [us1, us2, india],
        ignore_index=True
    )

    stocks = clean(stocks)

    stocks.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nSaved {len(stocks)} stocks.")
    print(f"Location: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()