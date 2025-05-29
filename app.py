import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from router.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # For future startup/cleanup logic if needed

app = FastAPI(lifespan=lifespan)
app.include_router(router)

@app.get("/health_check", tags=["Health Check"])
async def ping():
    return JSONResponse(content={"status": "ok"}, media_type="application/json")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)