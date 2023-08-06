"""
Boto3 client Waiter.
"""
from botocore.waiter import Waiter as Boto3Waiter

from mypy_boto3_builder.enums.service_module_name import ServiceModuleName
from mypy_boto3_builder.import_helpers.import_string import ImportString
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.structures.argument import Argument
from mypy_boto3_builder.structures.class_record import ClassRecord
from mypy_boto3_builder.structures.method import Method
from mypy_boto3_builder.type_annotations.external_import import ExternalImport
from mypy_boto3_builder.type_annotations.type import Type
from mypy_boto3_builder.type_annotations.type_class import TypeClass
from mypy_boto3_builder.type_annotations.type_literal import TypeLiteral


class Waiter(ClassRecord):
    """
    Boto3 client Waiter.
    """

    def __init__(
        self,
        name: str,
        waiter_name: str,
        service_name: ServiceName,
        docstring: str = "",
    ):
        super().__init__(
            name=name,
            docstring=docstring,
            bases=[TypeClass(Boto3Waiter, alias="Boto3Waiter")],
        )
        self.waiter_name = waiter_name
        self.service_name = service_name

    def get_client_method(self) -> Method:
        return Method(
            name="get_waiter",
            decorators=[Type.overload],
            docstring=self.docstring,
            arguments=[
                Argument("self", None),
                Argument("waiter_name", TypeLiteral(self.waiter_name)),
            ],
            return_type=ExternalImport(
                source=ImportString(self.service_name.module_name, ServiceModuleName.waiter.value),
                name=self.name,
            ),
        )
