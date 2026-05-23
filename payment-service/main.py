from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

INVENTORY_SERVICE_URL = "http://127.0.0.1:8001"
CART_SERVICE_URL = "http://127.0.0.1:8002"

# Store completed orders in memory
orders = {}
order_counter = 1

@app.get("/health")
def health():
    return {"status": "payment service is running"}

# View all orders
@app.get("/orders")
def get_orders():
    return orders

# View one order
@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]

# Checkout — the main action
@app.post("/checkout/{user_id}")
def checkout(user_id: str):
    global order_counter

    # Step 1 — fetch the user's cart
    try:
        cart_response = requests.get(f"{CART_SERVICE_URL}/cart/{user_id}")
    except Exception:
        raise HTTPException(status_code=503, detail="Cart service unreachable")

    cart = cart_response.json()

    # Step 2 — make sure cart is not empty
    if not cart["items"]:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Step 3 — reduce stock in inventory for each item
    for item in cart["items"]:
        try:
            reduce_response = requests.post(
                f"{INVENTORY_SERVICE_URL}/inventory/{item['product_id']}/reduce",
                params={"quantity": item["quantity"]}
            )
        except Exception:
            raise HTTPException(status_code=503, detail="Inventory service unreachable")

        if reduce_response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to reduce stock for {item['product_id']}"
            )

    # Step 4 — clear the cart after successful payment
    requests.delete(f"{CART_SERVICE_URL}/cart/{user_id}/clear")

    # Step 5 — record the order
    order_id = f"order-{order_counter:03d}"
    orders[order_id] = {
        "order_id": order_id,
        "user_id": user_id,
        "items": cart["items"],
        "total_items": cart["total_items"],
        "status": "paid"
    }
    order_counter += 1

    return {
        "message": "Payment successful",
        "order": orders[order_id]
    }