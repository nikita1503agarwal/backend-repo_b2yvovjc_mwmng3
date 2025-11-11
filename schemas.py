"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    address: Optional[str] = Field(None, description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    image: Optional[str] = Field(None, description="Image URL")
    in_stock: bool = Field(True, description="Whether product is in stock")

class Service(BaseModel):
    """
    Services collection schema
    Collection name: "service"
    """
    name: str = Field(..., description="Service name")
    description: Optional[str] = Field(None, description="Service details")
    base_price: float = Field(..., ge=0, description="Starting price")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags for filtering")

class OrderItem(BaseModel):
    product_id: str = Field(..., description="ID of the product")
    title: str = Field(..., description="Product title at time of order")
    quantity: int = Field(1, ge=1)
    price: float = Field(..., ge=0, description="Unit price at time of order")
    subtotal: float = Field(..., ge=0)

class Order(BaseModel):
    """
    Orders collection schema
    Collection name: "order"
    """
    customer_name: str
    customer_email: EmailStr
    customer_phone: Optional[str] = None
    items: List[OrderItem]
    total: float = Field(..., ge=0)
    status: str = Field("pending", description="Order status")
    notes: Optional[str] = None

class DesignRequest(BaseModel):
    """
    Design requests for custom services
    Collection name: "designrequest"
    """
    name: str
    email: EmailStr
    phone: Optional[str] = None
    service: str = Field(..., description="Selected service name")
    brief: str = Field(..., description="Project brief / requirements")
    budget: Optional[float] = Field(None, ge=0)
    status: str = Field("new", description="Request status")

# Add your own schemas here:
# --------------------------------------------------

# Note: The Flames database viewer will automatically:
# 1. Read these schemas from GET /schema endpoint
# 2. Use them for document validation when creating/editing
# 3. Handle all database operations (CRUD) directly
# 4. You don't need to create any database endpoints!
