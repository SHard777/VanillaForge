import os
import json
from datetime import datetime
import pandas as pd
import yfinance as yf
import seaborn as sns
import matplotlib.pyplot as plt


def fetch_market_data(
    ticker: str, start_date: str = None, end_date: str = None
) -> dict:
    """
    Downloads historical market data using yfinance, persists it locally as Parquet,
    generates a chart, and returns file paths and metadata.
    """
    try:
        # 1. Download Data
        ticker_obj = yf.Ticker(ticker)
        if start_date and end_date:
            df = ticker_obj.history(start=start_date, end=end_date)
        else:
            df = ticker_obj.history(
                period="1y"
            )  # Default to 1 year if no dates provided

        if df.empty:
            return {"error": f"No data found for ticker '{ticker}'."}

        # Ensure index is datetime for plotting and metadata
        df.index = pd.to_datetime(df.index)

        # 2. Setup Directory
        project_root = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        )
        temp_dir = os.path.join(project_root, "data_temp", ticker)
        os.makedirs(temp_dir, exist_ok=True)

        # File paths
        parquet_path = os.path.join(temp_dir, f"{ticker}_history.parquet")
        csv_path = os.path.join(temp_dir, f"{ticker}_history.csv")
        png_path = os.path.join(temp_dir, f"{ticker}_price_history.png")
        json_path = os.path.join(temp_dir, "metadata.json")

        # 3. Save Data (Parquet & CSV)
        df.to_parquet(parquet_path, engine="pyarrow")
        df.to_csv(csv_path)

        # 4. Generate Plot
        sns.set_theme(style="darkgrid")
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=df.index, y=df["Close"], label="Close Price")
        plt.title(f"Historical Closing Prices: {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Closing Price")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(png_path)
        plt.close()

        # 5. Metadata JSON

        metadata = {
            "ticker": ticker,
            "download_timestamp": datetime.now().isoformat(),
            "start_date": df.index.min().strftime("%Y-%m-%d"),
            "end_date": df.index.max().strftime("%Y-%m-%d"),
            "row_count": len(df),
            "available_columns": list(df.columns),
        }

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        # 6. Return Concise Summary
        return {
            "status": "success",
            "ticker": ticker,
            "message": "Historical market data successfully retrieved.",
            "files_created": [
                parquet_path.replace(project_root + os.sep, ""),
                csv_path.replace(project_root + os.sep, ""),
                png_path.replace(project_root + os.sep, ""),
                json_path.replace(project_root + os.sep, ""),
            ],
            "rows": len(df),
            "available_fields": ["Date"] + list(df.columns),
        }

    except Exception as e:
        return {"error": f"Failed to fetch market data: {str(e)}"}
