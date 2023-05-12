# Imports
import inspect
import os
import re
import sys
from importlib import import_module
from typing import Type

from src.shared.application.use_case import UseCase


class Import:
    __value: str

    def __init__(
        self, module: str, cls: str, alias: str | None = None
    ) -> None:
        self.__value = f"from {module} import {cls}"
        if alias is not None:
            self.__value += f" as {alias}"

    def __str__(self) -> str:
        return self.__value


class FunctionParser:
    def __init__(self, context: str, use_case: Type[UseCase]) -> None:
        print(context, use_case)
        self.__function_name: str = ""
        self.__args: list[dict[str, str]] = []
        self.__return_type: str = ""
        self.__use_case_name: str = ""
        self.__imports: list[Import] = []
        self.__use_case_alias: str = (
            f"{use_case.__name__}{context.capitalize()}"
        )

        self.set_function_name(use_case)
        self.__use_case_name = use_case.__name__
        self.__imports.append(
            Import(
                module=use_case.__module__,
                cls=self.__use_case_name,
                alias=self.__use_case_alias,
            )
        )

        sig = inspect.signature(getattr(use_case, "__call__"))
        self.set_args(sig)
        self.set_return_type(sig)

    def set_function_name(self, use_case: Type[UseCase]) -> None:
        self.__function_name = re.sub(
            r"(?<!^)(?=[A-Z])", "_", use_case.__name__.replace("UseCase", "")
        ).lower()

    def set_args(self, sig: inspect.Signature) -> None:
        for p in sig.parameters.values():
            if "core." in p.annotation.__module__:
                self.__imports.append(
                    Import(
                        module=p.annotation.__module__,
                        cls=p.annotation.__name__,
                    )
                )
        self.__args = [
            {"name": p.name, "annotation": p.annotation.__name__}
            for p in sig.parameters.values()
            if (
                p.name != "self"
                and p != inspect.Parameter.empty
                and p.annotation != inspect.Parameter.empty
            )
        ]

    def set_return_type(self, sig: inspect.Signature) -> None:
        return_type = "None"
        print(sig.return_annotation)
        if sig.return_annotation is not None:
            module = sig.return_annotation.__module__
            return_type = sig.return_annotation
            if return_type == inspect.Parameter.empty:  # type: ignore
                return_type = "None"
            elif module not in ["inspect", "builtins"]:
                return_type = sig.return_annotation.__name__
                self.__imports.append(Import(module=module, cls=return_type))

        self.__return_type = return_type

    def imports(self) -> list[str]:
        f_imports = [str(i) for i in self.__imports]
        return f_imports

    def body(self) -> str:
        params = []
        args = []
        for arg in self.__args:
            params.append(f"{arg['name']}: {arg['annotation']}")
            args.append(f"{arg['name']}={arg['name']}")

        return_clause = "return " if self.__return_type != "None" else ""
        return f"""
    def {self.__function_name}({', '.join(["self"] + params)}) -> {self.__return_type}:
        {return_clause}self.__container.get({self.__use_case_alias})({', '.join(args)})
"""


class ContextParser:
    def __init__(self, context: str, functions: list[FunctionParser]) -> None:
        self.__functions: list[FunctionParser] = functions
        self.__context_name = context
        self.__class_name = f"{self.__context_name.capitalize()}SDKContext"

    def imports(self) -> list[str]:
        f_imports = []
        for f in self.__functions:
            f_imports += f.imports()
        return f_imports

    def context_for_init(self) -> str:
        return f"        self.{self.__context_name} = self.container.get({self.__class_name})\n"

    def body(self) -> str:
        functions = [f.body() for f in self.__functions]
        return f"""
class {self.__class_name}:
    __container: DependencyContainer

    def __init__(self, container: DependencyContainer) -> None:
        self.__container = container
    {''.join(functions)}
"""


def find_contexts(root: str = "src") -> list[ContextParser]:
    contexts = os.listdir(f"./{root}")
    ignore_items = [
        "__init__.py",
        "__pycache__",
        "shared",
        "retrieve_repository.py",
        "write_repository.py",
        "ids.py",
        "movements.py",
    ]
    contexts_lists: list[ContextParser] = []
    for context in contexts:
        if context in ignore_items:
            continue

        module_name = f"{root}.{context}.application.use_case"
        print(module_name)
        import_module(module_name)
        cls_members = inspect.getmembers(
            sys.modules[module_name], inspect.isclass
        )
        functions: list[FunctionParser] = []
        for element in cls_members:
            use_case = element[1]
            if not (issubclass(use_case, UseCase) and use_case != UseCase):
                continue

            functions.append(FunctionParser(context, use_case))

        contexts_lists.append(
            ContextParser(context=context, functions=functions)
        )
    return contexts_lists


if __name__ == "__main__":
    # SDK module file
    file = "./src/sdk.py"

    # Remove sdk module if exists
    if os.path.exists(file):
        os.remove(file)

    # Body Sections
    imports = [
        "from src.shared.dependency_container import DependencyContainer",
        # "from core.shared.domain.connection import ConnectionConfig",
        # "from core.shared.infrastructure.connection import PostgreSQLAlchemyConnectionConfig",
        # "from core.users.application.unit_of_work import SQLAlchemyUserUoW, UserUoW",
        "from src import CoreConfig",
    ]
    context_classes = ""
    contexts_for_init = ""

    contexts = find_contexts()
    for context in contexts:
        imports += context.imports()
        context_classes += context.body()
        contexts_for_init += context.context_for_init()

    text_imports = "\n".join(set(imports))
    # Create module body
    module_txt = f"""{text_imports}

{context_classes}
class SDK:
    container = DependencyContainer.get_container()

    def __init__(self, config: CoreConfig) -> None:
        self.config = config
        self.__bootstrap()
{contexts_for_init}
    def __bootstrap(self) -> None:
        for key, value in self.config.bindings.items():
            self.container.set(key, value(self))
"""

    # Write Module
    f = open(file, "w")
    f.write(module_txt)
    f.close()
