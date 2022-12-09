from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from src.main.monitor.config import tags_metadata, Settings
from src.main.monitor.api.tasksRun.router import router_app as tasks_run_router_app
from src.main.monitor.database.executor.application import application as database_app
from src.main.monitor.api.taskStatus.router import router_app as task_status_router_app
from src.main.monitor.api.taskOutput.router import router_app as task_output_router_app
from src.main.monitor.api.tasksRunning.router import router_app as tasks_running_router_app
from src.main.monitor.api.tasksRunInput.router import router_app as tasks_run_input_router_app


app = FastAPI(
    docs_url="/stream/monitor/docs", redoc_url="/stream/monitor/re_doc", openapi_tags=tags_metadata, title="蘩"
)
Settings.create_all()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Stream Monitor Docs",
        version=Settings.version,
        description="蘩",
        routes=app.routes,
        tags=tags_metadata
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.openapi = custom_openapi
app.include_router(task_status_router_app)
app.include_router(tasks_run_router_app)
app.include_router(task_output_router_app)
app.include_router(tasks_run_input_router_app)
app.include_router(tasks_running_router_app)


@app.on_event("startup")
async def start_up():
    await database_app.init_connection()


@app.get("/settings", name="获取配置信息", description="获取配置信息", tags=["settings"])
def get_settings():
    return Settings.to_dict()


if __name__ == '__main__':
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - ' \
                                                    '"%(request_line)s" %(status_code)s'
    uvicorn.run(app, host="0.0.0.0", port=13000)
