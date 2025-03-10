from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import auth_router
from api.attendance import router as attendance_router
from api.student import router as student_router

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

    uvicorn.run(app, host='0.0.0.0', port=8000)
