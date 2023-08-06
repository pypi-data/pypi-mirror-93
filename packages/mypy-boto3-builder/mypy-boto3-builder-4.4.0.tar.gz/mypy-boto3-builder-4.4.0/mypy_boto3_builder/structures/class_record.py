"""
Base class for all structures that can be rendered to a class.
"""
from typing import Iterable, List, Set

from botocore import xform_name

from mypy_boto3_builder.import_helpers.import_record import ImportRecord
from mypy_boto3_builder.structures.attribute import Attribute
from mypy_boto3_builder.structures.method import Method
from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.internal_import import InternalImport


class ClassRecord:
    """
    Base class for all structures that can be rendered to a class.
    """

    _alias_name: str = ""

    def __init__(
        self,
        name: str,
        methods: Iterable[Method] = tuple(),
        attributes: Iterable[Attribute] = tuple(),
        bases: Iterable[FakeAnnotation] = tuple(),
        docstring: str = "",
        use_alias: bool = False,
    ):
        self.name = name
        self.methods = list(methods)
        self.attributes = list(attributes)
        self.bases = list(bases)
        self.docstring = docstring
        self.use_alias = use_alias

    @property
    def alias_name(self) -> str:
        if self._alias_name:
            return self._alias_name
        if not self.use_alias:
            raise ValueError(f"Cannot get alias for { self.name } with no alias.")
        return InternalImport.get_alias(self.name)

    def render_alias(self) -> str:
        return f"{self.alias_name} = {self.name}"

    def get_types(self) -> Set[FakeAnnotation]:
        types: Set[FakeAnnotation] = set()
        for method in self.methods:
            types.update(method.get_types())
        for attribute in self.attributes:
            types.update(attribute.get_types())
        for base in self.bases:
            types.update(base.get_types())
        return types

    def get_required_import_records(self) -> Set[ImportRecord]:
        result: Set[ImportRecord] = set()
        for type_annotation in self.get_types():
            import_record = type_annotation.get_import_record()
            if not import_record or import_record.is_builtins():
                continue
            result.add(import_record)

        return result

    def get_internal_imports(self) -> List[InternalImport]:
        result: List[InternalImport] = []
        for method in self.methods:
            for type_annotation in method.get_types():
                if not isinstance(type_annotation, InternalImport):
                    continue
                result.append(type_annotation)

        return result

    @property
    def variable_name(self) -> str:
        """
        Get a proper variable name for an instance of this class.
        """
        return xform_name(self.name)
