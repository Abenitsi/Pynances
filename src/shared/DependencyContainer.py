import inspect
from typing import Dict, Self, Type, TypeVar

T = TypeVar("T")


class DependencyContainer:
    __container: Self | None = None

    def __init__(self) -> None:
        self.__instances: Dict[Type[T], T] = {}  # type: ignore

    @classmethod
    def get_container(cls) -> "DependencyContainer":
        if cls.__container is None:
            cls.__container = DependencyContainer()
        return cls.__container

    def get(self, cls: Type[T]) -> T:
        if cls in self.__instances:
            return self.__instances[cls]

        # Inspeccionar la firma del constructor para recuperar los nombres de los argumentos
        sig = inspect.signature(cls.__init__)
        args = [
            {"name": p.name, "annotation": p.annotation}
            for p in sig.parameters.values()
            if p.name != "self"
        ]

        # Crear un diccionario de argumentos a partir de los nombres de los argumentos y sus valores
        args_dict = {}
        for arg in args:
            if arg["annotation"] is inspect._empty:
                continue
            args_dict[arg["name"]] = self.get(arg["annotation"])

        # Crear una instancia de la clase con las dependencias inyectadas
        instance = cls(**args_dict)
        self.__instances[cls] = instance

        return instance

    def set(self, cls: Type[T], instance: T) -> None:
        self.__instances[cls] = instance
