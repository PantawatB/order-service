import pytest
from inventory import InMemoryInventory, InventoryError

def test_inventory_reserve_and_release():
    inv = InMemoryInventory()
    inv.add_stock("S", 5)
    inv.reserve("S", 3)
    assert inv.get_stock("S") == 2
    inv.release("S", 3)
    assert inv.get_stock("S") == 5

def test_inventory_not_enough_stock():
    inv = InMemoryInventory()
    inv.add_stock("S", 1)
    with pytest.raises(InventoryError):
        inv.reserve("S", 2)
