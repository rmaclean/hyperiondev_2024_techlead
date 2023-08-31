import internals.coffeeEngine


class Machine:
    def __init__(self):
        self.milk_available = 200
        self.water_available = 750
        self.beans_available = 250
        self.cup_size = 200

    def makeOrder(self, order):
        order_type = order["type"]
        match order_type:
            case "coffee":
                return internals.coffeeEngine.CoffeeEngine().makeACoffee(order, self)
            case _:
                print(f"Sorry, I do not know how to make {order_type} yet")
                return None
