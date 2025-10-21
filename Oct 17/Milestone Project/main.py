from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# Load initial data from CSV
products_df = pd.read_csv('products.csv')
warehouses_df = pd.read_csv('warehouses.csv')

# Pydantic models for validation
class Product(BaseModel):
    ProductID: str
    ProductName: str
    Category: str
    UnitPrice: float

class Warehouse(BaseModel):
    WarehouseID: str
    Location: str
    Capacity: int


### --- PRODUCTS CRUD --- ###

@app.get("/products")
def get_products():
    return products_df.to_dict(orient="records")

@app.post("/products")
def add_product(product: Product):
    global products_df
    if product.ProductID in products_df['ProductID'].values:
        raise HTTPException(status_code=400, detail="Product ID already exists.")
    new_product = product.dict()
    products_df = pd.concat([products_df, pd.DataFrame([new_product])], ignore_index=True)
    return {"message": "Product added successfully", "product": new_product}

@app.put("/products/{product_id}")
def update_product(product_id: str, product: Product):
    global products_df
    if product_id not in products_df['ProductID'].values:
        raise HTTPException(status_code=404, detail="Product not found.")
    products_df.loc[products_df['ProductID'] == product_id, ['ProductName', 'Category', 'UnitPrice']] = \
        product.ProductName, product.Category, product.UnitPrice
    return {"message": f"Product {product_id} updated successfully"}

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    global products_df
    if product_id not in products_df['ProductID'].values:
        raise HTTPException(status_code=404, detail="Product not found.")
    products_df = products_df[products_df['ProductID'] != product_id]
    return {"message": f"Product {product_id} deleted successfully"}


### --- WAREHOUSES CRUD --- ###

@app.get("/warehouses")
def get_warehouses():
    return warehouses_df.to_dict(orient="records")

@app.post("/warehouses")
def add_warehouse(warehouse: Warehouse):
    global warehouses_df
    if warehouse.WarehouseID in warehouses_df['WarehouseID'].values:
        raise HTTPException(status_code=400, detail="Warehouse ID already exists.")
    new_warehouse = warehouse.dict()
    warehouses_df = pd.concat([warehouses_df, pd.DataFrame([new_warehouse])], ignore_index=True)
    return {"message": "Warehouse added successfully", "warehouse": new_warehouse}

@app.put("/warehouses/{warehouse_id}")
def update_warehouse(warehouse_id: str, warehouse: Warehouse):
    global warehouses_df
    if warehouse_id not in warehouses_df['WarehouseID'].values:
        raise HTTPException(status_code=404, detail="Warehouse not found.")
    warehouses_df.loc[warehouses_df['WarehouseID'] == warehouse_id, ['Location', 'Capacity']] = \
        warehouse.Location, warehouse.Capacity
    return {"message": f"Warehouse {warehouse_id} updated successfully"}

@app.delete("/warehouses/{warehouse_id}")
def delete_warehouse(warehouse_id: str):
    global warehouses_df
    if warehouse_id not in warehouses_df['WarehouseID'].values:
        raise HTTPException(status_code=404, detail="Warehouse not found.")
    warehouses_df = warehouses_df[warehouses_df['WarehouseID'] != warehouse_id]
    return {"message": f"Warehouse {warehouse_id} deleted successfully"}

