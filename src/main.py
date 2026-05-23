from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routes import router

app = FastAPI(
    title="PADCS API",
    description=(
        "API tối ưu hóa lộ trình du lịch cá nhân hóa dựa trên phương pháp Tìm kiếm hủy-dựng thích nghi cá nhân hóa (PADCS), "
        "giải bài toán Team Orienteering Problem with Time Windows (TOPTW). "
        "Hệ thống tối ưu lộ trình theo sở thích, ngân sách và ràng buộc thời gian của người dùng."
    ),
    version="1.0.0",
    contact={
        "name": "Hoàng Minh Đức",
    },
    license_info={
        "name": "MIT License",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api", tags=["Optimization"])


@app.get(
    "/",
    summary="Health Check",
    description="Kiểm tra trạng thái hoạt động của server.",
    tags=["System"],
)
def root():
    return {"status": "ok", "message": "Server is running..."}