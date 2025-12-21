# Student ID: 650612093

import pytest
from inventory import InMemoryInventory, InventoryError
from payment import SimplePayment, PaymentDeclinedError
from shipping import ShippingService
from order import OrderService
from emailer import EmailService


class SpyEmail(EmailService):
    def __init__(self):
        self.sent = []  # list of (to, subject, body)

    def send(self, to: str, subject: str, body: str) -> None:
        self.sent.append((to, subject, body))


@pytest.mark.sandwich
def test_order_success_with_real_payment_and_email_spy_region_th():
    inv = InMemoryInventory()
    inv.add_stock("A", 2)

    mail = SpyEmail()
    svc = OrderService(inv, SimplePayment(), ShippingService(), mail)
    items = [{"sku": "A", "qty": 1, "price": 900.0, "weight": 2.0}]

    res = svc.place_order("x@y.com", items, region="TH")

    assert inv.get_stock("A") == 1
    assert len(mail.sent) == 1

    to, subject, body = mail.sent[0]
    assert to == "x@y.com"
    assert subject == "Order confirmed"
    assert f"tx={res['transaction_id']}" in body
    assert body.startswith(f"Total amount {res['total']:.2f} THB")


@pytest.mark.sandwich
def test_order_success_region_us_sends_email_and_reduces_stock():
    inv = InMemoryInventory()
    inv.add_stock("A", 2)

    mail = SpyEmail()
    svc = OrderService(inv, SimplePayment(), ShippingService(), mail)

    # IMPORTANT: SimplePayment declines when amount > 1000
    # so make total <= 1000 to ensure success in US region too
    items = [{"sku": "A", "qty": 1, "price": 500.0, "weight": 2.0}]

    res = svc.place_order("x@y.com", items, region="US")

    assert inv.get_stock("A") == 1
    assert len(mail.sent) == 1

    to, subject, body = mail.sent[0]
    assert to == "x@y.com"
    assert subject == "Order confirmed"
    assert f"tx={res['transaction_id']}" in body
    assert body.startswith(f"Total amount {res['total']:.2f} THB")


@pytest.mark.sandwich
def test_order_us_total_too_high_declines_and_releases_stock_and_no_email():
    inv = InMemoryInventory()
    inv.add_stock("A", 2)

    mail = SpyEmail()
    svc = OrderService(inv, SimplePayment(), ShippingService(), mail)

    # ตั้งใจทำให้ total > 1000 เพื่อให้ PaymentDeclinedError("amount too high")
    items = [{"sku": "A", "qty": 1, "price": 900.0, "weight": 2.0}]

    with pytest.raises(PaymentDeclinedError):
        svc.place_order("x@y.com", items, region="US")

    # เพราะเป็น PaymentDeclinedError -> order.py ต้อง release คืน
    assert inv.get_stock("A") == 2
    assert mail.sent == []


@pytest.mark.sandwich
def test_order_inventory_error_no_payment_no_email():
    inv = InMemoryInventory()
    inv.add_stock("A", 0)  # force not enough stock

    mail = SpyEmail()
    svc = OrderService(inv, SimplePayment(), ShippingService(), mail)
    items = [{"sku": "A", "qty": 1, "price": 900.0, "weight": 2.0}]

    with pytest.raises(InventoryError):
        svc.place_order("x@y.com", items, region="US")

    # should not send email
    assert mail.sent == []
