from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
import fastapi
from datetime import datetime
from routers import router

# FastAPI Config
app = FastAPI(
    debug=True,
    docs_url=None,
    title="Kolas Swagger API",
    version="v1.0.0",
    # ,exception_handlers=exception_handlers
)

# 本地静态资源挂载
app.mount("/static", StaticFiles(directory="kolas-server/static"), name="static")
# 路由挂载
app.include_router(router, prefix="/api")
# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css"
    )

@app.get("/", tags=["index - 首页"])
async def index():
    return {
        "project_name": "Kolas",
        "project_version": "1.0.0",
        "fastapi_version" : fastapi.__version__,
        "build_time": datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    }

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        port=8020,
        app="main:app",
        reload=True
    )