# Imports
import inspect
import re
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
            if "src." in p.annotation.__module__:
                self.__imports.append(
                    Import(
                        module=p.annotation.__module__,
                        cls=p.annotation.__name__,
                    )
                )
            if (
                p.name != "self"
                and p != inspect.Parameter.empty
                and p.annotation != inspect.Parameter.empty
            ):
                self.__args.append(
                    {
                        "name": p.name,
                        "annotation": p.annotation.__name__,
                        "cls": p.annotation,
                    }
                )

    def set_return_type(self, sig: inspect.Signature) -> None:
        return_type = "None"
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
        transform_data = ""
        for arg in self.__args:
            if arg["annotation"] == self.__use_case_name + "Data":
                transform_data = f"""        {arg['name']} = {self.__use_case_name+"Data"}("""
                sig = inspect.signature(arg["cls"])  # type: ignore
                for p in sig.parameters.values():
                    if (
                        p.name != "self"
                        and p != inspect.Parameter.empty
                        and p.annotation != inspect.Parameter.empty
                    ):
                        params.append(f"{p.name}: {p.annotation.__name__}")
                        transform_data += f"""
            {p.name}={p.name},"""
                transform_data += f"""
        )"""
                args.append(f"{arg['name']}={arg['name']}")
            else:
                params.append(f"{arg['name']}: {arg['annotation']}")
                args.append(f"{arg['name']}={arg['name']}")

        return_clause = "return " if self.__return_type != "None" else ""
        return f"""
    def {self.__function_name}({', '.join(["self"] + params)}) -> {self.__return_type}:
{transform_data}
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
        return f"        self.{self.__context_name} = self.__container.get(contexts.{self.__class_name})\n"

    def body(self) -> str:
        functions = [f.body() for f in self.__functions]
        return f"""
class {self.__class_name}:
    __container: DependencyContainer

    def __init__(self, container: DependencyContainer) -> None:
        self.__container = container
    {''.join(functions)}
"""
