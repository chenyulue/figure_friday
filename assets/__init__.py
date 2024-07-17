from pathlib import Path

ASSETS = Path(__file__).parent

DATA24_WK28 = ASSETS / "data" / "Sample-Superstore.xls"
US_STATE = ASSETS / "data" / "us_state_code.csv"

if __name__ == "__main__":
    print(DATA24_WK28)