from sqlalchemy.orm import Session
from sqlalchemy.exc import InvalidRequestError
from app.models.product_model import Product


VALID_SORT_COLUMNS = {"id", "name", "price", "category", "brand", "rating",
                      "created_at"}


def get_products(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    category: str | None = None,
    sort_by: str = "id",
    order: str = "asc"
):

    if sort_by not in VALID_SORT_COLUMNS:
        sort_by = "id"
    
    if order not in ["asc", "desc"]:
        order = "asc"  
    
    query = db.query(Product).filter(Product.is_active.is_(True))

    if category:
        query = query.filter(Product.category == category)

    try:
        sort_column = getattr(Product, sort_by)
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    except (AttributeError, InvalidRequestError):
        query = query.order_by(Product.id.asc())

    return query.offset(skip).limit(limit).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()
