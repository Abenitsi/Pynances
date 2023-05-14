import os

from src.sdk.builder import ContextParser, FunctionParser
from src.shared.application.use_case import UseCase
from src.shared.class_locator import ClassLocator

if __name__ == "__main__":
    # SDK module file
    sdk_file = "./src/sdk/__init__.py"
    contexts_file = "./src/sdk/contexts.py"

    # Remove sdk module if exists
    if os.path.exists(contexts_file):
        os.remove(contexts_file)

    # Body Sections
    imports = [
        "from src.shared.dependency_container import DependencyContainer"
    ]
    context_classes = ""
    contexts_for_init = ""
    modules = ClassLocator.locate(
        path="src",
        class_name=UseCase,
        skip_modules=[".DS_Store", "__pycache__", "sdk"],
    )
    contexts: list[ContextParser] = []
    for module in modules:
        functions: list[FunctionParser] = []
        context = (
            module["module"]
            .replace("src.", "")
            .replace(".application.use_case", "")
        )
        for use_case in module["classes"]:
            functions.append(FunctionParser(context, use_case))

        context = ContextParser(context=context, functions=functions)
        imports += context.imports()
        context_classes += context.body()
        contexts_for_init += context.context_for_init()

    text_imports = "\n".join(set(imports))
    # Create module body
    module_txt = f"""{text_imports}

{context_classes}
"""

    # Write Module
    f = open(contexts_file, "w")
    f.write(module_txt)
    f.close()

    f = open(sdk_file, "r+")
    file_parts = f.read().split(
        "# ------------------- CUT HERE ------------------- #"
    )
    f.seek(0)
    f.write(
        f"""{file_parts[0]}# ------------------- CUT HERE ------------------- #
{contexts_for_init}        # ------------------- CUT HERE ------------------- #{file_parts[2]}"""
    )
    f.close()
