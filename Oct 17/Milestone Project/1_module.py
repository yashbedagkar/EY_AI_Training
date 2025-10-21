import pandas as pd

# Load initial data from CSV files
products_df = pd.read_csv('products.csv')
warehouses_df = pd.read_csv('warehouses.csv')

# Display the initial tables
print("Initial Products Data:")
print(products_df)
print("\nInitial Warehouses Data:")
print(warehouses_df)


# 1. Add a new product
def add_product(product_id, product_name, category, unit_price):
    global products_df
    # Check if product_id already exists to avoid duplicates
    if product_id in products_df['ProductID'].values:
        print(f"Product with ID {product_id} already exists.")
        return
    new_product = {
        'ProductID': product_id,
        'ProductName': product_name,
        'Category': category,
        'UnitPrice': unit_price
    }
    products_df = pd.concat([products_df, pd.DataFrame([new_product])], ignore_index=True)
    print(f"Added new product: {new_product}")


# 2. Update warehouse capacity
def update_warehouse_capacity(warehouse_id, new_capacity):
    global warehouses_df
    if warehouse_id not in warehouses_df['WarehouseID'].values:
        print(f"Warehouse with ID {warehouse_id} not found.")
        return
    warehouses_df.loc[warehouses_df['WarehouseID'] == warehouse_id, 'Capacity'] = new_capacity
    print(f"Updated capacity for warehouse {warehouse_id} to {new_capacity}")


# 3. Delete a product
def delete_product(product_id):
    global products_df
    if product_id not in products_df['ProductID'].values:
        print(f"Product with ID {product_id} not found.")
        return
    products_df = products_df[products_df['ProductID'] != product_id]
    print(f"Deleted product with ID {product_id}")


# 4. Fetch all products in Electronics category
def get_electronics_products():
    electronics = products_df[products_df['Category'].str.lower() == 'electronics']
    print("\nProducts in Electronics category:")
    print(electronics)
    return electronics


# Testing CRUD operations

# Add a new product
add_product('P106', 'Smartphone', 'Electronics', 600)

# Update warehouse capacity
update_warehouse_capacity('W02', 900)

# Delete a product
delete_product('P105')

# Fetch all Electronics products
electronics_products = get_electronics_products()

# Display updated DataFrames
print("\nUpdated Products Data:")
print(products_df)

print("\nUpdated Warehouses Data:")
print(warehouses_df)
