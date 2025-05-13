from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import List
from contextlib import asynccontextmanager

# FastAPI app
app = FastAPI(title="SQLModel Todo List API")

# SQLModel model for Todo (database and Pydantic)
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    completed: bool = False

# Pydantic model for request body
class TodoCreate(SQLModel):
    title: str
    description: str | None = None
    completed: bool = False

# Database setup
sqlite_url = "sqlite:///todo.db"
engine = create_engine(sqlite_url, echo=True)

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app.lifespan = lifespan

# Dependency to get database session
def get_session():
    with Session(engine) as session:
        yield session

@app.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate, session: Session = get_session()):
    db_todo = Todo.from_orm(todo)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@app.get("/todos", response_model=List[Todo])
async def get_todos(session: Session = get_session()):
    todos = session.exec(select(Todo)).all()
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, session: Session = get_session()):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo: TodoCreate, session: Session = get_session()):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    for key, value in todo.dict(exclude_unset=True).items():
        setattr(db_todo, key, value)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, session: Session = get_session()):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"message": "Todo deleted"}