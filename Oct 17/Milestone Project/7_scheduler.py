import schedule
import time
import pandas as pd
from datetime import datetime


def daily_shipment_summary():
    # Load the processed shipments file
    df = pd.read_csv("processed_shipments.csv")

    # Convert DispatchDate to datetime
    df["DispatchDate"] = pd.to_datetime(df["DispatchDate"])

    # Get today’s date for filtering summary (optional: to summarize only today's shipments)
    today = datetime.now().date()

    # Filter shipments dispatched today (or you can skip filtering if summary is for all data)
    today_shipments = df[df["DispatchDate"].dt.date == today]

    # If you want the entire dataset summary (not just today), comment out the filtering line above

    # Format filename
    filename = f"daily_shipments_{today.strftime('%Y%m%d')}.csv"

    # Save daily summary CSV
    today_shipments.to_csv(filename, index=False)

    print(f" Daily shipment summary saved to {filename}")


# Schedule the job every day at 07:00 AM
schedule.every().day.at("07:00").do(daily_shipment_summary)

print(" Scheduler started. Waiting for next run at 07:00 AM...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # check every 60 seconds
