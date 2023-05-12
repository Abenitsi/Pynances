from src.shared.application.middleware import log_middleware

middleware_chain = [
    # db_middleware,
    log_middleware,
    # publish_events,
]
