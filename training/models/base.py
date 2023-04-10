from typing import Any
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase


class Base(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSONB
    }
