import sys
from pathlib import Path

# 将项目根目录添加到 Python 路径中
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import auth_router
from app.api.attendance import router as attendance_router
from app.api.student import router as student_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(attendance_router)
app.include_router(student_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "FastAPI 运行中"}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 1 --reload
