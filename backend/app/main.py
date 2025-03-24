from fastapi import FastAPI
from app.routes import items
import uvicorn

app = FastAPI(title="FastAPI MongoDB Example")

# Register API routes
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with MongoDB"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
