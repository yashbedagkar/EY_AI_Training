import csv

with open('sales.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['product', 'price', 'quantity'])
    writer.writerow(['Laptop', 70000, 2])
    writer.writerow(['Mouse', 500, 5])
    writer.writerow(['Keyboard', 1200, 3])

import pandas as pd
import logging

logging.basicConfig(filename='sales.log', level=logging.INFO)

try:
    df = pd.read_csv('sales.csv')
    for index, row in df.iterrows():
        try:
            total_sales = float(row['price']) * int(row['quantity'])
            print(f"{row['product']}: ₹{total_sales}")
            logging.info(f"Computed total sales for {row['product']}")
        except ValueError:
            print(f"Invalid numeric value for product: {row['product']}")
except FileNotFoundError:
    print("The file sales.csv was not found.")
