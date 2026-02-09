# flake8: noqa: E402

import json
import sys
import os
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv

backend_root = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

load_dotenv(os.path.join(backend_root, '.env'))

sys.path.insert(0, backend_root)

from app.core.database import SessionLocal
from app.models.product_model import Product


def seed_products(clear_existing=True):
    db: Session = SessionLocal()
    try:
        if clear_existing:
            try:
                db.query(Product).delete()
                db.commit()
                print("Cleared existing products")
            except ProgrammingError:
                print("Table 'products' does not exist. Skipping deletion.")

        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "products.json")

        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)

        for product in products:
            if "created_at" in product and isinstance(product["created_at"], str):
                dt = datetime.fromisoformat(product["created_at"].replace(
                    "Z", "+00:00"))
                product["created_at"] = dt.replace(tzinfo=None)

            db.add(Product(**product))

        db.commit()
        print(f"Seeded {len(products)} products successfully")

    except Exception as e:
        db.rollback()
        print(f"Error seeding products: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_products(clear_existing=True)
