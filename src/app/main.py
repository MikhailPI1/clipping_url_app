from fastapi import FastAPI
import uvicorn

from db.db_con import init_db
from routers.url import router

app = FastAPI(title="URLShortener")

app.include_router(router)

if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="0.0.0.0", port=8000)