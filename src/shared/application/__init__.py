from src.shared.application.middleware import (
    db_middleware,
    log_middleware,
    publish_events,
)

middleware_chain = [
    db_middleware,
    log_middleware,
    publish_events,
]
