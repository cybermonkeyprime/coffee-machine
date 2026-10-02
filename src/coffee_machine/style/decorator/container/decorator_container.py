# src/ota_installer/containers/decorators.py
from dependency_injector import containers, providers


class Decorators(containers.DeclarativeContainer):
    from ...decorator.colorizer import Colorizer
    from ...decorator.indent_wrapper import IndentWrapper
    from ...decorator.output_printer import OutputPrinter
    from ...decorator.styled_indent_printer import StylizedIndentPrinter

    colorizer = providers.Factory(Colorizer)
    indent_wrapper = providers.Factory(IndentWrapper)
    output_printer = providers.Factory(OutputPrinter)

    stylized_indent_printer = providers.Factory(
        StylizedIndentPrinter,
        colorizer=colorizer,
        indent_wrapper=indent_wrapper,
        output_printer=output_printer,
    )


# Signed off by Brian Sanford on 20260625
