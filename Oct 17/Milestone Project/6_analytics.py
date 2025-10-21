import pandas as pd
import os

# Create reports folder if not exist
os.makedirs("reports", exist_ok=True)

# Load processed shipment data
df = pd.read_csv("processed_shipments.csv")

# Convert dates to datetime
df["DispatchDate"] = pd.to_datetime(df["DispatchDate"])
df["DeliveryDate"] = pd.to_datetime(df["DeliveryDate"])

# 1. Average delivery time per warehouse
avg_delivery = df.groupby("WarehouseID")["DeliveryDays"].mean().reset_index()
avg_delivery.columns = ["WarehouseID", "AverageDeliveryDays"]

# 2. Total shipment value per product category
total_value = df.groupby("Category")["TotalValue"].sum().reset_index()
total_value.columns = ["Category", "TotalShipmentValue"]

# 3. Number of shipments per month
df["Month"] = df["DispatchDate"].dt.to_period("M").astype(str)
shipments_month = df.groupby("Month")["ShipmentID"].count().reset_index()
shipments_month.columns = ["Month", "ShipmentCount"]

# 4. Late deliveries (DeliveryDays > 5)
late_deliveries = df[df["DeliveryDays"] > 5][
    ["ShipmentID", "ProductID", "WarehouseID", "DeliveryDays"]
]

# ------------------ Save to CSV ------------------ #
with open("reports/logistics_analytics.csv", "w") as f:
    f.write("Average Delivery Time per Warehouse\n")
    avg_delivery.to_csv(f, index=False)
    f.write("\nTotal Shipment Value per Product Category\n")
    total_value.to_csv(f, index=False)
    f.write("\nNumber of Shipments per Month\n")
    shipments_month.to_csv(f, index=False)
    f.write("\nLate Deliveries (DeliveryDays > 5)\n")
    late_deliveries.to_csv(f, index=False)

print("✅ Saved to reports/logistics_analytics.csv")
