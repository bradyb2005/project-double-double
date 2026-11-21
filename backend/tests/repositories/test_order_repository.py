import json

import pytest
from app.repositories.order_repository import OrderRepository


@pytest.fixture
def orders_data():
    return [
        {"id": 1, "customer_id": 1, "restaurant_id": 1, "total_price": 16.98, "status": "delivered"},
        {"id": 2, "customer_id": 2, "restaurant_id": 2, "total_price": 12.50, "status": "pending"},
        {"id": 3, "customer_id": 1, "restaurant_id": 3, "total_price": 9.99, "status": "pending"},
    ]


@pytest.fixture
def orders_file(tmp_path, orders_data):
    file_path = tmp_path / "orders.json"
    file_path.write_text(json.dumps(orders_data))
    return file_path


@pytest.fixture
def order_repository(orders_file):
    return OrderRepository(file_path=orders_file)


@pytest.fixture
def empty_order_repository(tmp_path):
    file_path = tmp_path / "orders.json"
    file_path.write_text("[]")
    return OrderRepository(file_path=file_path)


class TestGetAllOrders:
    def test_get_all_orders_returns_file_data(self, order_repository, orders_data):
        assert order_repository.get_all_orders() == orders_data

    def test_get_all_orders_returns_empty_list_for_empty_file(self, empty_order_repository):
        assert empty_order_repository.get_all_orders() == []

    def test_get_all_orders_raises_for_missing_file(self, tmp_path):
        repository = OrderRepository(file_path=tmp_path / "missing.json")

        with pytest.raises(FileNotFoundError, match="File not found"):
            repository.get_all_orders()

    def test_get_all_orders_raises_for_invalid_json(self, tmp_path):
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("not valid json")
        repository = OrderRepository(file_path=invalid_file)

        with pytest.raises(ValueError, match="not valid JSON"):
            repository.get_all_orders()


class TestSaveOrders:
    def test_save_orders_persists_data(self, order_repository):
        orders = [{"id": 10, "customer_id": 4, "status": "pending"}]

        order_repository.save_orders(orders)

        assert order_repository.get_all_orders() == orders

    def test_save_orders_leaves_no_temp_file(self, order_repository, orders_file):
        order_repository.save_orders([])

        assert not (orders_file.parent / "orders.json.tmp").exists()

    def test_save_orders_raises_for_unserializable_data(self, order_repository):
        with pytest.raises(OSError, match="Error saving data"):
            order_repository.save_orders([{"id": 1, "created_at": object()}])


class TestGetOrderById:
    def test_get_order_by_id_returns_matching_order(self, order_repository):
        order = order_repository.get_order_by_id(2)

        assert order is not None
        assert order["customer_id"] == 2
        assert order["total_price"] == 12.50

    def test_get_order_by_id_returns_none_for_unknown_order(self, order_repository):
        assert order_repository.get_order_by_id(999) is None


class TestGetOrdersByCustomerId:
    def test_get_orders_by_customer_id_returns_only_that_customers_orders(self, order_repository):
        orders = order_repository.get_orders_by_customer_id(1)

        assert [order["id"] for order in orders] == [1, 3]
        assert all(order["customer_id"] == 1 for order in orders)

    def test_get_orders_by_customer_id_returns_empty_list_for_customer_without_orders(self, order_repository):
        assert order_repository.get_orders_by_customer_id(42) == []


class TestCreateOrder:
    def test_create_order_assigns_next_id(self, order_repository):
        order = order_repository.create_order({"customer_id": 2, "status": "pending"})

        assert order["id"] == 4

    def test_create_order_persists_order(self, order_repository):
        order = order_repository.create_order({"customer_id": 2, "status": "pending"})

        assert order_repository.get_order_by_id(order["id"]) == order
        assert len(order_repository.get_all_orders()) == 4

    def test_create_order_starts_at_one_for_empty_file(self, empty_order_repository):
        order = empty_order_repository.create_order({"customer_id": 1, "status": "pending"})

        assert order["id"] == 1
        assert empty_order_repository.get_all_orders() == [order]

    def test_create_order_uses_highest_existing_id(self, tmp_path):
        file_path = tmp_path / "orders.json"
        file_path.write_text(json.dumps([{"id": 1}, {"id": 7}, {"id": 3}]))
        repository = OrderRepository(file_path=file_path)

        order = repository.create_order({"customer_id": 1, "status": "pending"})

        assert order["id"] == 8
