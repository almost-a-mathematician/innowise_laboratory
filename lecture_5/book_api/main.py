from fastapi import FastAPI
import uvicorn
from api.router import router as book_router


app = FastAPI()
app.include_router(book_router)

if __name__ == '__main__':
	uvicorn.run('main:app', reload=True)
