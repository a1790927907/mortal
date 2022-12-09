from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from src.main.streamStorage.config import tags_metadata, Settings
from src.main.streamStorage.api.task.router import router_app as task_router
from src.main.streamStorage.api.schema.router import router_app as schema_router
from src.main.streamStorage.api.connection.router import router_app as connection_router
from src.main.streamStorage.database.executor.application import application as database_app


app = FastAPI(docs_url="/stream/store/docs", redoc_url="/stream/store/re_doc", openapi_tags=tags_metadata, title="月")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Stream Storage Docs",
        version=Settings.version,
        description="月",
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(task_router)
app.include_router(connection_router)
app.include_router(schema_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database_app.settings.db_instance.connect()
    database_app.init_tables()


@app.get("/settings", name="获取配置信息", description="获取配置信息", tags=["settings"])
def get_settings():
    return Settings.to_dict()


if __name__ == '__main__':
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - ' \
                                                    '"%(request_line)s" %(status_code)s'
    uvicorn.run(app, host="0.0.0.0", port=9400)
