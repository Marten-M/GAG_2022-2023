import datetime

from classes import Customer, Basket, Store, Item

items = [Item("apple", 2), Item("pear", 5), Item("Car", 1000)]


def test_add_item_to_basket_adding_possible():
    """
    Testcase to test adding items to a basket when adding is possible.
    """
    basket = Basket()
    basket.add_item(items[0], 2)
    basket.add_item(items[1], 4)
    assert basket.items[items[0]] == 2
    assert basket.items[items[1]] == 4


def test_add_item_to_basket_amount_negative():
    """
    Testcase to add a negative amount of items to a basket.
    """
    basket = Basket()
    try:
        basket.add_item(items[0], -2)
        assert False
    except ValueError:
        assert True


def test_add_item_to_basket_some_items_already_in_basket():
    """
    Testcase where an item is added to a basket that already has some of that item.
    """
    basket = Basket()
    basket.add_item(items[2], 5)
    basket.add_item(items[2], 7)
    assert basket.items[items[2]] == 12


def test_remove_item_from_basket_removing_possible():
    """
    Testcase to test removing items from a basket when removing an item is possible.
    """
    basket = Basket()
    basket.add_item(items[0], 3)
    basket.remove_item(items[0], 2)
    assert basket.items[items[0]] == 1


def test_remove_item_amount_negative():
    """
    Testcase where item to be removed's amount is negative.
    """
    basket = Basket()
    basket.add_item(items[0], 3)
    try:
        basket.remove_item(items[0], -5)
        assert False
    except ValueError:
        assert True


def test_remove_item_item_not_in_basket():
    """
    Testcase where item to be removed does not exist in the basket.
    """
    basket = Basket()
    try:
        basket.remove_item(items[0], 2)
        assert False
    except ValueError:
        assert True


def test_remove_item_amount_more_than_in_basket():
    """
    Testcase where item to be removed's amount is larger than the amount in the basket.
    """
    basket = Basket()
    basket.add_item(items[1], 3)
    try:
        basket.remove_item(items[1], 5)
        assert False
    except ValueError:
        assert True


def test_calculate_cost():
    """
    Testcase to test whether the cost of the basket is calculated correctly.
    """
    basket = Basket()
    basket.add_item(items[0], 5)
    assert basket.cost == 10
    basket.add_item(items[2], 2)
    assert basket.cost == 2010


def test_get_purchase_log_entry():
    """
    Testcase to test whether the purchase log entry function works correctly.
    """
    basket = Basket()
    basket.add_item(items[2], 1)
    basket.add_item(items[1], 5)
    log = basket.get_purchase_log_entry()
    
    assert log[1] in ["Car x 1, pear x 5", "pear x 5, Car x 1"]


def test_customer_purchase_history_order():
    """
    Testcase to test whether customer sees his purchase history in the correct order.
    """
    customer = Customer(1, 150, False)
    
    purchase1 = ("11/04/2023 12:34", "Eggs x 1")
    purchase2 = ("12/04/2023 11:15", "Chips x 5, Milk x 1")

    customer.history.extend([purchase1, purchase2])

    assert customer.get_history() == [purchase2, purchase1]


def test_regular_customer_purchase_purchase_possible():
    """
    Testcase to test whether a normal customer can make a purchase when it is possible.
    """
    customer = Customer(1, 200, False)
    customer.basket.add_item(items[0], 5)
    customer.basket.add_item(items[1], 2)
    customer.make_purchase()
    
    assert customer.money == 180


def test_gold_customer_purchase_purchase_possible():
    """
    Testcase to check whether gold customer gets their purchase cheaper.
    """
    customer = Customer(1, 200, True)
    customer.basket.add_item(items[0], 5)
    customer.make_purchase()
    
    assert customer.money == 191


def test_customer_purchase_not_enough_money():
    """
    Testcase to test when customer is trying to make a purchase but does not have enough money.
    """
    customer = Customer(1, 5, False)
    customer.basket.add_item(items[0], 5)
    try:
        customer.make_purchase()
        assert False
    except ValueError:
        assert True


def test_gold_customer_does_not_have_enough_regularly_but_does_because_of_price_reduction():
    """
    Testcase where gold customer does not have enough money to make a purchase at full price but does have enough due to price reduction.
    """
    customer = Customer(1, 9, True)
    customer.basket.add_item(items[0], 5)
    customer.make_purchase()

    assert customer.money == 0


def test_add_customer():
    """
    Testcase to add a customer to a store.
    """
    store = Store()
    store.add_customer(100, False)
    
    assert len(store.customers) == 1


def test_add_customers_customers_id_not_same():
    """
    Testcase to test whether the ID's of created clients arent the same.
    """
    store = Store()
    for i in range(100):
        store.add_customer(100, False)
    
    used_ids = set()
    for customer in store.customers:
        if customer.id in used_ids:
            assert False
        else:
            used_ids.add(customer.id)
    assert True


def test_add_customer_with_negative_money():
    """
    Testcase where customer to add to store has negative money
    """
    store = Store()
    store.items = {
        items[0]: 10,
        items[1]: 6,
        items[2]: 2
    }
    try:
        store.add_customer(-1, False)
        assert False
    except ValueError:
        assert True


def test_add_customer_with_zero_money():
    """Testcase where customer to add to store has no money."""
    store = Store()
    store.items = {
        items[0]: 10,
        items[1]: 6,
        items[2]: 2
    }
    store.add_customer(0, False)
    assert len(store.customers) == 1


def test_normal_customer_makes_purchase_purchase_possible():
    """
    Testcase where customer makes a purchase and it is possible to make one.
    """
    store = Store()
    store.items = {
        items[0]: 10,
        items[1]: 6,
        items[2]: 2
    }
    store.add_customer(20, False)
    customer: Customer = store.customers[0]
    customer.basket.add_item(items[0], 3)
    
    store.make_purchase(customer)
    # Check if stock in store went down
    assert store.items[items[0]] == 7
    assert store.items[items[1]] == 6
    assert store.items[items[2]] == 2
    # Check if customer's money went down
    assert customer.money == 14

    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    log = "apple x 3"
    entry = (time, log)
    # Check if purchase is in stores purchase log
    assert store.purchases[customer][0] == entry
    # Check if purchase is in customer's purchase log
    assert customer.history[0] == entry
    # Check if customers basket is empty
    assert customer.basket.empty is True


def test_customer_makes_purchase_but_not_enough_items_in_stock():
    """
    Testcase where customer tries to make a purchase but there is not enough items in stock.
    """
    store = Store()
    store.items[items[2]] = 1
    store.add_customer(20000, True)
    customer: Customer = store.customers[0]

    customer.basket.add_item(items[2], 2)
    try:
        store.make_purchase(customer)
        assert False
    except ValueError:
        assert True


if __name__ == "__main__":
    # Basket class tests
    test_add_item_to_basket_adding_possible()
    test_add_item_to_basket_amount_negative()
    test_add_item_to_basket_some_items_already_in_basket()
    test_remove_item_from_basket_removing_possible()
    test_remove_item_amount_negative()
    test_remove_item_item_not_in_basket()
    test_remove_item_amount_more_than_in_basket()
    test_calculate_cost()
    test_get_purchase_log_entry()

    # Customer class tests
    test_customer_purchase_history_order()
    test_regular_customer_purchase_purchase_possible()
    test_gold_customer_purchase_purchase_possible()
    test_customer_purchase_not_enough_money()
    test_gold_customer_does_not_have_enough_regularly_but_does_because_of_price_reduction()

    # Store class tests
    test_add_customer()
    test_add_customers_customers_id_not_same()
    test_add_customer_with_negative_money()
    test_add_customer_with_zero_money()
    test_normal_customer_makes_purchase_purchase_possible()
    test_customer_makes_purchase_but_not_enough_items_in_stock()