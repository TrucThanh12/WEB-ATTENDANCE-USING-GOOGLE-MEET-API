from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import router as MainRouter

#
# import models
# from configs.database import engine

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Địa chỉ nguồn gốc của trình duyệt
    allow_credentials=True,
    allow_methods=["*"],  # Cho phép tất cả các phương thức (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Cho phép tất cả các header
)

# models.Base.metadata.create_all(engine)

app.include_router(MainRouter)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8002)
