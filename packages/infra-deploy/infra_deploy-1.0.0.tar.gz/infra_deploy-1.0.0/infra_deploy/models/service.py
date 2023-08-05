# from ctypes import Union
from loguru import logger
from pydantic.types import OptionalInt
from infra_deploy.models import ApiKinds, ServiceApiVersion
from infra_deploy.models.general import Metadatable, Selectable
from typing import Any, Dict, List, Optional, Union
from kubernetes.client import V1ServiceSpec, V1Service, V1ServicePort
from pydantic import BaseModel
from infra_deploy.models.base import KubeModel
from infra_deploy.utils import (
    remove_nones_dict as cleard,
)
from infra_deploy.models.ambassador.mappings import Mapping

DictStrAny = Dict[str, Any]
RecurseDictAny = Dict[str, DictStrAny]


class ServicePort(KubeModel):
    __api_model__: V1ServicePort = V1ServicePort

    port: int
    target_port: Optional[int]
    name: Optional[str]
    node_port: Optional[int]
    protocol: Optional[int]

    def __init__(
        self,
        *,
        port: int,
        target_port: Optional[Union[str,
                                    int]] = None,
        name: Optional[str] = None,
        node_port: Optional[int] = None,
        protocol: Optional[int] = None,
        **data: Any
    ) -> None:
        data.update(
            cleard(
                dict(
                    port=port,
                    target_port=target_port,
                    name=name,
                    node_port=node_port,
                    protocol=protocol
                )
            )
        )
        super().__init__(**data)

    def to_kube(self) -> V1ServicePort:
        _values: DictStrAny = self.get_compatible(is_convert=True)

        return V1ServicePort(**_values)


class Service(KubeModel, Metadatable, Selectable):
    __context__: str = "service"
    __service_spec__: V1ServiceSpec = V1ServiceSpec
    __api_model__: V1Service = V1Service

    api_version: ServiceApiVersion = ServiceApiVersion.V1
    ports: List[ServicePort] = []
    kind: ApiKinds = ApiKinds.SERVICE
    mappings: Optional[Mapping] = None
    latest_name: Optional[str] = None

    def __init__(self, *, name: str, **data: Any) -> None:
        super().__init__(**data)
        self.add_name(name)

    def add_name(self, name: str):
        self.add_meta("name", name)
        if self.mappings is not None:
            self.mappings.update_service(name)
        self.latest_name = name

    def add_service_port(self, **kwargs) -> ServicePort:
        return ServicePort(**kwargs)

    def to_kube(self):
        return V1Service(
            api_version=self.api_version.value,
            kind="Service",
            metadata=self.kube_meta,
            spec=V1ServiceSpec(
                selector=self.to_kube_select()['selector'],
                ports=[port.to_kube() for port in self.ports]
            )
        )

    def add_mappings(self, prefix: str, namespace: str = "default"):
        if self.latest_name is None:
            raise AttributeError("A name hasn't been set yet.")
        self.mappings = Mapping(
            name=self.latest_name,
            prefix=prefix,
            service=self.latest_name,
            namespace=namespace,
        )

    def ambassador_kube(self):
        return self.mappings.to_kube()

    def override_name(self, name: str):
        # logger.info("overriding name")
        self.add_selector("selector", dict(app=str(name)))

    def override_image(self, img: str):
        pass

    def override_port(self, num: int, target: OptionalInt = None):
        # logger.debug(target)
        new_service = ServicePort(port=num)
        if target is not None:
            new_service = ServicePort(port=target, target_port=num)
        self.ports = [new_service]
        # logger.info(self.ports)

    def override_service_name(self, name: str):
        self.add_name(name)