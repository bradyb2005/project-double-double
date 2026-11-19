import json
import os
from pathlib import Path


class OrderRepository:
    def __init__(self, file_path=None):
        if file_path:
            self.filePath = file_path
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
            self.filePath = base_dir / "data" / "orders.json"

    def get_all_orders(self):
        try:
            with open(self.filePath, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError: 
            raise FileNotFoundError(f"File not found: {self.filePath}")
        except json.JSONDecodeError:
            raise ValueError(f"Error is not valid JSON: {self.filePath}")

    def save_orders(self, orders):  
        temp_path = f"{self.filePath}.tmp"  
        try:  
            with open(temp_path, "w") as file:  
                json.dump(orders, file, indent=4)  
            os.replace(temp_path, self.filePath)  
        except (OSError, TypeError, ValueError) as e:
            raise OSError(f"Error saving data to {self.filePath}: {e}")
        
    def get_order_by_id(self, order_id: int):
        orders = self.get_all_orders()
        for order in orders:
            if order.get("id") == order_id:
                return order
        return None

    def create_order(self, order: dict):
        orders = self.get_all_orders()
        next_id = max((o.get("id", 0) for o in orders), default = 0 ) + 1

        order["id"] = next_id
        orders.append(order)
        self.save_orders(orders)
        return order
