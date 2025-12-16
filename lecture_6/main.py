"""FastAPI application with health check endpoint."""

from fastapi import FastAPI
import uvicorn
from api.router import router as book_router

app = FastAPI()
app.include_router(book_router)

@app.get("/healthcheck")
async def healthcheck() -> dict:
    """Health check endpoint that returns application status."""
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)
