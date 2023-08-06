"""
Boto3 ServiceResource.
"""
from typing import List, Set, Tuple

from boto3.resources.base import ServiceResource as Boto3ServiceResource

from mypy_boto3_builder.import_helpers.import_string import ImportString
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.structures.class_record import ClassRecord
from mypy_boto3_builder.structures.collection import Collection
from mypy_boto3_builder.structures.resource import Resource
from mypy_boto3_builder.type_annotations.external_import import ExternalImport
from mypy_boto3_builder.type_annotations.fake_annotation import FakeAnnotation
from mypy_boto3_builder.type_annotations.internal_import import InternalImport


class ServiceResource(ClassRecord):
    """
    Boto3 ServiceResource.
    """

    _alias_name = "ServiceResource"

    def __init__(
        self,
        name: str,
        service_name: ServiceName,
        boto3_service_resource: Boto3ServiceResource,
        docstring: str = "",
    ):
        super().__init__(
            name=name,
            docstring=docstring,
            bases=[
                ExternalImport(
                    source=ImportString("boto3", "resources", "base"),
                    name="ServiceResource",
                    alias="Boto3ServiceResource",
                )
            ],
        )
        self.service_name = service_name
        self.boto3_service_resource = boto3_service_resource
        self.collections: List[Collection] = []
        self.sub_resources: List[Resource] = []

    def __hash__(self) -> int:
        return hash(self.service_name)

    def get_types(self) -> Set[FakeAnnotation]:
        types = super().get_types()
        for collection in self.collections:
            types.update(collection.get_types())
        for sub_resource in self.sub_resources:
            types.update(sub_resource.get_types())

        return types

    def get_all_names(self) -> List[str]:
        result = [self.name]
        for resource in self.sub_resources:
            result.append(resource.name)
        for collection in self.get_collections():
            result.append(collection.name)
        return result

    def get_collections(self) -> List[Collection]:
        collection_names = [i.name for i in self.collections]
        result: List[Collection] = []
        result.extend(self.collections)
        for resource in self.sub_resources:
            for collection in resource.collections:
                if collection.name in collection_names:
                    raise ValueError(f"Conflicting collections: {collection.name}")
                collection_names.append(collection.name)
                result.append(collection)

        return result

    def get_sub_resources(self) -> List[Resource]:
        """
        Get sub-resource in safe order.

        Returns:
            A list of sub resources.
        """
        result: List[Resource] = []
        all_names: Set[str] = {i.name for i in self.sub_resources}
        added_names: Set[str] = set()
        sub_resources = list(self.sub_resources)
        sub_resources_list: List[Tuple[Resource, List[InternalImport]]] = []
        for sub_resource in sub_resources:
            internal_imports = sub_resource.get_internal_imports()
            sub_resources_list.append((sub_resource, internal_imports))

        sub_resources_list.sort(key=lambda x: len(x[1]))
        for sub_resource, internal_imports in sub_resources_list:
            for internal_import in internal_imports:
                if internal_import.name not in all_names:
                    continue
                if internal_import.name in added_names:
                    continue

                internal_import.stringify = True

            result.append(sub_resource)
            added_names.add(sub_resource.name)

        return result
