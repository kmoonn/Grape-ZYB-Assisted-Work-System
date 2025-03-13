import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import auth_router
from app.api.attendance import router as attendance_router
from app.api.student import router as student_router

app = FastAPI()

# 允许的前端地址（改为你实际的前端 URL）
origins = [
    "http://localhost:3000",  # 本地开发环境
    "http://47.94.107.234:3000",  # 服务器上的前端
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 不能用 "*"，要写具体地址
    allow_credentials=True,  # 允许携带 Cookie / 认证信息
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)

app.include_router(attendance_router)
app.include_router(student_router)
app.include_router(auth_router)


@app.get("/")
def read_root():
    return {"message": "FastAPI 运行中"}
