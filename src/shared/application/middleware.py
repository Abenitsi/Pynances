from typing import Callable, ParamSpec, TypeVar

from src import container, connection
from src.shared.domain.aggregate_root import AggregateRoot
from src.shared.domain.domain_event import DomainEventRepository

T = TypeVar("T", bound=AggregateRoot)
P = ParamSpec("P")


def publish_events(func: Callable[P, T]) -> Callable[P, T]:
    def run(*args: P.args, **kwargs: P.kwargs) -> T:
        res = func(*args, **kwargs)
        repository = container.get(DomainEventRepository)
        repository.store(*res.pull_events())
        return res

    return run


def db_middleware(func: Callable[P, T]) -> Callable[P, T]:
    def run(*args: P.args, **kwargs: P.kwargs) -> T:
        print("starting db transaction")
        with connection.begin_transaction():
            res = func(*args, **kwargs)
        # connection.commit()
        print("commiting db transaction")
        return res

    return run


def log_middleware(func: Callable[P, T]) -> Callable[P, T]:
    def run(*args: P.args, **kwargs: P.kwargs) -> T:
        print("starting log serive")
        res = func(*args, **kwargs)
        print("closing log service")
        return res

    return run


def extra_middleware(func: Callable[P, T]) -> Callable[P, T]:
    def run(*args: P.args, **kwargs: P.kwargs) -> T:
        print("starting extra")
        res = func(*args, **kwargs)
        print("closing extra")
        return res

    return run
