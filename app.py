import uvicorn
from fastapi import FastAPI

from routes.route import router
from utilities.Executor import Executor

app = FastAPI()

app.include_router(
    router,
    prefix="/api",
)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)

