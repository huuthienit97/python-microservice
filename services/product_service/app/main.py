from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .database import init_db, get_db

app = FastAPI(title="Product Service")

# Khởi tạo database khi khởi động
@app.on_event("startup")
async def startup_event():
    init_db()

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

@app.post("/products/", response_model=Product)
async def create_product(product: ProductCreate, db=Depends(get_db)):
    try:
        products_collection = db.collection('products')
        product_dict = product.dict()
        current_time = datetime.utcnow()
        product_dict.update({
            "created_at": current_time,
            "updated_at": current_time
        })
        result = products_collection.insert(product_dict)
        product_dict["id"] = result["_key"]
        return Product(**product_dict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/", response_model=List[Product])
async def get_products(db=Depends(get_db)):
    try:
        products_collection = db.collection('products')
        products = []
        for doc in products_collection.all():
            doc["id"] = doc.pop("_key")
            products.append(Product(**doc))
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: str, db=Depends(get_db)):
    try:
        products_collection = db.collection('products')
        product = products_collection.get(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product["id"] = product.pop("_key")
        return Product(**product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: str, product: ProductCreate, db=Depends(get_db)):
    try:
        products_collection = db.collection('products')
        if not products_collection.get(product_id):
            raise HTTPException(status_code=404, detail="Product not found")
        product_dict = product.dict()
        product_dict["updated_at"] = datetime.utcnow()
        products_collection.update_match({"_key": product_id}, product_dict)
        updated_product = products_collection.get(product_id)
        updated_product["id"] = updated_product.pop("_key")
        return Product(**updated_product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/products/{product_id}")
async def delete_product(product_id: str, db=Depends(get_db)):
    try:
        products_collection = db.collection('products')
        if not products_collection.get(product_id):
            raise HTTPException(status_code=404, detail="Product not found")
        products_collection.delete(product_id)
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
