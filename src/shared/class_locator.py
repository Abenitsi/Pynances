import inspect
import os
import sys
from importlib import import_module
from typing import TypeVar, Type

T = TypeVar("T")


class ClassLocator:
    @classmethod
    def _get_module_class(
        cls, module_name: str, class_name: Type[T]
    ) -> list[Type[T]]:
        classes: list[Type[T]] = []
        if module_name not in sys.modules:
            import_module(module_name)
        cls_members = inspect.getmembers(
            sys.modules[module_name], inspect.isclass
        )
        for element in cls_members:
            use_case = element[1]
            if not (
                issubclass(use_case, class_name) and use_case != class_name
            ):
                continue

            classes.append(use_case)
        return classes

    @classmethod
    def locate(
        cls,
        path: str,
        class_name: Type[T],
        skip_modules: list[str] = ["__pycache__", "sdk"],
    ) -> list[Type[T] | dict[str, list[Type[T]]]]:
        classes: list[Type[T] | dict[str, list[Type[T]]]] = []
        modules = filter(
            lambda file: file not in skip_modules, os.listdir(f"./{path}")
        )
        for module in modules:
            if ".py" in module:
                module_name = (
                    f"{path.replace('/', '.')}.{module.replace('.py', '')}"
                )
                elements = cls._get_module_class(module_name, class_name)
                if len(elements) > 0:
                    classes.append({"module": module_name, "classes": elements})  # type: ignore
            else:
                classes += cls.locate(
                    "/".join([path, module]), class_name, skip_modules
                )

        return classes
