from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from src.main.streamController.config import tags_metadata, Settings
from src.main.streamController.api.n8n.router import router_app as n8n_router_app
from src.main.streamController.api.trigger.router import router_app as trigger_router_app
from src.main.streamController.api.loader.task.router import router_app as task_router_app
from src.main.streamController.api.loader.monitor.router import router_app as monitor_router_app
from src.main.streamController.api.loader.connection.router import router_app as connection_router_app


app = FastAPI(
    docs_url="/stream/controller/docs", redoc_url="/stream/controller/re_doc", openapi_tags=tags_metadata, title="纭"
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Stream Controller Docs",
        version=Settings.version,
        description="纭",
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(trigger_router_app)
app.include_router(n8n_router_app)
app.include_router(task_router_app)
app.include_router(monitor_router_app)
app.include_router(connection_router_app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/settings", name="获取配置信息", description="获取配置信息", tags=["settings"])
def get_settings():
    return Settings.to_dict()


if __name__ == '__main__':
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - ' \
                                                    '"%(request_line)s" %(status_code)s'
    uvicorn.run(app, host="0.0.0.0", port=18000)
