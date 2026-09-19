"""M1 lesson 3: implement the list-based inventory.

Replace every `NotImplementedError` below. Do not change the public method
names or the exception types — the tests depend on them.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from herodungeon.core.events import AlgorithmEvent, EventRecorder
from herodungeon.core.models import Item


class InventoryFullError(ValueError):
    pass


class ItemNotFoundError(KeyError):
    pass


@dataclass(slots=True)
class Inventory:
    capacity: int
    recorder: EventRecorder = field(default_factory=EventRecorder)
    _items: list[Item] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.capacity <= 0:
            raise ValueError("capacity must be positive")

    @property
    def items(self) -> tuple[Item, ...]:
        return tuple(self._items)

    def add(self, item: Item) -> AlgorithmEvent:
        """Append `item` if there is room; otherwise reject and raise."""
        if len(self._items) >= self.capacity:
            self.recorder.emit("reject", "inventory", item_id=item.item_id)
            raise InventoryFullError("inventory full") # TODO: 背包满时 emit reject 并抛出 InventoryFullError
        for old_item in self._items:
            if old_item.item_id == item.item_id:
                raise ValueError("duplicate item id") # TODO: item_id 重复时抛出 ValueError
        self._items.append(item)
        return self.recorder.emit("insert", "inventory", item_id=item.item_id)# TODO: 追加物品并 emit insert
        # raise NotImplementedError("implement Inventory.add")

    def remove(self, item_id: str) -> Item:
        """Find `item_id` from the front, emit compare/remove/miss, and return it."""
        for idx, existed_item in enumerate(self._items):
            self.recorder.emit("compare", "inventory", item_id=existed_item.item_id)# TODO: 逐个 compare
            if existed_item.item_id == item_id:
                removed_item = self._items.pop(idx)
                self.recorder.emit("remove", "inventory", item_id=item_id)
                return removed_item# TODO: 找到后 pop，emit remove，返回该物品
        self.recorder.emit("miss", "inventory", item_id=item_id)
        raise ItemNotFoundError(f"item {item_id} not found")# TODO: 找不到时 emit miss 并抛出 ItemNotFoundError
        # raise NotImplementedError("implement Inventory.remove")

    def total_value(self) -> int:
        """Return the sum of item values currently in the bag."""
        return sum(item.value for item in self._items)# TODO: 返回所有物品 value 之和
        # raise NotImplementedError("implement Inventory.total_value")
