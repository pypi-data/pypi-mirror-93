"""Main cloudwanderer module."""
from cloudwanderer.cloud_wanderer_resource import CloudWandererResource
from typing import List
import logging
from typing import TYPE_CHECKING, Iterator, Callable
import concurrent.futures
from .utils import exception_logging_wrapper
from .boto3_interface import CloudWandererBoto3Interface
from .aws_urn import AwsUrn

logger = logging.getLogger('cloudwanderer')

if TYPE_CHECKING:
    from .storage_connectors import BaseStorageConnector  # noqa


class CloudWanderer():
    """CloudWanderer."""

    def __init__(
            self, storage_connectors: List['BaseStorageConnector'],
            cloud_interface: CloudWandererBoto3Interface = None) -> None:
        """Initialise CloudWanderer.

        Args:
            storage_connectors:
                CloudWanderer storage connector objects.
            cloud_interface (CloudWandererBoto3Interface):
                The cloud interface to get resources from.
                Defaults to :class:`~cloudwanderer.boto3_interface.CloudWandererBoto3Interface`.
        """
        self.storage_connectors = storage_connectors
        self.cloud_interface = cloud_interface or CloudWandererBoto3Interface()

    def write_resources(
            self, exclude_resources: List[str] = None, **kwargs) -> None:
        """Write all AWS resources in this account from all regions and all services to storage.

        Any additional args will be passed into the cloud interface's ``get_`` methods.

        Arguments:
            exclude_resources (list): A list of service:resources to exclude (e.g. ``['ec2:instance']``)
            **kwargs: Additional keyword arguments will be passed down to the cloud interface methods.
        """
        logger.info('Writing resources in all regions')
        for region_name in self.cloud_interface.enabled_regions:
            self.write_resources_in_region(
                exclude_resources=exclude_resources,
                region_name=region_name,
                **kwargs
            )

    def write_resources_concurrently(
            self, cloud_interface_generator: Callable, exclude_resources: List[str] = None, concurrency: int = 10,
            **kwargs) -> None:
        """Write all AWS resources in this account from all regions and all services to storage.

        Any additional args will be passed into the cloud interface's ``get_`` methods.

        Arguments:
            exclude_resources (list):
                exclude_resources (list): A list of service:resources to exclude (e.g. ``['ec2:instance']``)
            concurrency (int):
                Number of query threads to invoke concurrently.
                If the number of threads exceeds the number of regions by at least two times
                multiple services to be queried concurrently in each region.
                **WARNING:** Experimental. Complete data capture depends heavily on the thread safeness of the
                storage connector and has not been thoroughly tested!
            cloud_interface_generator (Callable): A method which returns a new cloud interface session when called.
                This helps prevent non-threadsafe cloud interfaces from interfering with each others.
            **kwargs: Additional keyword arguments will be passed down to the cloud interface methods.
        """
        logger.info('Writing resources in all regions')
        logger.warning('Using concurrency of: %s - CONCURRENCY IS EXPERIMENTAL', concurrency)
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            for region_name in self.cloud_interface.enabled_regions:
                cw = CloudWanderer(
                    storage_connectors=self.storage_connectors,
                    cloud_interface=cloud_interface_generator()
                )
                executor.submit(
                    exception_logging_wrapper,
                    method=cw.write_resources_in_region,
                    exclude_resources=exclude_resources,
                    region_name=region_name,
                    **kwargs
                )

    def write_resources_in_region(
            self, exclude_resources: List[str] = None, region_name: str = None,
            **kwargs) -> None:
        """Write all AWS resources in this account region from all services to storage.

        Any additional args will be passed into the cloud interface's ``get_`` methods.

        Arguments:
            exclude_resources (list):
                exclude_resources (list): A list of service:resources to exclude (e.g. ``['ec2:instance']``)
            region_name (str):
                The name of the region to get resources from
                (defaults to session default if not specified)
            **kwargs: Additional keyword arguments will be passed down to the cloud interface methods.
        """
        exclude_resources = exclude_resources or []
        for boto3_service in self.cloud_interface.get_all_resource_services():
            self.write_resources_of_service_in_region(
                service_name=boto3_service.meta.service_name,
                exclude_resources=exclude_resources,
                region_name=region_name,
                **kwargs
            )

    def write_resources_of_service_in_region(
            self, service_name: str, exclude_resources: List[str] = None,
            region_name: str = None, **kwargs) -> None:
        """Write all AWS resources in this region in this service to storage.

        Cleans up any resources in the StorageConnector that no longer exist.

        Any additional args will be passed into the cloud interface's ``get_`` methods.

        Arguments:
            service_name (str):
                The name of the service to write resources for (e.g. ``'ec2'``)
            exclude_resources (list):
                exclude_resources (list): A list of service:resources to exclude (e.g. ``['ec2:instance']``)
            region_name (str):
                The name of the region to get resources from
                (defaults to session default if not specified)
            **kwargs: Additional keyword arguments will be passed down to the cloud interface methods.
        """
        region_name = region_name or self.cloud_interface.region_name

        logger.info("Writing all %s resources in %s", service_name, region_name)
        exclude_resources = exclude_resources or []

        for resource_type in self.cloud_interface.get_service_resource_types(service_name=service_name):
            if f'{service_name}:{resource_type}' in exclude_resources:
                logger.info('Skipping %s as per exclude_resources', f'{service_name}:{resource_type}')
                continue
            self.write_resources_of_type_in_region(
                service_name=service_name,
                resource_type=resource_type,
                region_name=region_name,
                **kwargs
            )

    def write_resources_of_type_in_region(
            self, service_name: str, resource_type: str = None,
            region_name: str = None, **kwargs) -> None:
        """Write all AWS resources in this region in this service to storage.

        Cleans up any resources in the StorageConnector that no longer exist.

        Any additional args will be passed into the cloud interface's ``get_`` methods.

        Arguments:
            service_name (str):
                The name of the service to write resources for (e.g. ``'ec2'``)
            resource_type (str):
                The name of the type of the resource to write (e.g. ``'instance'``)
            region_name (str):
                The name of the region to get resources from
                (defaults to session default if not specified)
            **kwargs: Additional keyword arguments will be passed down to the cloud interface methods.
        """
        region_name = region_name or self.cloud_interface.region_name
        logger.info('--> Fetching %s %s from %s', service_name, resource_type, region_name)
        resources = self.cloud_interface.get_resources_of_type(
            service_name=service_name, resource_type=resource_type, region_name=region_name, **kwargs)
        urns = []
        for resource in resources:
            urns.extend(list(self._write_resource(resource, region_name)))

        self._clean_resources_in_region(service_name, resource_type, region_name, urns)

    def _write_resource(self, resource: CloudWandererResource, region_name: str) -> Iterator[AwsUrn]:
        for storage_connector in self.storage_connectors:
            storage_connector.write_resource(resource)
        yield resource.urn

    def _clean_resources_in_region(
            self, service_name: str, resource_type: str, region_name: str, current_urns: List[AwsUrn]) -> None:
        """Remove all resources of this type in this region which no longer exist.

        Arguments:
            service_name (str):
                The name of the service to write resources for (e.g. ``'ec2'``)
            resource_type (str):
                The name of the type of the resource to write (e.g. ``'instance'``)
            region_name (str):
                The name of the region to get resources from
                (defaults to session default if not specified)
            current_urns (List[AwsUrn]):
                A list of URNs which are still current and should not be deleted.
        """
        regions_returned = self.cloud_interface.resource_regions_returned_from_api_region(service_name, region_name)
        for region_name in regions_returned:
            logger.info('---> Deleting %s %s from %s', service_name, resource_type, region_name)
            for storage_connector in self.storage_connectors:
                storage_connector.delete_resource_of_type_in_account_region(
                    service=service_name,
                    resource_type=resource_type,
                    account_id=self.cloud_interface.account_id,
                    region=region_name,
                    urns_to_keep=current_urns
                )
