import pandas as pd

def run_pipeline():
    products = pd.read_csv("3_products.csv")
    customers = pd.read_csv("3_customers.csv")
    orders = pd.read_csv("3_orders.csv")

    orders_customers= pd.merge(orders,customers,on='CustomerID',how='inner')
    final_df = pd.merge(orders_customers, products, on='ProductID',how='inner')

    final_df["TotalAmount"] = final_df["Quantity"] * final_df["Price"]
    final_df["OrderDate"] = pd.to_datetime(final_df["OrderDate"])
    final_df["OrderMonth"] = final_df["OrderDate"].dt.month


    final_df = final_df[final_df["Quantity"] >= 2]
    final_df = final_df[final_df["Country"].isin(['India','UAE'])]

    revenue_per_category = final_df.groupby('Category')['TotalAmount'].sum().reset_index()

    revenue_per_customer_segment = final_df.groupby('Segment')['TotalAmount'].sum().reset_index()

    final_df = final_df.sort_values(by='TotalAmount', ascending=False)

    final_df.to_csv("3_processed_orders.csv", index=False)
    revenue_per_category.to_csv("3_category_summary.csv", index=False)
    revenue_per_customer_segment.to_csv("3_segment_summary.csv", index=False)

if __name__ == "__main__":
    run_pipeline()