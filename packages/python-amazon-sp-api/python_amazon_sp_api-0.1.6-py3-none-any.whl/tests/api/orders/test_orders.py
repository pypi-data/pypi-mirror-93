from datetime import datetime, timedelta

from sp_api.api import Orders
from sp_api.base import Marketplaces


def test_get_orders():
    res = Orders().get_orders(CreatedAfter='TEST_CASE_200')
    assert res.errors is None
    assert res.payload.get('Orders') is not None


def test_get_order_items():
    res = Orders().get_order_items('TEST_CASE_200')
    assert res.errors is None
    assert res.payload.get('AmazonOrderId') is not None


def test_get_order_address():
    res = Orders().get_order_address('TEST_CASE_200')
    assert res.errors is None
    assert res.payload.get('AmazonOrderId') is not None


def test_get_order_buyer_info():
    res = Orders().get_order_buyer_info('TEST_CASE_200')
    assert res.errors is None
    assert res.payload.get('AmazonOrderId') is not None


def test_get_order():
    res = Orders().get_order('TEST_CASE_200')
    assert res.errors is None
    assert res.payload.get('AmazonOrderId') is not None


def test_get_order_items_buyer_info():
    res = Orders().get_order_items_buyer_info('TEST_CASE_200')
    assert res.errors is None
    assert res.payload.get('AmazonOrderId') is not None

