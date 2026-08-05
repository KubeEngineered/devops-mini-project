# Source code for product catalogue

pip install fastapi uvicorn pydantic

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Quick-Commerce Product Catalog Microservice")

# --- Data Models ---
class Product(BaseModel):
    id: str
    name: str
    category: str
    price_inr: float
    unit: str  # e.g., "500g", "1L", "1 pack"
    in_stock: bool
    stock_count: int
    image_url: str

# --- In-Memory Product Database (Simulating fast-delivery items) ---
PRODUCT_DB: List[Product] = [
    Product(
        id="prod_101",
        name="Amul Taaza Toned Milk",
        category="Dairy & Bread",
        price_inr=27.0,
        unit="500 ml",
        in_stock=True,
        stock_count=45,
        image_url="https://cdn.example.com/images/amul_taaza.jpg"
    ),
    Product(
        id="prod_102",
        name="Fresh Banana - Robusta",
        category="Fruits & Vegetables",
        price_inr=40.0,
        unit="1 kg",
        in_stock=True,
        stock_count=20,
        image_url="https://cdn.example.com/images/banana.jpg"
    ),
    Product(
        id="prod_103",
        name="Lay's India's Magic Masala Chips",
        category="Snacks & Munchies",
        price_inr=20.0,
        unit="50 g",
        in_stock=False,
        stock_count=0,
        image_url="https://cdn.example.com/images/lays_blue.jpg"
    ),
    Product(
        id="prod_104",
        name="Amul Salted Butter",
        category="Dairy & Bread",
        price_inr=58.0,
        unit="100 g",
        in_stock=True,
        stock_count=12,
        image_url="https://cdn.example.com/images/amul_butter.jpg"
    )
]

# --- Endpoints ---

@app.get("/api/v1/catalog/products", response_model=List[Product])
def get_products(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by product name"),
    only_in_stock: bool = Query(False, description="Filter available items only")
):
    """Fetch product catalog with optional search, category filter, and stock check."""
    results = PRODUCT_DB

    if category:
        results = [p for p in results if p.category.lower() == category.lower()]

    if search:
        results = [p for p in results if search.lower() in p.name.lower()]

    if only_in_stock:
        results = [p for p in results if p.in_stock]

    return results


@app.get("/api/v1/catalog/products/{product_id}", response_model=Product)
def get_product_details(product_id: str):
    """Get single product details by ID."""
    for product in PRODUCT_DB:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/api/v1/catalog/categories")
def get_categories():
    """Get distinct list of available categories for the app home screen."""
    categories = list(set(product.category for product in PRODUCT_DB))
    return {"categories": sorted(categories)}
