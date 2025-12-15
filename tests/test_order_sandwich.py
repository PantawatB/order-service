from inventory import InMemoryInventory
from payment import SimplePayment
from shipping import ShippingService
from order import OrderService
from emailer import EmailService

class SpyEmail(EmailService):
    def __init__(self): self.calls = 0
    def send(self, to, subject, body): self.calls += 1

def test_order_success_with_real_payment():
    inv = InMemoryInventory()
    inv.add_stock("A", 2)
    svc = OrderService(inv, SimplePayment(), ShippingService(), SpyEmail())
    items = [{"sku":"A","qty":1,"price":900.0,"weight":2.0}]
    res = svc.place_order("x@y.com", items, region="TH")
    assert inv.get_stock("A") == 1
