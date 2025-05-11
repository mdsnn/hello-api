from fastapi import FastAPI

app = FastAPI(title="Hello World API")

@app.get("/greet")
def greet_user():
    return {"message": "Hello, World!"}