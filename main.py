from fastapi import FastAPI

app = FastAPI(title="Hello World API")

@app.get("/greet")
def greet_user(name: str | None = None):
    if name:
        return {"message": f"Hello, {name}!"}
    return {"message": "Hello, World!"}