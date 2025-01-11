from fastapi import FastAPI

from app.core.config import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/settings")
def read_settings():
    return settings


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
