from sqlalchemy import String, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

from src.core.models import Base
from src.core.models.mixin import IdIntPkMixin

if TYPE_CHECKING:
    from src.core.models.order_menu_association import OrderMenuAssociation


class MenuItemModel(Base, IdIntPkMixin):
    __tablename__ = "menu_items"

    __table_args__ = (
        CheckConstraint(
            "type IN ('not assigned', 'first courses', 'second courses', 'garnishes', 'salads', 'desserts',"
            " 'cold drinks', 'hot drinks', 'others')",
            name="check_type_valid",
        ),
    )

    name: Mapped[str] = mapped_column(String(42))
    type: Mapped[str] = mapped_column(String(20), default="not assigned")
    price: Mapped[Optional[float]] = mapped_column(Numeric(8, 1))

    orders_details: Mapped[List["OrderMenuAssociation"]] = relationship(
        back_populates="menu_item",
    )

    def __str__(self) -> str:
        return (
            f"<Menu_item(id={self.id}, "
            f"name={self.name}, "
            f"type={self.type}, "
            f"price={self.price})>"
        )

    def __repr__(self) -> str:
        return str(self)

    class Meta:
        name: str = "Блюдо"
        name_plural: str = "Блюда"
