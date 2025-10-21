import pandas as pd

# Step 1: Extract
products_df = pd.read_csv("products.csv")
warehouses_df = pd.read_csv("warehouses.csv")
shipments_df = pd.read_csv("shipments.csv")

# Convert date columns to datetime
shipments_df["DispatchDate"] = pd.to_datetime(shipments_df["DispatchDate"])
shipments_df["DeliveryDate"] = pd.to_datetime(shipments_df["DeliveryDate"])

# Step 2: Transform

# Merge with products to get UnitPrice, ProductName, Category
merged_df = pd.merge(shipments_df, products_df, on="ProductID", how="left")

# Merge with warehouses to get Location and Capacity
merged_df = pd.merge(merged_df, warehouses_df, on="WarehouseID", how="left")

# Calculate TotalValue = Quantity * UnitPrice
merged_df["TotalValue"] = merged_df["Quantity"] * merged_df["UnitPrice"]

# Calculate DeliveryDays = DeliveryDate - DispatchDate
merged_df["DeliveryDays"] = (merged_df["DeliveryDate"] - merged_df["DispatchDate"]).dt.days

# Optional: Reorder columns for clarity
processed_df = merged_df[[
    "ShipmentID", "ProductID", "ProductName", "Category",
    "WarehouseID", "Location", "Quantity",
    "DispatchDate", "DeliveryDate", "DeliveryDays",
    "UnitPrice", "TotalValue"
]]

# Step 3: Load
processed_df.to_csv("processed_shipments.csv", index=False)

print("ETL completed. File saved as 'processed_shipments.csv'.")
