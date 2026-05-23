from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

INVENTORY_SERVICE_URL = "http://127.0.0.1:8001"

# In-memory cart storage
carts = {}

@app.get("/health")
def health():
    return {"status": "cart service is running"}

# View a cart
@app.get("/cart/{user_id}")
def get_cart(user_id: str):
    if user_id not in carts:
        return {"user_id": user_id, "items": [], "total_items": 0}
    return carts[user_id]

# Add item to cart
@app.post("/cart/{user_id}/add")
def add_to_cart(user_id: str, product_id: str, quantity: int):
    
    # First — check inventory service if item is in stock
    try:
        response = requests.get(f"{INVENTORY_SERVICE_URL}/inventory/{product_id}")
    except Exception:
        raise HTTPException(status_code=503, detail="Inventory service unreachable")

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Product not found in inventory")

    product = response.json()

    if product["stock"] < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    # Build the cart for this user if it doesn't exist
    if user_id not in carts:
        carts[user_id] = {"user_id": user_id, "items": [], "total_items": 0}

    # Check if product already in cart — if so, increase quantity
    for item in carts[user_id]["items"]:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            carts[user_id]["total_items"] += quantity
            return carts[user_id]

    # Otherwise add as new item
    carts[user_id]["items"].append({
        "product_id": product_id,
        "name": product["name"],
        "quantity": quantity
    })
    carts[user_id]["total_items"] += quantity

    return carts[user_id]

# Remove item from cart
@app.delete("/cart/{user_id}/remove/{product_id}")
def remove_from_cart(user_id: str, product_id: str):
    if user_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")

    cart = carts[user_id]
    cart["items"] = [i for i in cart["items"] if i["product_id"] != product_id]
    cart["total_items"] = sum(i["quantity"] for i in cart["items"])

    return cart

# Clear entire cart
@app.delete("/cart/{user_id}/clear")
def clear_cart(user_id: str):
    if user_id not in carts:
        raise HTTPException(status_code=404, detail="Cart not found")
    carts[user_id] = {"user_id": user_id, "items": [], "total_items": 0}
    return {"message": "Cart cleared"}