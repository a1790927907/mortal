from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from src.main.streamParser.config import tags_metadata, Settings
from src.main.streamParser.api.n8n.router import router_app as n8n_parser_router_app


app = FastAPI(
    docs_url="/stream/parser/docs", redoc_url="/stream/parser/re_doc", openapi_tags=tags_metadata, title="氲"
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Stream Parser Docs",
        version=Settings.version,
        description="氲",
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(n8n_parser_router_app)


@app.get("/settings", name="获取配置信息", description="获取配置信息", tags=["settings"])
def get_settings():
    return Settings.to_dict()


if __name__ == '__main__':
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - ' \
                                                    '"%(request_line)s" %(status_code)s'
    uvicorn.run(app, host="0.0.0.0", port=16500)
