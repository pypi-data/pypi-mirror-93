"""
Creates, updates, and deletes a deployment using AppsV1Api.
"""

from typing import Any, Dict, List, Literal, Optional, Type

from infra_deploy.models import PullPolicy
from infra_deploy.models.base import KubeModel
from kubernetes import client
from kubernetes.client import V1Container, V1ResourceRequirements
from loguru import logger
from pydantic import BaseModel, ByteSize

DictStrAny = Dict[str, Any]
RecurseDictAny = Dict[str, DictStrAny]
OptBySize = Optional[ByteSize]
RESOURCE_ATTRS = V1ResourceRequirements.attribute_map


def ref_mem(value: str) -> str:
    removed_b = value.capitalize().rsplit("b")[0]
    i = 0
    for i, c in enumerate(removed_b):
        if not c.isdigit() and c != ".":
            break

    # logger.info(i)
    # logger.debug(removed_b[:i])
    # logger.debug(removed_b[i:])

    return (removed_b[:i] + removed_b[i:].capitalize())


class MemCPU(BaseModel):
    memory: OptBySize
    cpu: OptBySize

    def to_kube(self):
        return {
            "memory": ref_mem(self.memory.human_readable()),
            "cpu": ref_mem(self.cpu.human_readable(decimal=True)).lower()
        }


class ContainerModel(KubeModel):
    __context__: str = "container"
    __api_model__: Type[V1Container] = V1Container
    name: str
    image: str
    pull_policy: str = "Always"
    ports: Dict[str, int] = {}
    resources: Dict[Literal["limits", "requests"], MemCPU] = {}

    def __init__(
        __pydantic_self__,
        *,
        name: str,
        image: str,
        ports: Dict[str,
                    int] = {},
        **data: Any
    ) -> None:
        data['name'] = name
        data['image'] = image
        data['ports'] = ports

        super().__init__(**data)

    def to_kube(self):
        return V1Container(
            name=self.name,
            image=self.image,
            image_pull_policy=self.pull_policy,
            ports=[
                client.V1ContainerPort(container_port=v)
                for v in self.ports.values()
            ],
            resources=client.V1ResourceRequirements(
                **{k: v.dict()
                   for k,
                   v in self.resources.items()}
            )
        )


class Container(KubeModel):
    # We'll take the information from decorator functions
    __api_model__: Type[V1Container] = V1Container
    name: str
    image: str
    pull_policy: PullPolicy = PullPolicy.ALWAYS
    ports: List[int] = []
    resources: Dict[str, MemCPU] = {}

    def __init__(
        __pydantic_self__,
        *,
        name: str,
        image: str,
        ports: List[int] = [],
        **data: Any
    ) -> None:
        data['name'] = name
        data['image'] = image
        data['ports'] = ports

        super().__init__(**data)

    def add_resource(self, name, **values):
        if name not in RESOURCE_ATTRS:
            raise ValueError(
                f"Item {name} isn't one of the field names [{RESOURCE_ATTRS.keys()}]"
            )

        self.resources[name] = MemCPU(**values)

    @property
    def kresources(self):
        return V1ResourceRequirements(
            **{k: v.to_kube()
               for k,
               v in self.resources.items()}
        )

    def to_kube(self):
        # logger.info()
        response = V1Container(
            name=self.name,
            image=self.image,
            image_pull_policy=self.pull_policy,
            ports=[
                client.V1ContainerPort(container_port=v) for v in self.ports
            ]
        )
        resrc = self.resources
        if not resrc:
            return response
        response.resources = self.kresources
        return response
