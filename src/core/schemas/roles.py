from pydantic import BaseModel, field_validator, ConfigDict
from typing import List

from src.core.models import Permission


class RoleBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    pass


class Role(RoleBase):
    id: int
    permissions: List[str]

    @field_validator("permissions")
    @classmethod
    def convert_permissions_to_strings(cls, perm):
        if isinstance(perm, Permission):
            return perm.name
        return perm
