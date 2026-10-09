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
from app.models.stock_movement import StockMovement
from app.routers.stock_movements import router as stock_movements_router
from app.routers.dashboard import router as dashboard_router
from fastapi.staticfiles import StaticFiles
from app.routers.reports import router as reports_router


app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(order_items_router)
app.include_router(stock_movements_router)
app.include_router(dashboard_router)
app.include_router(reports_router)

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

@app.get("/orders-page")
def orders_page():
    return FileResponse("frontend/orders.html")

@app.get("/stock-movements-page")
def stock_movements_page():
    return FileResponse("frontend/stock-movements.html")

@app.get("/users-page")
def users_page():
    return FileResponse("frontend/users.html")

@app.get("/dashboard-page")
def dashboard_page():
    return FileResponse("frontend/dashboard.html")

@app.get("/reports-page")
def reports_page():
    return FileResponse("frontend/reports.html")
