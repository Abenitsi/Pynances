from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Callable, ParamSpec, TypeVar

from src.shared.application import middleware_chain
from src.shared.domain.aggregate_root import AggregateRoot

T = TypeVar("T", bound=AggregateRoot)
P = ParamSpec("P")


class MetaUseCase(ABCMeta):
    def __new__(cls, name: str, bases, attrs):  # type: ignore
        # attrs["__call__"] = cls.chain_middlewares(attrs["__call__"])
        return super().__new__(cls, name, bases, attrs)

    # @staticmethod
    def chain_middlewares(next: Callable[P, T]) -> Callable[P, T]:
        def run(*args: P.args, **kwargs: P.kwargs) -> T:
            res = next
            for middleware in reversed(middleware_chain):
                res = middleware(res)

            return res(*args, **kwargs)

        return run


class UseCase(ABC):
    @abstractmethod
    def __call__(self, *args: Any, **kwargs: Any) -> None:
        pass
