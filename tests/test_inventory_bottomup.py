# Student ID: 650612093
# Student ID: 650612079

import pytest
from inventory import InMemoryInventory, InventoryError


@pytest.mark.bottomup
def test_inventory_reserve_and_release_restores_stock():
    inv = InMemoryInventory()
    inv.add_stock("S", 5)

    inv.reserve("S", 3)
    assert inv.get_stock("S") == 2

    inv.release("S", 3)
    assert inv.get_stock("S") == 5


@pytest.mark.bottomup
def test_inventory_reserve_exact_stock_boundary_ok():
    inv = InMemoryInventory()
    inv.add_stock("S", 5)

    inv.reserve("S", 5)
    assert inv.get_stock("S") == 0


@pytest.mark.bottomup
def test_inventory_not_enough_stock_boundary_raises():
    inv = InMemoryInventory()
    inv.add_stock("S", 1)

    with pytest.raises(InventoryError):
        inv.reserve("S", 2)
