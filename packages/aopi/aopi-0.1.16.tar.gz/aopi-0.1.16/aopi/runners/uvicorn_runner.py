import uvicorn

from aopi.settings import settings


def run_app() -> None:
    settings.pprint()
    uvicorn.run(
        app="aopi.application:get_application",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        workers=settings.workers_count,
        log_config=None,
    )
