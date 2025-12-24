# Student ID: 650612093
# Student ID: 650612079

import pytest
from inventory import InMemoryInventory
from shipping import ShippingService
from order import OrderService
from payment import PaymentDeclinedError
from emailer import EmailService


# ---------- Stubs / Spies (Top-down) ----------

class StubSuccessPayment:
    def __init__(self, tx_id: str = "TX_OK"):
        self.tx_id = tx_id
        self.charges = []  # keep (amount, currency)

    def charge(self, amount: float, currency: str) -> str:
        self.charges.append((amount, currency))
        return self.tx_id

    def refund(self, transaction_id: str) -> None:
        return


class StubFailPaymentDeclined:
    """Fail แบบ business decline -> OrderService จะ release stock คืน"""
    def charge(self, amount: float, currency: str) -> str:
        raise PaymentDeclinedError("simulated decline")

    def refund(self, transaction_id: str) -> None:
        return


class StubFailPaymentNetwork:
    """Fail แบบ technical error (ไม่ได้เป็น PaymentDeclinedError) -> OrderService ไม่ release"""
    def charge(self, amount: float, currency: str) -> str:
        raise RuntimeError("simulated network error")

    def refund(self, transaction_id: str) -> None:
        return


class SpyEmail(EmailService):
    def __init__(self):
        self.sent = []  # list of (to, subject, body)

    def send(self, to: str, subject: str, body: str) -> None:
        self.sent.append((to, subject, body))


# ---------- Tests (Top-down) ----------

@pytest.mark.topdown
def test_success_sends_email_with_correct_subject_and_body_and_reduces_stock():
    inv = InMemoryInventory()
    inv.add_stock("SKU1", 10)

    pay = StubSuccessPayment(tx_id="TX123")
    spy_mail = SpyEmail()

    svc = OrderService(inv, pay, ShippingService(), spy_mail)
    items = [{"sku": "SKU1", "qty": 3, "price": 100.0, "weight": 1.0}]

    res = svc.place_order("a@b.com", items, region="TH")

    # stock should be reserved (reduced)
    assert inv.get_stock("SKU1") == 7

    # email must be sent with exact subject and body pattern from order.py
    assert len(spy_mail.sent) == 1
    to, subject, body = spy_mail.sent[0]
    assert to == "a@b.com"
    assert subject == "Order confirmed"
    # body uses total with 2 decimals and includes tx id
    assert f"tx={res['transaction_id']}" in body
    assert body.startswith(f"Total amount {res['total']:.2f} THB")

    # also verify payment was called with THB
    assert pay.charges and pay.charges[0][1] == "THB"


@pytest.mark.topdown
def test_payment_declined_releases_stock_and_does_not_send_email():
    inv = InMemoryInventory()
    inv.add_stock("SKU1", 10)

    svc = OrderService(inv, StubFailPaymentDeclined(), ShippingService(), SpyEmail())
    items = [{"sku": "SKU1", "qty": 3, "price": 100.0, "weight": 1.0}]

    with pytest.raises(PaymentDeclinedError):
        svc.place_order("a@b.com", items, region="TH")

    # because it's PaymentDeclinedError -> release happens
    assert inv.get_stock("SKU1") == 10


@pytest.mark.topdown
def test_payment_network_error_does_not_release_stock_and_does_not_send_email():
    inv = InMemoryInventory()
    inv.add_stock("SKU1", 10)

    spy_mail = SpyEmail()
    svc = OrderService(inv, StubFailPaymentNetwork(), ShippingService(), spy_mail)
    items = [{"sku": "SKU1", "qty": 3, "price": 100.0, "weight": 1.0}]

    with pytest.raises(RuntimeError):
        svc.place_order("a@b.com", items, region="TH")

    # IMPORTANT behavior from order.py: only PaymentDeclinedError triggers release
    # so stock stays reserved (reduced)
    assert inv.get_stock("SKU1") == 7

    # email should not be sent because we never reach send()
    assert spy_mail.sent == []
