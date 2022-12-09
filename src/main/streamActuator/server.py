from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from src.main.streamActuator.config import tags_metadata, Settings
from src.main.streamActuator.api.trigger.router import router_app as trigger_router_app
from src.main.streamActuator.recorder.worker.application import application as recorder_worker_app


app = FastAPI(
    docs_url="/stream/actuator/docs", redoc_url="/stream/actuator/re_doc", openapi_tags=tags_metadata, title="氤"
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Stream Actuator Docs",
        version=Settings.version,
        description="氤",
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
app.include_router(trigger_router_app)


@app.on_event("startup")
async def start_up():
    await recorder_worker_app.init_queue_consumer()


@app.get("/settings", name="获取配置信息", description="获取配置信息", tags=["settings"])
def get_settings():
    return Settings.to_dict()


if __name__ == '__main__':
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - ' \
                                                    '"%(request_line)s" %(status_code)s'
    uvicorn.run(app, host="0.0.0.0", port=16000)
