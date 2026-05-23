from fastapi import FastAPI, HTTPException

app = FastAPI()

# This is our "database" for now — just a dictionary in memory
inventory = {
    "product-001": {"name": "Wireless Mouse", "stock": 50},
    "product-002": {"name": "Mechanical Keyboard", "stock": 30},
    "product-003": {"name": "USB-C Hub", "stock": 15},
}

# Health check — confirms the service is alive
@app.get("/health")
def health():
    return {"status": "inventory service is running"}

# Get all products
@app.get("/inventory")
def get_all_inventory():
    return inventory

# Get one product by ID
@app.get("/inventory/{product_id}")
def get_product(product_id: str):
    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    return inventory[product_id]

# Reduce stock when an item is purchased
@app.post("/inventory/{product_id}/reduce")
def reduce_stock(product_id: str, quantity: int):
    if product_id not in inventory:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if inventory[product_id]["stock"] < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")
    
    inventory[product_id]["stock"] -= quantity
    return {
        "message": "Stock updated",
        "product_id": product_id,
        "remaining_stock": inventory[product_id]["stock"]
    }