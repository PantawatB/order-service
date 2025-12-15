import pytest
from inventory import InMemoryInventory
from shipping import ShippingService
from order import OrderService
from payment import PaymentDeclinedError
from emailer import EmailService

class StubFailPayment:
    def charge(self, amount: float, currency: str) -> str:
        raise PaymentDeclinedError("simulated decline")
    def refund(self, transaction_id: str) -> None:
        return

class SpyEmail(EmailService):
    def __init__(self):
        self.sent = []
    def send(self, to, subject, body):
        self.sent.append((to, subject, body))

def test_payment_decline_releases_stock():
    inv = InMemoryInventory()
    inv.add_stock("SKU1", 10)
    svc = OrderService(inv, StubFailPayment(), ShippingService(), SpyEmail())
    items = [{"sku":"SKU1","qty":3,"price":100.0,"weight":1.0}]
    with pytest.raises(PaymentDeclinedError):
        svc.place_order("a@b.com", items, region="TH")
    assert inv.get_stock("SKU1") == 10
