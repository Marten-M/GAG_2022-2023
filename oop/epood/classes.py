"""Classes file."""

from typing import Tuple

import datetime

log_entry = Tuple[str, str]


class Customer(object):
    def __init__(self, id: int, money: float, gold_customer: bool):
        """
        Initialize customer.

        :param id: id of customer
        :param money: how much money customer has
        :param gold_customer: boolean indicating whether customer is of gold type
        """
        self.id = id
        self.basket = Basket()
        self.money = money
        self.gold_client = gold_customer
        self.history = []

    def get_history(self) -> list:
        """
        Get purchase history of customer.

        :return: list of purchases, where the most recent order is first
        """
        self.history.sort(key=lambda x: datetime.datetime.strptime(x[0], "%d/%m/%Y %H:%M"), reverse=True)
        return self.history

    def make_purchase(self) -> log_entry:
        """
        Make a purchase of the items in the customers basket.

        :return: log entry of purchase
        """
        cost = self.basket.cost
        if self.gold_client:
            cost *= 0.9
        # If customer does not have enough money
        if self.money < cost:
            raise ValueError

        self.money -= cost
        
        log = self.basket.get_purchase_log_entry()
        self.history.append(log)

        self.basket.clear()
        return log


class Item(object):
    def __init__(self, name: str, price: float):
        """
        Initialize sellable item.

        :param name: name of item
        :param price: price of item
        """
        self.name = name
        if price < 0:
            raise ValueError
        self.price = price


class Basket(object):
    def __init__(self):
        """
        Initialize class.
        """
        self.items = dict()

    def add_item(self, item: Item, amount: int):
        """
        Add item to basket.

        :param item: item to add
        :param amount: how many items to add
        """
        if amount < 0:
            raise ValueError
        self.items[item] = self.items.get(item, 0) + amount

    def remove_item(self, item: Item, amount: int):
        """
        Remove items from basket.

        :param item: item to remove
        :param amount: how many items to remove
        """
        if amount < 0:
            raise ValueError
        if item not in self.items or self.items[item] < amount:
            raise ValueError
        self.items[item] -= amount

    @property
    def empty(self) -> bool:
        """
        Get whether the basket is empty.
        """
        return len(self.items) == 0

    @property
    def cost(self) -> float:
        """
        Get the total cost of the items in the basket.
        """
        sm = 0
        for item in self.items:
            sm += self.items[item] * item.price
        return sm
    
    def clear(self):
        """
        Empty the basket of items.
        """
        self.items.clear()

    def get_purchase_log_entry(self) -> log_entry:
        """
        Get purchase log entry of current basket.

        :return: tuple containing the time of purchase and the purchased item names with their counts
        """
        time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        log = ", ".join(f"{item.name} x {self.items[item]}" for item in self.items)
        
        return (time, log)

    def __contains__(self, key):
        return key in self.items


class Store(object):
    def __init__(self):
        """
        Initialize class.
        """
        self.items = dict()
        self.purchases = dict()
        self.customers = []
        self.id_tracker = 0

    def add_customer(self, money: float, gold_customer: bool):
        """
        Add customer to store.

        :param money: how much money customer to add has
        :param gold_customer: whether the customer to add is a gold customer
        """
        if money < 0:
            raise ValueError

        customer = Customer(self.id_tracker, money, gold_customer)
        self.customers.append(customer)
        self.id_tracker += 1

    def make_purchase(self, customer: Customer):
        """
        Have a customer make a purchase.

        :param customer: customer that makes the purchase
        """
        # Check if store has enough items in stock for the purchase
        customer_items = customer.basket.items.copy()
        for item in customer_items:
            if not self.in_stock(item, customer_items[item]):
                raise ValueError

        
        log_entry = customer.make_purchase()
        for item in customer_items:
            self.items[item] -= customer_items[item]
        tmp = self.purchases.get(customer, [])
        tmp.append(log_entry)
        self.purchases[customer] = tmp

    def in_stock(self, item: Item, count: int) -> bool:
        """
        Check if the store has enough of a given item.

        :param item: item who'se stock to check
        :param count: how many should be in stock

        :return: boolean indicating whether the store has enough of given item in stock
        """
        return self.items[item] >= count
