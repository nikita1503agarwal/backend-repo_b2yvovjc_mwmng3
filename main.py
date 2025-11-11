import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Product, Service, Order, DesignRequest

app = FastAPI(title="Design & Commerce API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Design & Commerce API running"}

# Utility to convert Mongo _id to string

def serialize_doc(doc):
    if not doc:
        return doc
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return doc

# Seed demo products/services if empty
@app.on_event("startup")
async def seed_data():
    try:
        if db is None:
            return
        if db["product"].count_documents({}) == 0:
            demo_products = [
                {"title": "Kartu Nama Premium", "description": "Kartu nama dengan finishing doff dan emboss.", "price": 150000, "category": "print", "image": "https://images.unsplash.com/photo-1517849845537-4d257902454a"},
                {"title": "Poster A3 Glossy", "description": "Poster kualitas tinggi untuk promosi.", "price": 75000, "category": "print", "image": "https://images.unsplash.com/photo-1497032628192-86f99bcd76bc"},
                {"title": "Stiker Die-cut", "description": "Stiker custom tahan air.", "price": 50000, "category": "print", "image": "https://images.unsplash.com/photo-1520975916090-3105956dac38"},
            ]
            for p in demo_products:
                db["product"].insert_one({**p})
        if db["service"].count_documents({}) == 0:
            demo_services = [
                {"name": "Desain Logo", "description": "Paket pembuatan logo profesional (3 konsep)", "base_price": 1200000, "tags": ["brand", "logo"]},
                {"name": "Desain Instagram Feed", "description": "Template feed 9 post + panduan brand", "base_price": 900000, "tags": ["social", "template"]},
                {"name": "Company Profile", "description": "Desain company profile 8-12 halaman", "base_price": 2500000, "tags": ["print", "profile"]},
            ]
            for s in demo_services:
                db["service"].insert_one({**s})
    except Exception:
        # On environments without DB, just skip seeding
        pass

# Public catalog endpoints
@app.get("/api/products")
def list_products():
    items = get_documents("product") if db else []
    return [serialize_doc(i) for i in items]

@app.get("/api/services")
def list_services():
    items = get_documents("service") if db else []
    return [serialize_doc(i) for i in items]

# Orders
@app.post("/api/orders")
def create_order(order: Order):
    try:
        inserted_id = create_document("order", order)
        return {"id": inserted_id, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Design requests
@app.post("/api/design-requests")
def create_design_request(req: DesignRequest):
    try:
        inserted_id = create_document("designrequest", req)
        return {"id": inserted_id, "status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
