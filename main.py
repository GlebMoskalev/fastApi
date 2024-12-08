from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# Создание приложения FastAPI
app = FastAPI(title="Пример API на FastAPI", description="Это тестовый сервер с несколькими ручками.", version="1.0")

# Модель для POST-запросов
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# Ручка для проверки статуса
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Добро пожаловать на сервер FastAPI!"}


# Получение данных по ID
@app.get("/items/{item_id}", tags=["Items"])
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "query": q}


# Создание элемента
@app.post("/items/", tags=["Items"], response_model=Item)
def create_item(item: Item):
    return {"name": item.name, "description": item.description, "price": item.price, "tax": item.tax}


# Обновление элемента
@app.put("/items/{item_id}", tags=["Items"])
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "updated_data": item}


# Удаление элемента
@app.delete("/items/{item_id}", tags=["Items"])
def delete_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Item with id {item_id} has been deleted"}


# Получение списка элементов
fake_items_db = [{"id": 1, "name": "Item One"}, {"id": 2, "name": "Item Two"}, {"id": 3, "name": "Item Three"}]

@app.get("/items/", tags=["Items"])
def get_items(skip: int = 0, limit: int = 10) -> List[dict]:
    return fake_items_db[skip: skip + limit]
