"""
Main entrypoint for builder.
"""
import sys
from typing import List

from boto3 import __version__ as boto3_version
from boto3.session import Session

from mypy_boto3_builder.cli_parser import parse_args
from mypy_boto3_builder.constants import BOTO3_STUBS_NAME, DUMMY_REGION, MODULE_NAME, PYPI_NAME
from mypy_boto3_builder.jinja_manager import JinjaManager
from mypy_boto3_builder.logger import get_logger
from mypy_boto3_builder.service_name import ServiceName, ServiceNameCatalog
from mypy_boto3_builder.writers.processors import (
    process_boto3_stubs,
    process_master,
    process_service,
)


def main() -> None:
    """
    Main entrypoint for builder.
    """
    args = parse_args(sys.argv[1:])
    logger = get_logger(verbose=args.debug, panic=args.panic)
    session = Session(region_name=DUMMY_REGION)
    args.output_path.mkdir(exist_ok=True)
    service_names: List[ServiceName] = []
    master_service_names: List[ServiceName] = []
    available_services = session.get_available_services()

    for available_service in available_services:
        try:
            service_name = ServiceNameCatalog.find(available_service)
        except ValueError:
            logger.info(f"Service {available_service} is not fully supported.")
            continue

        service_name.boto3_version = boto3_version
        master_service_names.append(service_name)

    if args.service_names:
        for service_name in args.service_names:
            if service_name.name not in available_services:
                logger.info(f"Service {service_name.name} is not provided by boto3, skipping.")
                continue

            service_name.boto3_version = boto3_version
            service_names.append(service_name)
    else:
        service_names = master_service_names

    build_version = args.build_version or boto3_version
    JinjaManager.update_globals(
        master_pypi_name=PYPI_NAME,
        master_module_name=MODULE_NAME,
        boto3_stubs_name=BOTO3_STUBS_NAME,
        boto3_version=boto3_version,
        build_version=build_version,
        builder_version=args.builder_version,
    )

    logger.info(f"Bulding version {build_version}")

    if not args.skip_services:
        total_str = f"{len(service_names)}"
        for index, service_name in enumerate(service_names):
            current_str = f"{{:0{len(total_str)}}}".format(index + 1)
            logger.info(f"[{current_str}/{total_str}] Generating {service_name.module_name} module")
            process_service(
                session=session,
                output_path=args.output_path,
                service_name=service_name,
                generate_setup=not args.installed,
            )

    if not args.skip_master:
        if not args.installed:
            logger.info(f"Generating {MODULE_NAME} module")
            process_master(
                session,
                args.output_path,
                service_names,
                generate_setup=not args.installed,
            )

        logger.info(f"Generating {BOTO3_STUBS_NAME} module")
        process_boto3_stubs(
            session,
            args.output_path,
            service_names,
            generate_setup=not args.installed,
        )

    logger.info("Completed")


if __name__ == "__main__":
    main()
