from fastapi import FastAPI
from app.database.database import engine, Base, get_db
from app.routers.categories import router as categories_router
from app.models.product import Product
from app.routers.products import router as products_router
from app.models.user import User
from app.routers.users import router as users_router
from app.models.order import Order
from app.routers.orders import router as orders_router
from app.models.order_item import OrderItem
from app.routers.order_items import router as order_items_router
from fastapi.responses import FileResponse

app = FastAPI()

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(order_items_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Warehouse API is running"}


@app.get("/login")
def login_page():
    return FileResponse("frontend/login.html")

@app.get("/products-page")
def products_page():
    return FileResponse("frontend/products.html")

@app.get("/categories-page")
def categories_page():
    return FileResponse("frontend/categories.html")
