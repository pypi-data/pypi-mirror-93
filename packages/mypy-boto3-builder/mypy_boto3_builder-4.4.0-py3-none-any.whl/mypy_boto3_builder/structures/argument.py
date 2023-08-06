"""
Method or function argument.
"""
from typing import Optional, Set

from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.type_constant import TypeConstant


class Argument:
    """
    Method or function argument.

    Arguments:
        name -- Argument name.
        type_annotation -- Argument type annotation.
        value -- Default argument value.
        prefix -- Used for starargs.
    """

    def __init__(
        self,
        name: str,
        type_annotation: Optional[FakeAnnotation],
        default: Optional[TypeConstant] = None,
        prefix: str = "",
    ):
        self.name = name
        self.type_annotation = type_annotation
        self.default = default
        self.prefix = prefix

    def get_types(self) -> Set[FakeAnnotation]:
        types: Set[FakeAnnotation] = set()
        if self.type_annotation is not None:
            types.update(self.type_annotation.get_types())
        if self.default is not None:
            types.update(self.default.get_types())

        return types

    @property
    def required(self) -> bool:
        return self.default is None
