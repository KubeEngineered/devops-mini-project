from enum import Enum
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Inventory Microservice")


class StockStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    INSUFFICIENT_STOCK = "INSUFFICIENT_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"


class StockCheckRequest(BaseModel):
    product_id: str
    dark_store_id: str  # Fast delivery relies on local dark store stock
    requested_quantity: int = Field(gt=0, description="Quantity must be at least 1")


class StockCheckResponse(BaseModel):
    product_id: str
    dark_store_id: str
    status: StockStatus
    available_quantity: int


# Mock database representing stock per dark store location
INVENTORY_DB = {
    "DS_DELHI_01": {
        "PROD_MILK_01": 15,
        "PROD_BREAD_01": 0,
    }
}


@app.post("/api/v1/inventory/check", response_model=StockCheckResponse)
async def check_product_availability(request: StockCheckRequest):
    store_stock = INVENTORY_DB.get(request.dark_store_id)
    if store_stock is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dark store '{request.dark_store_id}' not found",
        )

    available_qty = store_stock.get(request.product_id, 0)

    if available_qty == 0:
        current_status = StockStatus.OUT_OF_STOCK
    elif available_qty < request.requested_quantity:
        current_status = StockStatus.INSUFFICIENT_STOCK
    else:
        current_status = StockStatus.AVAILABLE

    return StockCheckResponse(
        product_id=request.product_id,
        dark_store_id=request.dark_store_id,
        status=current_status,
        available_quantity=available_qty,
    )
