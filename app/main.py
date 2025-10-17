"""
应用入口模块 - WhisprRT 实时语音转文字服务
"""
from typing import Dict, Any
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.logging import logger
from app.config import HOST, PORT

# 创建FastAPI应用
app = FastAPI(
    title="WhisprRT - Real-time Speech Transcription",
    description="基于 Whisper 的本地实时语音转文字工具",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# 添加CORS中间件以支持跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 设置模板
templates = Jinja2Templates(directory="templates")

# 注册API路由
app.include_router(api_router)

@app.on_event("startup")
async def startup_event() -> None:
    """应用启动时的事件处理"""
    logger.info("WhisprRT application starting up...")
    logger.info(f"Server will be available at http://{HOST}:{PORT}")

@app.on_event("shutdown")
async def shutdown_event() -> None:
    """应用关闭时的事件处理"""
    logger.info("WhisprRT application shutting down...")

@app.get('/', response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """
    渲染主页

    Args:
        request: FastAPI 请求对象

    Returns:
        HTMLResponse: 渲染后的 HTML 页面
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/health')
async def health_check() -> Dict[str, Any]:
    """
    健康检查端点

    Returns:
        Dict: 健康状态信息
    """
    return {
        "status": "healthy",
        "service": "WhisprRT",
        "version": "2.0.0"
    }

if __name__ == '__main__':
    try:
        logger.info("Starting WhisprRT server...")
        uvicorn.run(
            app,
            host=HOST,
            port=PORT,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise