from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.product_schema import ProductOut
from app.models.product_model import Product

router = APIRouter(prefix="/products", tags=["Products"])

VALID_SORT_FIELDS = {"id", "name", "price", "category", "brand", "rating",
                     "created_at"}


@router.get("/", response_model=List[ProductOut])
def list_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    category: Optional[str] = None,
    sort_by: str = Query("id"),
    order: str = Query("asc"),
    db: Session = Depends(get_db),
):
    if sort_by not in VALID_SORT_FIELDS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by parameter. Valid options are: {
                ', '.join(sorted(VALID_SORT_FIELDS))}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, 
                            detail="Invalid order parameter."
                            "Must be 'asc' or 'desc'")

    skip = (page - 1) * limit

    query = db.query(Product).filter(Product.is_active.is_(True))

    if category:
        query = query.filter(Product.category == category)

    # Apply sorting
    sort_column = getattr(Product, sort_by)
    if order == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    products = query.order_by(sort_column).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductOut)
def product_detail(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
