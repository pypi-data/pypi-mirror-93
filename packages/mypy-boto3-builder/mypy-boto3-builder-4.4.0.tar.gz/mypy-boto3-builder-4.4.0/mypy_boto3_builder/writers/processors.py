"""
Processors for parsing and writing modules.
"""
from pathlib import Path
from typing import List

from boto3.session import Session

from mypy_boto3_builder.logger import get_logger
from mypy_boto3_builder.parsers.boto3_stubs_package import parse_boto3_stubs_package
from mypy_boto3_builder.parsers.master_package import parse_master_package
from mypy_boto3_builder.parsers.service_package import parse_service_package
from mypy_boto3_builder.service_name import ServiceName
from mypy_boto3_builder.structures.boto3_stubs_package import Boto3StubsPackage
from mypy_boto3_builder.structures.master_package import MasterPackage
from mypy_boto3_builder.structures.service_package import ServicePackage
from mypy_boto3_builder.utils.nice_path import NicePath
from mypy_boto3_builder.writers.boto3_stubs_package import write_boto3_stubs_package
from mypy_boto3_builder.writers.master_package import write_master_package
from mypy_boto3_builder.writers.service_package import write_service_package

logger = get_logger()


def process_boto3_stubs(
    session: Session,
    output_path: Path,
    service_names: List[ServiceName],
    generate_setup: bool,
) -> Boto3StubsPackage:
    """
    Parse and write stubs package `boto3_stubs`.

    Arguments:
        session -- boto3 session.
        output_path -- Package output path.
        service_names -- List of known service names.
        generate_setup -- Whether to generate install or installed package.

    Return:
        Parsed Boto3StubsPackage.
    """
    logger.debug("Parsing boto3 stubs")
    boto3_stub_package = parse_boto3_stubs_package(session=session, service_names=service_names)
    logger.debug(f"Writing boto3 stubs to {NicePath(output_path)}")

    modified_paths = write_boto3_stubs_package(
        boto3_stub_package, output_path, generate_setup=generate_setup
    )
    for modified_path in modified_paths:
        logger.debug(f"Updated {NicePath(modified_path)}")

    return boto3_stub_package


def process_master(
    session: Session,
    output_path: Path,
    service_names: List[ServiceName],
    generate_setup: bool,
) -> MasterPackage:
    """
    Parse and write master package `mypy_boto3`.

    Arguments:
        session -- boto3 session.
        output_path -- Package output path.
        service_names -- List of known service names.
        generate_setup -- Whether to generate install or installed package.

    Return:
        Parsed MasterPackage.
    """
    logger.debug("Parsing master")
    master_package = parse_master_package(session, service_names)
    logger.debug(f"Writing master to {NicePath(output_path)}")

    modified_paths = write_master_package(
        master_package, output_path=output_path, generate_setup=generate_setup
    )
    for modified_path in modified_paths:
        logger.debug(f"Updated {NicePath(modified_path)}")

    return master_package


def process_service(
    session: Session,
    service_name: ServiceName,
    output_path: Path,
    generate_setup: bool,
) -> ServicePackage:
    """
    Parse and write service package `mypy_boto3_*`.

    Arguments:
        session -- boto3 session.
        service_name -- Target service name.
        output_path -- Package output path.
        generate_setup -- Whether to generate install or installed package.

    Return:
        Parsed ServicePackage.
    """
    logger.debug(f"Parsing {service_name.boto3_name}")
    service_module = parse_service_package(session, service_name)
    logger.debug(f"Writing {service_name.boto3_name} to {NicePath(output_path)}")

    modified_paths = write_service_package(
        service_module, output_path=output_path, generate_setup=generate_setup
    )
    for modified_path in modified_paths:
        logger.debug(f"Updated {NicePath(modified_path)}")

    return service_module
