from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

app = FastAPI()

# Defined SQLAlchemy models
Base = declarative_base()

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(1024))

# Create a database connection
DATABASE_URL = "mysql://root:root@localhost/python"
engine = create_engine(DATABASE_URL)


# Create tables in the database
Base.metadata.create_all(bind=engine)


# Pydantic model for API input
class ItemCreate(BaseModel):
    name: str
    description: str


class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

# CRUD operations

#POST
@app.post("/items/", response_model=ItemResponse)
def create_item(item: ItemCreate):
    with Session(engine) as session:
        db_item = Item(**item.dict())
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item

#GET BY ID
@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    with Session(engine) as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item


#GET-ALL
@app.get("/items/", response_model=list[ItemResponse])
def read_items(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        items = session.query(Item).offset(skip).limit(limit).all()
        return items

#PUT
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item_update: ItemCreate):
    with Session(engine) as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        for key, value in item_update.dict().items():
            setattr(item, key, value)
        session.commit()
        session.refresh(item)
        return item

#DELETE
@app.delete("/items/{item_id}", response_model=ItemResponse)
def delete_item(item_id: int):
    with Session(engine) as session:
        item = session.query(Item).filter(Item.id == item_id).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        session.delete(item)
        session.commit()
        return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
